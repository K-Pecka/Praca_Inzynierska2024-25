from django.urls import path
from .views import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify"),
]
