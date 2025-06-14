import stripe
from django.conf import settings
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser, UserProfile, UserProfileType
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.db import transaction

from datetime import datetime, timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

SUBSCRIPTION_MAP = {
    'price_1RRymmB3a037ikFEaqDq2J8N': 'basic',
    'price_1RQV0aB3a037ikFEAEbdKvqx': 'tourist',
    'price_1RQwW7B3a037ikFEidRPP1SS': 'guide',
    'price_1RSRkBB3a037ikFE3FNMd1ub': ':)',
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

        if event['type'] == 'invoice.paid':
            invoice = event['data']['object']
            print("== RAW INVOICE ==")

            subscription_id = (
                invoice.get("lines", {})
                .get("data", [{}])[0]
                .get("parent", {})
                .get("subscription_item_details", {})
                .get("subscription")
            )
            print("Extracted subscription_id:", subscription_id)

            if not subscription_id:
                print('❌ Brak subscription_id – przerywam')
                return HttpResponse(status=200)

            sessions = stripe.checkout.Session.list(subscription=subscription_id, limit=1)
            if not sessions.data:
                print("❌ Nie znaleziono session po subscription_id")
                return HttpResponse(status=200)

            session = sessions.data[0]
            session_id = session.id
            print("✅ Session ID:", session_id)

            try:
                with transaction.atomic():
                    order = Order.objects.get(stripe_session_id=session_id)
                    order.is_paid = True
                    order.save()
                    user = order.user

                    if order.subscription_type == 'tourist':
                        profile = user.get_default_profile()
                        profile_type = UserProfileType.objects.filter(code='tourist').first()
                        profile.type = profile_type
                        profile.save()
                    elif order.subscription_type == 'guide':
                        profile_type = UserProfileType.objects.filter(code='guide').first()
                        profile = UserProfile.objects.create(
                            user=user,
                            is_default=True,
                            type=profile_type
                        )
                        profile.save()

                    subscription = stripe.Subscription.retrieve(subscription_id)

                    current_period_end_ts = subscription["items"]["data"][0]["current_period_end"]
                    if not current_period_end_ts:
                        print("❌ current_period_end nie istnieje – subskrypcja może być anulowana lub nieaktywna")
                        return HttpResponse(status=200)

                    current_period_end = datetime.fromtimestamp(current_period_end_ts, tz=timezone.utc)
                    print('✅ current_period_end:', current_period_end)

                    user.subscription_active = True
                    user.subscription_plan = order.subscription_type
                    user.stripe_subscription_id = subscription_id
                    user.subscription_ends_at = current_period_end
                    user.save()

            except Order.DoesNotExist:
                print(f"❌ Nie znaleziono zamówienia dla session_id={session_id}")

        elif event['type'] == 'invoice.payment_failed':
            subscription = (
                invoice.get("lines", {})
                .get("data", [{}])[0]
                .get("parent", {})
                .get("subscription_item_details", {})
                .get("subscription")
            )
            try:
                user = CustomUser.objects.get(stripe_subscription_id=subscription)
                print(f"Payment failed for {user.username}")
            except CustomUser.DoesNotExist:
                print("Nie znaleziono profilu użytkownika")

        elif event['type'] == 'customer.subscription.deleted':
            subscription_id = (
                invoice.get("lines", {})
                .get("data", [{}])[0]
                .get("parent", {})
                .get("subscription_item_details", {})
                .get("subscription")
            )

            try:
                user = CustomUser.objects.get(stripe_subscription_id=subscription_id)
                user.subscription_active = False
                user.subscription_ends_at = None
                user.save()
                print(f"Subscription {subscription_id} deactivated.")
            except CustomUser.DoesNotExist:
                print("Nie znaleziono subskrypcji.")

        return HttpResponse(status=200)


@extend_schema(tags=["payments"], operation_id="cancel_subscription")
class CancelSubscriptionView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        subscription_id = user.stripe_subscription_id

        if not subscription_id:
            return Response(
                {"error": "Użytkownik nie ma aktywnej subskrypcji."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            canceled = stripe.Subscription.modify(subscription_id, cancel_at_period_end=True)

            user.stripe_subscription_id = None
            user.save(update_fields=["stripe_subscription_id",])

            return Response({
                "message": "Subskrypcja została anulowana.",
                "stripe_status": canceled.status,
                "stripe_id": canceled.id,
            })

        except stripe.error.StripeError as e:
            return Response(
                {"error": f"Błąd Stripe: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
