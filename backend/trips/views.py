from django.contrib.auth import login
from django.core.mail import send_mail

from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
# def login_with_token(request):
#     if request.method != 'GET':
#         return JsonResponse({'error': 'Niepoprawna metoda zapytania.'}, status=405)
#
#     token = request.GET.get('token')
#     if not token:
#         return JsonResponse({'error': 'Brak tokenu w linku.'}, status=400)
#
#     trip_access_token = get_trip_access_token(token)
#
#     user_profile = trip_access_token.user_profile
#     user = user_profile.user
