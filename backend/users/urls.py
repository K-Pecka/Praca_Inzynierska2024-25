from django.urls import path

from users.views.user_profile_views import UserProfileListAPIView, UserProfileUpdateAPIView, UserProfileCreateAPIView, \
    ChangeDefaultUserProfileView
from users.views.user_views import UserUpdateAPIView, UserUpdatePasswordAPIView, UserCreateAPIView, ConfirmEmailView, \
    CheckAccessView, CheckAccountTypeAPIView, UserByProfileRetrieveAPIView, UserDeleteAPIView

urlpatterns = [
    # User management
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('password/', UserUpdatePasswordAPIView.as_view(), name='update-user-password'),
    path('profile/', UserProfileListAPIView.as_view(), name='user-profile-list'),
    path('account-type/', CheckAccountTypeAPIView.as_view(), name='user-account-type'),
    path('delete/', UserDeleteAPIView.as_view(), name='user-delete'),

    # User registration process
    path('create/', UserCreateAPIView.as_view(), name='user-register'),
    path('confirm-email/<str:uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('check/<int:user_pk>/permission/<str:perm_code>/action/<str:perm_action>/', CheckAccessView.as_view(), name='check-permission'),

    # User profile management
    path('profile/create/', UserProfileCreateAPIView.as_view(), name='user-profile-create'),
    path('profile/<int:pk>/update/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),

    path('user/by-profile/<str:pk>/', UserByProfileRetrieveAPIView.as_view(), name='user-by-profile'),
    path('profile/<str:role>/change-default/', ChangeDefaultUserProfileView.as_view(), name='change-default-user-profile'),
]
