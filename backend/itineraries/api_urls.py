from django.urls import path
from .api_views import (ItineraryUpdateAPIView, ItineraryListAPIView, ItineraryCreateAPIView, ItineraryDestroyAPIView,
                        ItineraryRetrieveAPIView)
from .api_views import (ItineraryActivityUpdateAPIView, ItineraryActivityListAPIView, ItineraryActivityCreateAPIView,
                        ItineraryActivityDestroyAPIView,
                        ItineraryActivityRetrieveAPIView)

urlpatterns = [
    path('itineraries/', ItineraryListAPIView.as_view(), name='itinerary-list'),
    path('itineraries/create/', ItineraryCreateAPIView.as_view(), name='itinerary-create'),
    path('itineraries/<int:pk>/', ItineraryRetrieveAPIView.as_view(), name='itinerary-detail'),
    path('itineraries/<int:pk>/update/', ItineraryUpdateAPIView.as_view(), name='itinerary-update'),
    path('itineraries/<int:pk>/delete/', ItineraryDestroyAPIView.as_view(), name='itinerary-delete'),
    path('activities/', ItineraryActivityListAPIView.as_view(), name='activity-list'),
    path('activities/create/', ItineraryActivityCreateAPIView.as_view(), name='activity-create'),
    path('activities/<int:pk>/', ItineraryActivityRetrieveAPIView.as_view(), name='activity-detail'),
    path('activities/<int:pk>/update/', ItineraryActivityUpdateAPIView.as_view(), name='activity-update'),
    path('activities/<int:pk>/delete/', ItineraryActivityDestroyAPIView.as_view(), name='activity-delete'),
]
