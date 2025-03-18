from django.urls import path
from .api_views import UserCreateAPIView, UserUpdateAPIView, UserUpdatePasswordAPIView, UserProfileListAPIView, \
    CheckAccessView, ConfirmEmailView

urlpatterns = [
    # User management
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('password/', UserUpdatePasswordAPIView.as_view(), name='update-user-password'),
    path('profile/', UserProfileListAPIView.as_view(), name='user-profile-list'),

    # User registration process
    path('create/', UserCreateAPIView.as_view(), name='user-register'),
    path('confirm-email/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('check/<user_pk>/permission/<perm_code>/action/<perm_action>/', CheckAccessView.as_view(), name='check-permission'),
]
