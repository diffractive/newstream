from django.db.models import Q

from newstream.functions import raiseObjectNone
from donations.models import Donation, STATUS_PENDING
from donations.payment_gateways.gateway_factory import PaymentGatewayFactory
from donations.payment_gateways._2c2p.gateway import Gateway_2C2P


class Factory_2C2P(PaymentGatewayFactory):
    @staticmethod
    def initGateway(request, donation, subscription):
        return Gateway_2C2P(request, donation, subscription)

    @staticmethod
    def initGatewayByVerification(request):
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

                return Factory_2C2P.initGateway(request, donation, None)

        # case two: standard payment response from 2C2P(either onetime or recurring payment's initial donation)
        if 'user_defined_1' in request.POST and request.POST['user_defined_1'] != '':
            donation = Donation.objects.get(
                pk=int(request.POST['user_defined_1']))
            if not donation:
                raiseObjectNone(
                    'Donation id - {} from user_defined_1 is not found in the omp database.'.format(request.POST['user_defined_1']))
            else:
                return Factory_2C2P.initGateway(request, donation, None)

    @staticmethod
    def initGatewayByReturn(request):
        pass
