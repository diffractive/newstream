from donations.functions import raiseObjectNone
from donations.payment_gateways.core import PaymentGatewayManager
from donations.payment_gateways._2c2p import Gateway_2C2P
from donations.payment_gateways.paypal import Gateway_Paypal
from donations.models import Donation, STATUS_PENDING
# todo: Add Stripe's payment gateway import


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
        # todo: Add Stripe's Gateway init line
        else:
            raiseObjectNone(
                'The Provided gateway has not been implemented yet')

    @staticmethod
    def initGatewayByVerification(request):
        """ Instantiate the specific type of payment gateway manager with current request (expected to be a form of verification response from gateway server) """
        # case one: recurring renewals from 2C2P
        if 'recurring_unique_id' in request.POST:
            # Find the parent donation
            pDonationSet = Donation.objects.filter(
                parent_donation__isnull=True, metas__field_key='recurring_unique_id', metas__field_value=request.POST['recurring_unique_id']).distinct()
            if not pDonationSet:
                raiseObjectNone('Recurring unique id: {} has no initial donation found'.format(
                    request.POST['recurring_unique_id']))
            else:
                pDonation = pDonationSet[0]

                # Create new donation record from pDonation
                donation = Donation(
                    order_number=request.POST['order_id'],
                    donor=pDonation.donor,
                    form=pDonation.form,
                    gateway=pDonation.gateway,
                    is_recurring=True,
                    # todo: need to actually convert from POST['amount'] to db format, since future renewals might be updated
                    donation_amount=pDonation.donation_amount,
                    currency=pDonation.currency,
                    is_create_account=pDonation.is_create_account,
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
        if 'user_defined_1' in request.POST:
            donation = Donation.objects.get(
                pk=int(request.POST['user_defined_1']))
            if not donation:
                raiseObjectNone(
                    'Donation id - {} from user_defined_1 is not found in the omp database.'.format(request.POST['user_defined_1']))
            else:
                return Gateway_2C2P(request, donation)

        # todo: add paypal and stripe's verification listener logic
