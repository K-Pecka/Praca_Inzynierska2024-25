from django.urls import path
from .api_views import UserCreateAPIView, UserUpdateAPIView, UserUpdatePasswordAPIView


urlpatterns = [
    path('', UserUpdateAPIView.as_view(), name='update-user'),
    path('create/', UserCreateAPIView.as_view(), name='create-user'),
    path('password/', UserUpdatePasswordAPIView.as_view(), name='update-user-password'),
]
