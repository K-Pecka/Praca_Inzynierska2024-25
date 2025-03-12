from django.urls import path
from .api_views import UserCreateAPIView, UserUpdateAPIView, UserUpdatePasswordAPIView, UserProfileListAPIView

urlpatterns = [
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('create/', UserCreateAPIView.as_view(), name='user-register'),
    path('password/', UserUpdatePasswordAPIView.as_view(), name='update-user-password'),
    path('profile/', UserProfileListAPIView.as_view(), name='user-profile-list'),
]
