from django.urls import path

from donations import views
from donations.payment_gateways._2c2p.views import verify_2c2p_response, return_from_2c2p
from donations.payment_gateways.stripe.views import create_checkout_session, verify_stripe_response, return_from_stripe, cancel_from_stripe

app_name = 'donations'
urlpatterns = [
    path('donate/', views.donate,
         name='donate'),
    path('cancel-recurring/', views.cancel_recurring,
         name='cancel-recurring'),
    path('donation-details/', views.donation_details,
         name='donation-details'),
    path('verify-2c2p-response/', verify_2c2p_response,
         name='verify-2c2p-response'),
    path('return-from-2c2p/', return_from_2c2p,
         name='return-from-2c2p'),
    path('create-stripe-session/', create_checkout_session,
         name='create-stripe-session'),
    path('verify-stripe-response/', verify_stripe_response,
         name='verify-stripe-response'),
    path('return-from-stripe/', return_from_stripe,
         name='return-from-stripe'),
    path('cancel-from-stripe/', cancel_from_stripe,
         name='cancel-from-stripe'),
    path('thank-you/', views.thank_you, name='thank-you'),
    path('cancelled/', views.cancelled, name='cancelled'),
    path('my-onetime-donations/', views.my_onetime_donations, name='my-onetime-donations'),
    path('my-recurring-donations/', views.my_recurring_donations, name='my-recurring-donations'),
    path('my-renewals/<int:id>/', views.my_renewals, name='my-renewals'),
]
