from django.urls import path
from . import views

app_name = 'donations'
urlpatterns = [
    path('donate/', views.donate,
         name='donate'),
    path('personal-info/', views.personal_info,
         name='personal-info'),
    path('donation-details/', views.donation_details,
         name='donation-details'),
    path('verify-gateway-response/', views.verify_gateway_response,
         name='verify-gateway-response'),
    path('return-from-gateway/', views.return_from_gateway,
         name='return-from-gateway'),
    path('thank-you/', views.thank_you, name='thank-you'),
    path('my-donations/', views.my_donations, name='my-donations'),
]
