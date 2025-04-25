from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import SystemVariableViewSet

router = DefaultRouter()

router.register(r'system-variables', SystemVariableViewSet, basename='systemvariable')

urlpatterns = router.urls