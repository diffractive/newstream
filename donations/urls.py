from django.conf.urls import url
from . import views

app_name = 'donations'
urlpatterns = [
    url(r'^onetime-donation', views.onetime_form,
        name='onetime-donation'),
    url(r'^recurring-donation', views.recurring_form,
        name='recurring-donation'),
    url(r'^verify-gateway-response', views.verify_gateway_response,
        name='verify-gateway-response'),
    url(r'^return-from-gateway', views.return_from_gateway,
        name='return-from-gateway'),
    url(r'^thank-you', views.thank_you, name='thank-you'),
]
