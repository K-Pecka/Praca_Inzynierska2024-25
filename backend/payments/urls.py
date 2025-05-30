from django.urls import path
from .views import CreateCheckoutSessionView, StripeWebhookView

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]