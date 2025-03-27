from django.urls import path

from users.views.user_profile_views import UserProfileListAPIView
from users.views.user_views import UserUpdateAPIView, UserUpdatePasswordAPIView, UserCreateAPIView, ConfirmEmailView, \
    CheckAccessView

urlpatterns = [
    # User management
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('password/', UserUpdatePasswordAPIView.as_view(), name='update-user-password'),
    path('profile/', UserProfileListAPIView.as_view(), name='user-profile-list'),

    # User registration process
    path('create/', UserCreateAPIView.as_view(), name='user-register'),
    path('confirm-email/<str:uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('check/<int:user_pk>/permission/<str:perm_code>/action/<str:perm_action>/', CheckAccessView.as_view(), name='check-permission'),
]
