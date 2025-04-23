from django.urls import path
from .views.frankfurter_views import CurrencyRateView

urlpatterns = [
    path("currency/", CurrencyRateView.as_view(), name="currency_api"),
]