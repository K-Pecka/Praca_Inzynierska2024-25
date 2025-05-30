from django.urls import path, include

from rest_framework.routers import DefaultRouter

from itineraries.views.itinerary_activity_type_views import ItineraryActivityTypeListAPIView
from itineraries.views.itinerary_activity_views import ItineraryActivityViewSet
from itineraries.views.itinerary_views import ItineraryViewSet


router = DefaultRouter()
router.register(r'', ItineraryViewSet, basename='itinerary')

urlpatterns = [
    # Itineraries
    path('', include(router.urls)),

    # Activities
    path('<int:itinerary_pk>/activities/', ItineraryActivityViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='activity-list-create'),

    path('<int:itinerary_pk>/activities/<int:pk>/', ItineraryActivityViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='activity-detail'),

    # Itinerary activity type
    path('activity-types/', ItineraryActivityTypeListAPIView.as_view(), name='activity-type-list'),
]
