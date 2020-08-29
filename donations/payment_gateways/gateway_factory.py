from django.db.models import Q

from newstream.functions import raiseObjectNone
from donations.payment_gateways.core import PaymentGatewayManager
from donations.payment_gateways._2c2p import Gateway_2C2P
from donations.payment_gateways.paypal import Gateway_Paypal
from donations.payment_gateways.stripe import Gateway_Stripe
from donations.models import Donation, STATUS_PENDING


class PaymentGatewayFactory(object):

    @staticmethod
    def initGateway(request, donation):
        """ Instantiate the specific type of payment gateway manager with current request and specified gateway and donation record """
        if not donation:
            raiseObjectNone(
                'Donation object cannot be none while initializing BasePaymentGateway class')
        if donation.gateway.is_2c2p():
            return Gateway_2C2P(request, donation)
        elif donation.gateway.is_paypal():
            return Gateway_Paypal(request, donation)
        elif donation.gateway.is_stripe():
            return Gateway_Stripe(request, donation)
        else:
            raiseObjectNone(
                'The Provided gateway has not been implemented yet')

    @staticmethod
    def initGatewayByVerification(request):
        """ Instantiate the specific type of payment gateway manager with current request (expected to be a form of verification response from gateway server) """
        # case one: recurring renewals from 2C2P
        if 'recurring_unique_id' in request.POST and request.POST['recurring_unique_id'] != '':
            # First distinguish between initial and renewal payment responses
            # The parent donation should have both the matching recurring_unique_id and order_prefix, thus producing two records exactly
            # the -5 position is to cut away the 0000n numbering on the order_id to just match the order prefixx
            DonationSet = Donation.objects.filter((Q(payment_metas__field_key='recurring_unique_id', payment_metas__field_value=request.POST['recurring_unique_id']) | Q(
                payment_metas__field_key='order_prefix', payment_metas__field_value=request.POST['order_id'][:-5])) & Q(parent_donation__isnull=True) & Q(id=int(request.POST['user_defined_1'])))
            if len(DonationSet) == 2:
                pDonation = DonationSet[0]

                # Create new donation record from pDonation
                donation = Donation(
                    order_number=request.POST['order_id'],
                    user=pDonation.user,
                    form=pDonation.form,
                    gateway=pDonation.gateway,
                    is_recurring=True,
                    donation_amount=Gateway_2C2P.extract_payment_amount(
                        request.POST['currency'], request.POST['amount']),
                    currency=pDonation.currency,
                    payment_status=STATUS_PENDING,
                    parent_donation=pDonation
                )
                try:
                    donation.save()
                except Exception as e:
                    # Should rarely happen, but in case some bugs or order id repeats itself
                    print(str(e))
                    raise e

                return Gateway_2C2P(request, donation)

        # case two: standard payment response from 2C2P(either onetime or recurring payment's initial donation)
        if 'user_defined_1' in request.POST and request.POST['user_defined_1'] != '':
            donation = Donation.objects.get(
                pk=int(request.POST['user_defined_1']))
            if not donation:
                raiseObjectNone(
                    'Donation id - {} from user_defined_1 is not found in the omp database.'.format(request.POST['user_defined_1']))
            else:
                return Gateway_2C2P(request, donation)

        # todo: Add Stripe's and PayPal's verification listener logic
