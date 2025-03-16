import base64
import secrets
import json

from urllib.parse import urlencode

from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

from trips.models import Trip, TripAccessToken
from users.models import CustomUser


def create_invitation_link(request, trip_id, user):
    token = TripAccessToken.generate_token()
    url = reverse('trip_join')
    trip = Trip.objects.by_id(trip_id)

    try:
        user_profile = user.get_default_profile()

        token_instance, created = TripAccessToken.objects.get_or_create(
            trip=trip,
            user_profile=user_profile,
            defaults={'token': token}
        )

        query_params = urlencode({'token': token})
        invitation_link = f"{settings.API_URL}{url}?{query_params}"

        if not created:
            token_instance.token = token
            token_instance.save()

        return invitation_link
    except TripAccessToken.DoesNotExist:
        return JsonResponse({'error': 'Token nie został stworzony!'}, status=404)


def send_trip_invitation_link(request, trip_id, user, name, date, email):
    subject = 'Zaproszenie do wycieczki Plannder'
    trip = Trip.objects.get(id=trip_id)
    invitation_link = create_invitation_link(request=request, trip_id=trip_id, user=user)
    html_message = render_to_string('emails/trip_invitation_email.html', {
        'name': name,
        'trip_name': trip.name,
        'date': date,
        'trip_link': invitation_link
    })
    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email,],
        html_message=html_message,
    )

@csrf_exempt
def invite_user(request, trip_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dane przekazane w niepoprawny sposób'})

        name = data.get('name')
        date = data.get('date')
        email = data.get('email')
        user = data.get('user')
        is_guest = data.get('is_guest')

        if is_guest:
            user = CustomUser.create_guest_account(name, email)
        elif user is None:
            return JsonResponse({'error': 'Użytkownik jest wymagany, przekaż go w zapytaniu lub zaznacz opcję gościa.'})

        send_trip_invitation_link(request=request, trip_id=trip_id, user=user, name=name, date=date, email=email)
        return JsonResponse({"message": "Zaproszenie wysłane!"})

    return JsonResponse({"error": "Niepoprawna metoda zapytania"}, status=405)


@csrf_exempt
def join_from_link(request):
    if request.method == 'GET':
        try:
            token = request.GET.get('token')

            if not token:
                return JsonResponse({'error': 'Brak tokenu w linku.'}, status=400)

            trip_access_token = TripAccessToken.objects.by_token(token)

            if not trip_access_token:
                raise TripAccessToken.DoesNotExist

            trip = trip_access_token.trip
            user_profile = trip_access_token.user_profile

            Trip.add_member(trip, user_profile)
            return JsonResponse({"message": "Użytkownik dołączył do wycieczki!"})
        except TripAccessToken.DoesNotExist:
            return JsonResponse({'error': 'Podany token nie istnieje.'}, status=404)
    return JsonResponse({'error': 'Niepoprawna metoda zapytania.'}, status=405)
