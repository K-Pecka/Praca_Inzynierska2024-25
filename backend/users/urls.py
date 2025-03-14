from django.urls import path
from .views import confirm_email, check_access

urlpatterns = [
    path('confirm-email/<uidb64>/<token>/', confirm_email, name='confirm_email'),
    path('check/user/<user_pk>/permission/<perm_code>/action/<perm_action>/', check_access, name='check-permission'),
]
