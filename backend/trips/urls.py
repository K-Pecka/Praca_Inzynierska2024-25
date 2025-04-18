from django.urls import path

from trips.views.budget_views import BudgetUpdateAPIView, BudgetDestroyAPIView
from trips.views.expense_views import ExpenseCreateAPIView, ExpenseRetrieveAPIView, ExpenseListAPIView, \
    ExpenseUpdateAPIView, ExpenseDestroyAPIView
from trips.views.ticket_views import TicketCreateAPIView, TicketRetrieveAPIView, TicketListAPIView, TicketUpdateAPIView, \
    TicketDestroyAPIView
from trips.views.trip_participant_views import JoinTripAPIView, TripParticipantsUpdateAPIView
from trips.views.trip_views import TripCreateAPIView, TripRetrieveAPIView, TripListAPIView, TripUpdateAPIView, \
    TripDestroyAPIView


urlpatterns = [
    # Trip URLs
    path('create/', TripCreateAPIView.as_view(), name='trip-create'),
    path('<int:pk>/', TripRetrieveAPIView.as_view(), name='trip-retrieve'),
    path('all/', TripListAPIView.as_view(), name='trip-list'),
    path('<int:pk>/update/', TripUpdateAPIView.as_view(), name='trip-update'),
    path('<int:pk>/delete/', TripDestroyAPIView.as_view(), name='trip-delete'),

    # Trip participants URLs
    path('<int:trip_pk>/participants/manage/', TripParticipantsUpdateAPIView.as_view(), name='trip-participants-manage-no-account'),
    path('join/', JoinTripAPIView.as_view(), name='trip_join'),

    # Ticket URLs
    path('ticket/create/', TicketCreateAPIView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/', TicketRetrieveAPIView.as_view(), name='ticket-retrieve'),
    path('ticket/all/', TicketListAPIView.as_view(), name='ticket-list'),
    path('ticket/<int:pk>/update/', TicketUpdateAPIView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDestroyAPIView.as_view(), name='ticket-delete'),

    # Budget URLs
    path('<int:trip_pk>/budget/update/', BudgetUpdateAPIView.as_view(), name='budget-update'),
    path('<int:trip_pk>/budget/delete/', BudgetDestroyAPIView.as_view(), name='budget-delete'),

    # Expense URLs
    path('<int:trip_pk>/expense/create/', ExpenseCreateAPIView.as_view(), name='expense-create'),
    path('<int:trip_pk>/expense/<int:pk>/', ExpenseRetrieveAPIView.as_view(), name='expense-retrieve'),
    path('<int:trip_pk>/expense/all/', ExpenseListAPIView.as_view(), name='expense-list'),
    path('<int:trip_pk>/expense/<int:pk>/update/', ExpenseUpdateAPIView.as_view(), name='expense-update'),
    path('<int:trip_pk>/expense/<int:pk>/delete/', ExpenseDestroyAPIView.as_view(), name='expense-delete'),
]

