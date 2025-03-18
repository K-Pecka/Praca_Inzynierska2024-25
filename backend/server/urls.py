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


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # OpenAPI schema generation endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Redoc UI
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Other
    path('user/', include('users.api_urls')),
    path('user_auth/', include('user_auth.api_urls')),
    path('trip/<int:trip_pk>/itinerary/', include('itineraries.api_urls')),
    path('chat/', include('chats.api_urls')),
    path('trip/', include('trips.api_urls')),
    path('', include('users.urls'), name='confirm_email'),
]
