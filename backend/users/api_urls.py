from django.urls import path
from .api_views import UserCreateView

urlpatterns = [
    path('', UserCreateView.as_view(), name='create-user'),
]
