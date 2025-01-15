from django.urls import path
from .api_views import ItineraryUpdateAPIView, ItineraryListAPIView, ItineraryCreateAPIView, ItineraryDestroyAPIView, \
    ItineraryRetrieveAPIView

urlpatterns = [
    path('itineraries/', ItineraryListAPIView.as_view(), name='itinerary-list'),
    path('itineraries/create/', ItineraryCreateAPIView.as_view(), name='itinerary-create'),
    path('itineraries/<int:pk>/', ItineraryRetrieveAPIView.as_view(), name='itinerary-detail'),
    path('itineraries/<int:pk>/update/', ItineraryUpdateAPIView.as_view(), name='itinerary-update'),
    path('itineraries/<int:pk>/delete/', ItineraryDestroyAPIView.as_view(), name='itinerary-delete'),
]
