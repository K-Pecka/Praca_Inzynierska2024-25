from django.urls import path
from .api_views import (
    TripCreateAPIView, TripRetrieveAPIView, TripUpdateAPIView, TripDestroyAPIView, TripListAPIView,
    TripActivityCreateAPIView, TripActivityRetrieveAPIView, TripActivityUpdateAPIView, TripActivityDestroyAPIView, TripActivityListAPIView,
    TicketCreateAPIView, TicketRetrieveAPIView, TicketUpdateAPIView, TicketDestroyAPIView, TicketListAPIView,
)

urlpatterns = [
    # Trip URLs
    path('trips/', TripListAPIView.as_view(), name='trip-list'),
    path('trips/create/', TripCreateAPIView.as_view(), name='trip-create'),
    path('trips/<int:pk>/', TripRetrieveAPIView.as_view(), name='trip-retrieve'),
    path('trips/<int:pk>/update/', TripUpdateAPIView.as_view(), name='trip-update'),
    path('trips/<int:pk>/delete/', TripDestroyAPIView.as_view(), name='trip-delete'),

    # TripActivity URLs
    path('activities/', TripActivityListAPIView.as_view(), name='trip-activity-list'),
    path('activities/create/', TripActivityCreateAPIView.as_view(), name='trip-activity-create'),
    path('activities/<int:pk>/', TripActivityRetrieveAPIView.as_view(), name='trip-activity-retrieve'),
    path('activities/<int:pk>/update/', TripActivityUpdateAPIView.as_view(), name='trip-activity-update'),
    path('activities/<int:pk>/delete/', TripActivityDestroyAPIView.as_view(), name='trip-activity-delete'),

    # Ticket URLs
    path('tickets/', TicketListAPIView.as_view(), name='ticket-list'),
    path('tickets/create/', TicketCreateAPIView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/', TicketRetrieveAPIView.as_view(), name='ticket-retrieve'),
    path('tickets/<int:pk>/update/', TicketUpdateAPIView.as_view(), name='ticket-update'),
    path('tickets/<int:pk>/delete/', TicketDestroyAPIView.as_view(), name='ticket-delete'),
]
