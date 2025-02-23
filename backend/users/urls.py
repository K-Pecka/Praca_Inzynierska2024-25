from django.urls import path
from .views import confirm_email


urlpatterns = [
    path('confirm-email/<uidb64>/<token>/', confirm_email, name='confirm_email'),
]
