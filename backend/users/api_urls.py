from django.urls import path
from .api_views import UserCreateAPIView, UserUpdateAPIView

urlpatterns = [
    path('', UserCreateAPIView.as_view(), name='create-user'),
    path('<int:id>/', UserUpdateAPIView.as_view(), name='update-user'),
]
