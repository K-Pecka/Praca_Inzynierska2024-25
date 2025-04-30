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
from django.conf.urls.static import static
from django.conf import settings

from . import views


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
    path('user/', include('users.urls')),
    path('user_auth/', include('user_auth.urls')),
    path('trip/<int:trip_pk>/itinerary/', include('itineraries.urls')),
    path('trip/<int:trip_pk>/chat/', include('chats.urls')),
    path('dict/', include('dicts.urls')),
    path('trip/', include('trips.urls')),
    path('apis/', include('apis.urls')),

    path('download/<str:filename>/', views.download_ticket, name='download_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
