from getpass import getpass
from mysql.connector import connect, error
from datetime import datetime, timezone
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from newstream_user.models import UserMeta
from newstream.functions import round_half_up
from donations.models import Donation, DonationPaymentMeta, Subscription, SubscriptionPaymentMeta, STATUS_ACTIVE, STATUS_PROCESSING, STATUS_PAUSED, STATUS_CANCELLED, STATUS_INACTIVE, STATUS_COMPLETE, STATUS_REFUNDED, STATUS_REVOKED, STATUS_FAILED

User = get_user_model()

class Command(BaseCommand):
    help = 'Migrate donors and related data from Givewp\'s database'

    def add_arguments(self, parser):
        parser.add_argument('donor_ids', nargs='+', type=int)

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

    def handle(self, *args, **options):
        try:
            with connect(
                host="localhost",
                user=input("Enter username: "),
                password=getpass("Enter password: "),
                database="support_clone"
            ) as connection:
                for donor_id in options['donor_ids']:
                    select_donors_lj_meta_query = "select id, email, date_created, dnm.* from wp_give_donors dn left join wp_give_donormeta dnm on dn.id = dnm.donor_id where dn.id = %d;" % donor_id
                    select_subscriptions_query = "select * from wp_give_subscriptions where customer_id = %d;" % donor_id
                    with connection.cursor() as cursor:
                        cursor.execute(select_donors_lj_meta_query)
                        result = cursor.fetchall()
                        newUser = None
                        for i, row in enumerate(result):
                            if i == 0:
                                # Add the user first
                                newUser = User.objects.create_user(username=row[1], email=row[1], password='password628')
                                newUser.save()
                            if row[5] == '_give_donor_first_name':
                                newUser.first_name = row[6]
                            elif row[5] == '_give_donor_last_name':
                                newUser.last_name = row[6]
                            else:
                                um = UserMeta(user=newUser, field_key=row[5], field_value=row[6])
                                um.save()
                        newUser.save()
                        # add subscriptions
                        cursor.execute(select_subscriptions_query)
                        result = cursor.fetchall()
                        newSubscription = None
                        for i, row in enumerate(result):
                            newSubscription = Subscription(
                                is_test=True,
                                profile_id=row[13],
                                user=newUser,
                                gateway=self.donation.gateway,
                                recurring_amount=round_half_up(row[4], 2),
                                currency=currencyCodeToKey(self.data['currency']),
                                recurring_status=self.subscription_status_mapping(row[12]),
                                created_at=datetime.strptime(row[10], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                            )

        except Error as e:
            self.stdout.write(e)