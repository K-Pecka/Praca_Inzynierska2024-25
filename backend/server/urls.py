"""
URL configuration for server project.
"""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
'''
Extending schema example
@extend_schema(
    summary="Custom summary for this endpoint",
    description="Detailed description of what this endpoint does",
    responses={200: "Successful response example"}
)
'''

urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI schema generation endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
