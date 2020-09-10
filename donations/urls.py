from django.urls import path

from . import views
from .payment_gateways.stripe import create_checkout_session, verify_stripe_response, return_from_stripe, cancel_from_stripe

app_name = 'donations'
urlpatterns = [
    path('donate/', views.donate,
         name='donate'),
    path('cancel-recurring/', views.cancel_recurring,
         name='cancel-recurring'),
    path('donation-details/', views.donation_details,
         name='donation-details'),
    path('create-stripe-session/', create_checkout_session,
         name='create-stripe-session'),
    path('verify-gateway-response/', views.verify_gateway_response,
         name='verify-gateway-response'),
    path('return-from-gateway/', views.return_from_gateway,
         name='return-from-gateway'),
    path('verify-stripe-response/', verify_stripe_response,
         name='verify-stripe-response'),
    path('return-from-stripe/', return_from_stripe,
         name='return-from-stripe'),
    path('cancel-from-stripe/', cancel_from_stripe,
         name='cancel-from-stripe'),
    path('thank-you/', views.thank_you, name='thank-you'),
    path('cancelled/', views.cancelled, name='cancelled'),
    path('my-donations/', views.my_donations, name='my-donations'),
    path('my-renewals/<int:id>/', views.my_renewals, name='my-renewals'),
]
