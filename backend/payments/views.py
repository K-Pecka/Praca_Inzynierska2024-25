import json

import stripe
from django.conf import settings
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import CustomUser
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from datetime import datetime, timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

SUBSCRIPTION_MAP = {
    'price_1RRymmB3a037ikFEaqDq2J8N': 'Podstawowy',
    'price_1RQV0aB3a037ikFEAEbdKvqx': 'Turysta',
    'price_1RQwW7B3a037ikFEidRPP1SS': 'Przewodnik',
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

            print(f'ssssssssssssssssssssssssssssss {session.id}')

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
        print('##########################################################################')
        payload = request.body
        print('payload', payload)
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        print(f'event type: {event["type"]}')
        print("====== FULL STRIPE EVENT ======")
        print(json.dumps(event, indent=2))
        print("================================")

        if event['type'] == 'invoice.paid':
            print('XDXDXD')
            invoice = event['data']['object']
            subscription_id = None
            print("== RAW INVOICE ==")

            try:
                subscription_id = (
                    invoice.get('lines', {})
                    .get('data', [{}])[0]
                    .get('parent', {})
                    .get('subscription_item_details', {})
                    .get('subscription')
                )
            except Exception as e:
                pass

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
                print('XD1')
                order = Order.objects.get(stripe_session_id=session_id)
                order.is_paid = True
                order.save()
                print('XD2')
                user = order.user
                subscription = stripe.Subscription.retrieve(subscription_id)
                print("📦 Subskrypcja z Stripe:", json.dumps(subscription, indent=2))

                current_period_end_ts = subscription.get('current_period_end')
                if not current_period_end_ts:
                    print("❌ current_period_end nie istnieje – subskrypcja może być anulowana lub nieaktywna")
                    return HttpResponse(status=200)
                try:
                    current_period_end_ts = subscription["items"]["data"][0]["current_period_end"]
                    current_period_end = datetime.fromtimestamp(current_period_end_ts, tz=timezone.utc)
                except (KeyError, IndexError) as e:
                    print(f"❌ Błąd przy pobieraniu current_period_end: {e}")
                    return HttpResponse(status=200)
                print('XD3')
                user.subscription_active = True
                user.subscription_plan = order.subscription_type
                user.stripe_subscription_id = subscription_id
                print('XD4')
                user.subscription_ends_at = current_period_end
                user.save()

            except Order.DoesNotExist:
                print("Nie znaleziono zamówienia.")

        elif event['type'] == 'invoice.payment_failed':
            print('fdgdfgdfggdfg')
            subscription = event['data']['object'].get('subscription')
            try:
                user = CustomUser.objects.get(stripe_subscription_id=subscription)
                print(f"Payment failed for {user.username}")
            except CustomUser.DoesNotExist:
                print("Nie znaleziono profilu użytkownika")

        elif event['type'] == 'customer.subscription.deleted':
            print('grfhfghfghfgh')
            subscription = event['data']['object']
            subscription_id = subscription.get('id')

            try:
                user = CustomUser.objects.get(stripe_subscription_id=subscription_id)
                user.subscription_active = False
                user.subscription_ends_at = None
                user.save()
                print(f"Subscription {subscription_id} deactivated.")
            except CustomUser.DoesNotExist:
                print("Nie znaleziono subskrypcji.")

        return HttpResponse(status=200)