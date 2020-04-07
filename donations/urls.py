from django.urls import path
from . import views

donation_urlpatterns = [
    path('onetime-donation', views.onetime_form, name='onetime-donation'),
    path('recurring-donation', views.recurring_form, name='recurring-donation'),
]
