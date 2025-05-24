from django.urls import path, include
from trips.views.expense_views import DetailedExpenseViewSet, ExpenseViewSet
from trips.views.ticket_views import TicketCreateAPIView, TicketRetrieveAPIView, TicketUpdateAPIView, \
    TicketDestroyAPIView, TicketListByTripAPIView
from trips.views.trip_participant_views import JoinTripAPIView, TripParticipantsUpdateAPIView
from trips.views.trip_views import TripCreateAPIView, TripRetrieveAPIView, TripListAPIView, TripUpdateAPIView, \
    TripDestroyAPIView

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='trip-expense')
router.register(r'debt', DetailedExpenseViewSet, basename='detailed-expense')

urlpatterns = [
    # Trip URLs
    path('create/', TripCreateAPIView.as_view(), name='trip-create'),
    path('<int:pk>/', TripRetrieveAPIView.as_view(), name='trip-retrieve'),
    path('all/', TripListAPIView.as_view(), name='trip-list'),
    path('<int:pk>/update/', TripUpdateAPIView.as_view(), name='trip-update'),
    path('<int:pk>/delete/', TripDestroyAPIView.as_view(), name='trip-delete'),

    # Trip participants URLs
    path('<int:trip_pk>/participants/manage/', TripParticipantsUpdateAPIView.as_view(),
         name='trip-participants-manage-no-account'),
    path('join/', JoinTripAPIView.as_view(), name='trip_join'),

    # Ticket URLs
    path('<int:trip_pk>/ticket/create/', TicketCreateAPIView.as_view(), name='ticket-create'),
    path('<int:trip_pk>/ticket/<int:pk>/', TicketRetrieveAPIView.as_view(), name='ticket-retrieve'),
    path('<int:trip_pk>/ticket/<int:pk>/update/', TicketUpdateAPIView.as_view(), name='ticket-update'),
    path('<int:trip_pk>/ticket/<int:pk>/delete/', TicketDestroyAPIView.as_view(), name='ticket-delete'),
    path('<int:trip_pk>/ticket/all/', TicketListByTripAPIView.as_view(), name='ticket-list-by-trip'),

    # Expense URLs
    path('<int:trip_pk>/', include(router.urls)),
]
