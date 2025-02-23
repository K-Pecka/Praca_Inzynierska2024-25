from django.urls import path
from .api_views import (ItineraryUpdateAPIView, ItineraryListAPIView, ItineraryCreateAPIView, ItineraryDestroyAPIView,
                        ItineraryRetrieveAPIView)
from .api_views import (ItineraryActivityUpdateAPIView, ItineraryActivityListAPIView, ItineraryActivityCreateAPIView,
                        ItineraryActivityDestroyAPIView,
                        ItineraryActivityRetrieveAPIView)

urlpatterns = [
    path('create/', ItineraryCreateAPIView.as_view(), name='itinerary-create'),
    path('<int:pk>/', ItineraryRetrieveAPIView.as_view(), name='itinerary-detail'),
    path('', ItineraryListAPIView.as_view(), name='itinerary-list'),
    path('<int:pk>/update/', ItineraryUpdateAPIView.as_view(), name='itinerary-update'),
    path('<int:pk>/delete/', ItineraryDestroyAPIView.as_view(), name='itinerary-delete'),
    path('<int:itinerary_pk>/activities/all/', ItineraryActivityListAPIView.as_view(), name='activity-list'),
    path('<int:itinerary_pk>/activities/create/', ItineraryActivityCreateAPIView.as_view(), name='activity-create'),
    path('<int:itinerary_pk>/activities/<int:pk>/', ItineraryActivityRetrieveAPIView.as_view(), name='activity-detail'),
    path('<int:itinerary_pk>/activities/<int:pk>/update/', ItineraryActivityUpdateAPIView.as_view(),
         name='activity-update'),
    path('<int:itinerary_pk>/activities/<int:pk>/delete/', ItineraryActivityDestroyAPIView.as_view(),
         name='activity-delete'),
]
