from getpass import getpass
from subprocess import PIPE, Popen
from mysql.connector import connect
from datetime import datetime, timezone
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import transaction

from newstream_user.models import UserMeta
from newstream.functions import round_half_up
from donations.functions import gen_transaction_id
from donations.models import Donation, DonationPaymentMeta, Subscription, SubscriptionPaymentMeta, STATUS_ACTIVE, STATUS_PROCESSING, STATUS_PAUSED, STATUS_CANCELLED, STATUS_INACTIVE, STATUS_COMPLETE, STATUS_REFUNDED, STATUS_REVOKED, STATUS_FAILED
from site_settings.models import PaymentGateway, GATEWAY_STRIPE, GATEWAY_PAYPAL_OLD, GATEWAY_MANUAL, GATEWAY_OFFLINE

User = get_user_model()

class Command(BaseCommand):
    help = 'Migrate donors and related data from Givewp\'s database'

    def add_arguments(self, parser):
        parser.add_argument('donor_ids', nargs='+', type=int)
        
        # Named (optional) arguments
        parser.add_argument(
            '--test',
            action='store_true',
            help='Indicate data migrated is in test mode',
        )

        # Named (optional) arguments
        parser.add_argument(
            '--backupdb',
            action='store_true',
            help='Tell script to backup newstream db before migration',
        )

    def subscription_status_mapping(self, givewp_status):
        if givewp_status == 'active':
            return STATUS_ACTIVE
        if givewp_status == 'failing' or givewp_status == 'completed':
            return STATUS_INACTIVE
        if givewp_status == 'cancelled':
            return STATUS_CANCELLED
        if givewp_status == 'pending':
            return STATUS_PROCESSING
        return STATUS_INACTIVE

    def donation_status_mapping(self, givewp_status):
        if givewp_status == 'publish' or givewp_status == 'give_subscription':
            return STATUS_COMPLETE
        if givewp_status == 'pending' or givewp_status == 'processing':
            return STATUS_PROCESSING
        if givewp_status == 'refunded':
            return STATUS_REFUNDED
        if givewp_status == 'revoked':
            return STATUS_REVOKED
        if givewp_status == 'failed':
            return STATUS_FAILED
        if givewp_status == 'cancelled' or givewp_status == 'abandoned':
            return STATUS_CANCELLED
        return STATUS_FAILED

    def gateway_mapping(self, give_gateway):
        gateway_title = None
        if give_gateway == 'manual' or give_gateway == 'manual_donation':
            gateway_title = GATEWAY_MANUAL
        if give_gateway == 'offline':
            gateway_title = GATEWAY_OFFLINE
        if give_gateway == 'paypal':
            gateway_title = GATEWAY_PAYPAL_OLD
        if give_gateway == 'stripe':
            gateway_title = GATEWAY_STRIPE
        if gateway_title:
            return PaymentGateway.objects.get(title=gateway_title)
        else:
            raise ValueError('Cannot map payment gateway from givewp, the gateway: %s' % give_gateway)

    def paymentmode_mapping(self, give_payment_mode):
        if give_payment_mode == 'test':
            return True
        else:
            return False

    def print(self, msg):
        self.stdout.write(msg)

    def handle(self, *args, **options):
        if options['test']:
            is_test = True
        else:
            is_test = False
        # ask user if backup the newstream database
        if options['backupdb']:
            subp = Popen(["/bin/bash", "/srv/www/newstream/backup-db"], stdin=PIPE, stdout=PIPE)
            outputs, errors = subp.communicate()
            self.print("[√] Saved a backup of the newstream database at .backups/")
        else:
            self.print("...skipping database backup")

        try:
            with connect(
                host="localhost",
                user=input("Enter username: "),
                password=getpass("Enter password: "),
                database="support_clone"
            ) as connection:
                self.print("Connected to support_clone.")
                with transaction.atomic():
                    for donor_id in options['donor_ids']:
                        # select_donor_query = "select * from wp_give_donors where id = %d" % donor_id
                        select_donors_lj_meta_query = "select id, email, name, date_created, dnm.* from wp_give_donors dn left join wp_give_donormeta dnm on dn.id = dnm.donor_id where dn.id = %d;" % donor_id
                        select_subscriptions_query = "select * from wp_give_subscriptions where customer_id = %d;" % donor_id
                        with connection.cursor() as cursor:
                            self.print("...Now processing queries of givewp donor %d" % donor_id)
                            cursor.execute(select_donors_lj_meta_query)
                            donorMetaResult = cursor.fetchall()
                            newUser = None
                            um = None
                            for i, row in enumerate(donorMetaResult):
                                givewp_donor_email = row[1]
                                givewp_donor_name = row[2]
                                givewp_donormeta_key = row[6]
                                givewp_donormeta_value = row[7]
                                if i == 0:
                                    # Add the user first
                                    newUser = User.objects.create_user(username=givewp_donor_email, email=givewp_donor_email, password='password628')
                                    newUser.save()
                                    # save donor's name attribute as UserMeta as I am not sure how to correctly split the name into first and last names
                                    um = UserMeta(user=newUser, field_key='_give_donor_name', field_value=givewp_donor_name)
                                    um.save()
                                if givewp_donormeta_key == '_give_donor_first_name':
                                    newUser.first_name = givewp_donormeta_value
                                elif givewp_donormeta_key == '_give_donor_last_name':
                                    newUser.last_name = givewp_donormeta_value
                                else:
                                    um = UserMeta(user=newUser, field_key=givewp_donormeta_key, field_value=givewp_donormeta_value)
                                    um.save()
                            newUser.save()
                            self.print("[√] Created Newstream User (email: %s, name: %s)." % (newUser.email, newUser.fullname))

                            # add subscriptions
                            self.print("...Now processing queries of subscriptions of givewp donor %d" % donor_id)
                            cursor.execute(select_subscriptions_query)
                            subscriptionsResult = cursor.fetchall()
                            newSubscription = None
                            for i, row in enumerate(subscriptionsResult):
                                # extract givewp subscription data
                                givewp_subscription_id = row[0]
                                givewp_subscription_initial_amount = row[4]
                                givewp_parent_donation_id = row[8]
                                givewp_subscription_created = row[10]
                                givewp_subscription_status = row[12]
                                subscription_profile_id = row[13]
                                self.print("[info] givewp subscription id: %s" % givewp_subscription_id)
                                self.print("[info] givewp subscription amount: %s" % givewp_subscription_initial_amount)
                                self.print("[info] givewp subscription parent donation id: %s" % givewp_parent_donation_id)
                                self.print("[info] givewp subscription created at: %s" % givewp_subscription_created)
                                self.print("[info] givewp subscription status: %s" % givewp_subscription_status)
                                self.print("[info] givewp subscription profile id: %s" % subscription_profile_id)
                                # query data for subscription's parent donation
                                parent_donation_query = "select * from wp_posts where ID = %d;" % givewp_parent_donation_id
                                cursor.execute(parent_donation_query)
                                parentDonationResult = cursor.fetchone()
                                parent_donation_status = parentDonationResult[7]
                                parent_donation_datetime = parentDonationResult[3]
                                self.print("[info] givewp parent donation status: %s" % parent_donation_status)
                                self.print("[info] givewp parent donation created at: %s" % parent_donation_datetime)
                                # query data for parent donation's meta data
                                parent_donationmeta_query = "select * from wp_give_donationmeta where donation_id = %d;" % givewp_parent_donation_id
                                cursor.execute(parent_donationmeta_query)
                                parentDonationMetaResult = cursor.fetchall()
                                parentDonationMetaDict = {}
                                for meta in parentDonationMetaResult:
                                    parentDonationMetaDict[meta[2]] = meta[3]
                                # query data for renewals of the subscription
                                renewals_query = "select distinct donation_id from wp_give_donationmeta where meta_key = 'subscription_id' and meta_value = %d;" % givewp_subscription_id
                                cursor.execute(renewals_query)
                                renewalsResult = cursor.fetchall()

                                newSubscription = Subscription(
                                    is_test=self.paymentmode_mapping(parentDonationMetaDict['_give_payment_mode']),
                                    profile_id=subscription_profile_id,
                                    user=newUser,
                                    gateway=self.gateway_mapping(parentDonationMetaDict['_give_payment_gateway']),
                                    recurring_amount=round_half_up(givewp_subscription_initial_amount, 2),
                                    currency=parentDonationMetaDict['_give_payment_currency'],
                                    recurring_status=self.subscription_status_mapping(givewp_subscription_status),
                                    created_at=givewp_subscription_created.replace(tzinfo=timezone.utc)
                                )
                                newSubscription.save()
                                self.print("[√] Created Newstream Subscription (id: %d, profile_id: %s)" % (newSubscription.id, newSubscription.profile_id))

                                # add donations linked to this subscription(need to link with the new subscription id in Newstream)
                                # need to add the parent payment first, so it gets the smallest id among the renewals
                                parentDonation = Donation(
                                    is_test=newSubscription.is_test,
                                    subscription=newSubscription,
                                    transaction_id=parentDonationMetaDict['_give_payment_transaction_id'] if '_give_payment_transaction_id' in parentDonationMetaDict else gen_transaction_id(newSubscription.gateway),
                                    user=newUser,
                                    gateway=newSubscription.gateway,
                                    is_recurring=True,
                                    donation_amount=round_half_up(parentDonationMetaDict['_give_payment_total'], 2),
                                    currency=newSubscription.currency,
                                    payment_status=self.donation_status_mapping(parent_donation_status),
                                    donation_date=parent_donation_datetime.replace(tzinfo=timezone.utc),
                                )
                                parentDonation.save()
                                self.print("[√] Created Newstream Parent Donation (id: %d, amount: %s)" % (parentDonation.id, parentDonation.donation_amount))

                                # save all meta data as DonationPaymentMeta
                                for key, value in parentDonationMetaDict.items():
                                    # if newUser first name and last name empty, save once again
                                    if key == '_give_donor_billing_first_name' and not newUser.first_name:
                                        newUser.first_name = value
                                        newUser.save()
                                    if key == '_give_donor_billing_last_name' and not newUser.last_name:
                                        newUser.last_name = value
                                        newUser.save()
                                    dpm = DonationPaymentMeta(donation=parentDonation, field_key=key, field_value=value)
                                    dpm.save()
                                
                                # then add renewals as well
                                for renewalID in renewalsResult:
                                    # query data for renewal donation's meta data
                                    renewal_donation_query = "select * from wp_posts where ID = %d" % renewalID[0]
                                    cursor.execute(renewal_donation_query)
                                    renewalDonationResult = cursor.fetchone()
                                    renewal_donation_status = renewalDonationResult[7]
                                    renewal_donation_datetime = renewalDonationResult[3]
                                    self.print("[info] givewp renewal donation status: %s" % renewal_donation_status)
                                    self.print("[info] givewp renewal donation created at: %s" % renewal_donation_datetime)
                                    renewal_donationmeta_query = "select * from wp_give_donationmeta where donation_id = %d;" % renewalID[0]
                                    cursor.execute(renewal_donationmeta_query)
                                    renewalDonationMetaResult = cursor.fetchall()
                                    renewalDonationMetaDict = {}
                                    for meta in renewalDonationMetaResult:
                                        renewalDonationMetaDict[meta[2]] = meta[3]

                                    renewalDonation = Donation(
                                        is_test=parentDonation.is_test,
                                        subscription=newSubscription,
                                        transaction_id=renewalDonationMetaDict['_give_payment_transaction_id'] if '_give_payment_transaction_id' in renewalDonationMetaDict else gen_transaction_id(self.gateway_mapping(renewalDonationMetaDict['_give_payment_gateway'])),
                                        user=newUser,
                                        gateway=self.gateway_mapping(renewalDonationMetaDict['_give_payment_gateway']),
                                        is_recurring=True,
                                        donation_amount=round_half_up(renewalDonationMetaDict['_give_payment_total'], 2),
                                        currency=renewalDonationMetaDict['_give_payment_currency'],
                                        payment_status=self.donation_status_mapping(renewal_donation_status),
                                        donation_date=renewal_donation_datetime.replace(tzinfo=timezone.utc),
                                    )
                                    renewalDonation.save()
                                    self.print("[√] Created Newstream Renewal Donation (id: %d, amount: %s)" % (renewalDonation.id, renewalDonation.donation_amount))

                                    # save all meta data as DonationPaymentMeta
                                    for key, value in renewalDonationMetaDict.items():
                                        dpm = DonationPaymentMeta(donation=renewalDonation, field_key=key, field_value=value)
                                        dpm.save()

                            # todo: add one-time donations

        except Exception as e:
            self.print(str(e))
            self.print("...rolling back previous changes.")

        