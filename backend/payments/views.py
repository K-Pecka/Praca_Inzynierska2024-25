import stripe
from django.conf import settings
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import UserProfile
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.decorators import method_decorator

stripe.api_key = settings.STRIPE_SECRET_KEY

SUBSCRIPTION_MAP = {
    'prod_SMiD43Ponu9enH': 'Podstawowy',
    'prod_SLBNtcXwVv0mvV': 'Turysta',
    'prod_SLdnNHfZFFu0Sj': 'Podróżnik',
}

@extend_schema(
    tags=["payments"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "price_id": {"type": "string", "example": "price_12345"}
            },
            "required": ["price_id"]
        }
    },
    responses={200: None}
)
class CreateCheckoutSessionView(APIView):
    def post(self, request):
        user = request.user
        price_id = request.data.get("price_id")

        if not price_id:
            return Response({'error': 'Missing price_id'}, status=status.HTTP_400_BAD_REQUEST)

        plan_name = SUBSCRIPTION_MAP.get(price_id, "Unknown")

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url='https://plannder.com/payment/success',
                cancel_url='https://plannder.com/payment/cancel',
            )

            Order.objects.create(
                user=user,
                stripe_session_id=session.id,
                is_paid=False,
                subscription_type=plan_name
            )

            return Response({'checkout_url': session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
@extend_schema(exclude=True)
class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            session_id = session.get('id')
            subscription_id = session.get('subscription')

            try:
                order = Order.objects.get(stripe_session_id=session_id)
                order.is_paid = True
                order.save()

                user = order.user
                profile = user.get_default_profile()
                user.subscription_active = True
                user.subscription_plan = order.subscription_type
                user.stripe_subscription_id = subscription_id
                profile.save()
            except Order.DoesNotExist:
                print("Nie znaleziono zamówienia.")

        elif event['type'] == 'invoice.payment_failed':
            subscription = event['data']['object'].get('subscription')
            try:
                profile = UserProfile.objects.get(stripe_subscription_id=subscription)
                print(f"Payment failed for {profile.user.username}")
            except UserProfile.DoesNotExist:
                print("Nie znaleziono profilu użytkownika")

        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            subscription_id = subscription.get('id')

            try:
                profile = UserProfile.objects.get(stripe_subscription_id=subscription_id)
                profile.subscription_active = False
                profile.save()
                print(f"Subscription {subscription_id} deactivated.")
            except UserProfile.DoesNotExist:
                print("Nie znaleziono subskrypcji.")

        return HttpResponse(status=200)