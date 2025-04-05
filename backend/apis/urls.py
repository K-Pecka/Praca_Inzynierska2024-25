from django.urls import path
from .views.frankfurter_views import currency_rate

urlpatterns = [
    path("currency/", currency_rate, name="currency_api"),
]