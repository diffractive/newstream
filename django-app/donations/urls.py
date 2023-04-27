from django.urls import path

from donations import views
from donations.payment_gateways._2c2p.views import verify_2c2p_response, return_from_2c2p
from donations.payment_gateways.stripe.views import create_checkout_session, verify_stripe_response, return_from_stripe, cancel_from_stripe
from donations.payment_gateways.paypal.views import create_paypal_transaction, verify_paypal_response, capture_paypal_order, return_from_paypal, cancel_from_paypal
from donations.payment_gateways.paypal_legacy.views import verify_paypal_legacy_response

app_name = 'donations'
urlpatterns = [
    path('donate/', views.donate, name='donate'),
    path('register-signin/', views.register_signin, name='register-signin'),
    path('confirm-donation/', views.confirm_donation, name='confirm-donation'),
    # path('donation-details/', views.donation_details, name='donation-details'),
    path('edit-recurring/<int:id>/', views.edit_recurring, name='edit-recurring'),
    path('toggle-recurring/', views.toggle_recurring, name='toggle-recurring'),
    path('cancel-recurring/', views.cancel_recurring, name='cancel-recurring'),
    # path('verify-2c2p-response/', verify_2c2p_response, name='verify-2c2p-response'),
    # path('return-from-2c2p/', return_from_2c2p, name='return-from-2c2p'),
    path('create-stripe-session/', create_checkout_session, name='create-stripe-session'),
    path('verify-stripe-response/', verify_stripe_response, name='verify-stripe-response'),
    path('return-from-stripe/', return_from_stripe, name='return-from-stripe'),
    path('cancel-from-stripe/', cancel_from_stripe, name='cancel-from-stripe'),
    path('create-paypal-transaction/', create_paypal_transaction, name='create-paypal-transaction'),
    path('return-from-paypal/', return_from_paypal, name='return-from-paypal'),
    path('cancel-from-paypal/', cancel_from_paypal, name='cancel-from-paypal'),
    path('verify-paypal-response/', verify_paypal_response, name='verify-paypal-response'),
    path('verify-paypal-legacy-response/', verify_paypal_legacy_response, name='verify-paypal-legacy-response'),
    path('thank-you/', views.thank_you, name='thank-you'),
    path('cancelled/', views.cancelled, name='cancelled'),
    path('revoked/', views.revoked, name='revoked'),
    path('my-onetime-donations/', views.my_onetime_donations, name='my-onetime-donations'),
    path('my-recurring-donations/', views.my_recurring_donations, name='my-recurring-donations'),
    path('my-renewals/<int:id>/', views.my_renewals, name='my-renewals'),
    path('export-donations/', views.export_donations, name='export-donations'),
    path('export-subscriptions', views.export_subscriptions, name='export-subscriptions'),
    path('export-donors/', views.export_donors, name='export-donors')
]
