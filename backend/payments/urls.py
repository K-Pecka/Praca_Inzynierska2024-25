from django.urls import path
from .views import CreateCheckoutSessionView, StripeWebhookView, CancelSubscriptionView

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path("subscription/cancel/", CancelSubscriptionView.as_view(), name="cancel-subscription"),
]
