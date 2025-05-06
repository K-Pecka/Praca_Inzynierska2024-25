from django.urls import path

from itineraries.views.itinerary_activity_type_views import ItineraryActivityTypeListAPIView
from itineraries.views.itinerary_activity_views import ItineraryActivityListAPIView, ItineraryActivityCreateAPIView, \
    ItineraryActivityRetrieveAPIView, ItineraryActivityUpdateAPIView, ItineraryActivityDestroyAPIView
from itineraries.views.itinerary_views import ItineraryListAPIView, ItineraryCreateAPIView, ItineraryRetrieveAPIView, \
    ItineraryUpdateAPIView, ItineraryDestroyAPIView

urlpatterns = [
    # Itineraries
    path('all/', ItineraryListAPIView.as_view(), name='itinerary-list'),
    path('<int:pk>/', ItineraryRetrieveAPIView.as_view(), name='itinerary-detail'),
    path('create/', ItineraryCreateAPIView.as_view(), name='itinerary-create'),
    path('<int:pk>/update/', ItineraryUpdateAPIView.as_view(), name='itinerary-update'),
    path('<int:pk>/delete/', ItineraryDestroyAPIView.as_view(), name='itinerary-delete'),

    # Itinerary activity
    path('<int:itinerary_pk>/activities/all/', ItineraryActivityListAPIView.as_view(), name='activity-list'),
    path('<int:itinerary_pk>/activities/<int:pk>/', ItineraryActivityRetrieveAPIView.as_view(), name='activity-detail'),
    path('<int:itinerary_pk>/activities/create/', ItineraryActivityCreateAPIView.as_view(), name='activity-create'),
    path('<int:itinerary_pk>/activities/<int:pk>/update/', ItineraryActivityUpdateAPIView.as_view(),
         name='activity-update'),
    path('<int:itinerary_pk>/activities/<int:pk>/delete/', ItineraryActivityDestroyAPIView.as_view(),
         name='activity-delete'),

    # Itinerary activity type
    path('activity-types/all/', ItineraryActivityTypeListAPIView.as_view(), name='activity-type-list'),
]
