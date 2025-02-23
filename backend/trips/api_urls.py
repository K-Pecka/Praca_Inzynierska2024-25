from django.urls import path
from .api_views import (
    TripCreateAPIView, TripRetrieveAPIView, TripUpdateAPIView, TripDestroyAPIView, TripListAPIView,
    TicketCreateAPIView, TicketRetrieveAPIView, TicketUpdateAPIView, TicketDestroyAPIView, TicketListAPIView, BudgetUpdateAPIView, BudgetDestroyAPIView,
    ExpenseCreateAPIView, ExpenseRetrieveAPIView, ExpenseUpdateAPIView, ExpenseDestroyAPIView, ExpenseListAPIView
)

urlpatterns = [
    # Trip URLs
    path('create/', TripCreateAPIView.as_view(), name='trip-create'),
    path('<int:pk>/', TripRetrieveAPIView.as_view(), name='trip-retrieve'),
    path('all/', TripListAPIView.as_view(), name='trip-list'),
    path('<int:pk>/update/', TripUpdateAPIView.as_view(), name='trip-update'),
    path('<int:pk>/delete/', TripDestroyAPIView.as_view(), name='trip-delete'),

    # Ticket URLs
    path('ticket/create/', TicketCreateAPIView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/', TicketRetrieveAPIView.as_view(), name='ticket-retrieve'),
    path('ticket/all/', TicketListAPIView.as_view(), name='ticket-list'),
    path('ticket/<int:pk>/update/', TicketUpdateAPIView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDestroyAPIView.as_view(), name='ticket-delete'),

    # Budget URLs
    path('<int:trip_id>/budget/update/', BudgetUpdateAPIView.as_view(), name='budget-update'),
    path('<int:trip_id>/budget/delete/', BudgetDestroyAPIView.as_view(), name='budget-delete'),

    # Expense URLs
    path('<int:trip_id>/expense/create/', ExpenseCreateAPIView.as_view(), name='expense-create'),
    path('<int:trip_id>/expense/<int:pk>/', ExpenseRetrieveAPIView.as_view(), name='expense-retrieve'),
    path('<int:trip_id>/expense/all/', ExpenseListAPIView.as_view(), name='expense-list'),
    path('<int:trip_id>/expense/<int:pk>/update/', ExpenseUpdateAPIView.as_view(), name='expense-update'),
    path('<int:trip_id>/expense/<int:pk>/delete/', ExpenseDestroyAPIView.as_view(), name='expense-delete'),
]
