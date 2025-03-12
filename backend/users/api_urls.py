from django.urls import path
from .api_views import UserCreateAPIView, UserUpdateAPIView, UserUpdatePasswordAPIView

urlpatterns = [
    # path('', UserListAPIView.as_view(), name='user-list'),
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('create/', UserCreateAPIView.as_view(), name='user-register'),
    path('password/', UserUpdatePasswordAPIView.as_view(), name='update-user-password'),
]
