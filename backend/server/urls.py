"""
URL configuration for server project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from users.views import confirm_email

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
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('user_auth/', include('user_auth.api_urls')),
    path('user/', include('users.api_urls')),
    path('trip/<int:trip_pk>/itinerary/', include('itineraries.api_urls')),
    path('chat/', include('chats.api_urls')),
    path('trip/', include('trips.api_urls')),
    path('', confirm_email, name='confirm_email'),
]
