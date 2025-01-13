from django.urls import path
from .api_views import UserCreateAPIView, UserUpdateAPIView, UserUpdatePasswordAPIView

urlpatterns = [
    path('', UserCreateAPIView.as_view(), name='create-user'),
    path('', UserUpdateAPIView.as_view(), name='update-user'),
    path('password/', UserUpdatePasswordAPIView.as_view(), name='update-user-password'),
]
