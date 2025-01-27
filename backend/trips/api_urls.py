from django.urls import path
from .api_views import (
    TripCreateAPIView, TripRetrieveAPIView, TripUpdateAPIView, TripDestroyAPIView, TripListAPIView,
    TripActivityCreateAPIView, TripActivityRetrieveAPIView, TripActivityUpdateAPIView, TripActivityDestroyAPIView,
    TripActivityListAPIView,
    TicketCreateAPIView, TicketRetrieveAPIView, TicketUpdateAPIView, TicketDestroyAPIView, TicketListAPIView,
    BudgetCreateAPIView, BudgetRetrieveAPIView, BudgetUpdateAPIView, BudgetDestroyAPIView, BudgetListAPIView,
    ExpenseCreateAPIView, ExpenseRetrieveAPIView, ExpenseUpdateAPIView, ExpenseDestroyAPIView, ExpenseListAPIView
)

urlpatterns = [
    # Trip URLs
    path('', TripCreateAPIView.as_view(), name='trip-create'),
    path('<int:pk>/', TripRetrieveAPIView.as_view(), name='trip-retrieve'),
    path('all/', TripListAPIView.as_view(), name='trip-list'),
    path('<int:pk>/update/', TripUpdateAPIView.as_view(), name='trip-update'),
    path('<int:pk>/delete/', TripDestroyAPIView.as_view(), name='trip-delete'),

    # TripActivity URLs
    path('<int:trip_id>/activity/', TripActivityCreateAPIView.as_view(), name='trip-activity-create'),
    path('<int:trip_id>/activity/<int:pk>/', TripActivityRetrieveAPIView.as_view(), name='trip-activity-retrieve'),
    path('<int:trip_id>/activity/all/', TripActivityListAPIView.as_view(), name='trip-activity-list'),
    path('<int:trip_id>/activity/<int:pk>/update/', TripActivityUpdateAPIView.as_view(), name='trip-activity-update'),
    path('<int:trip_id>/activity/<int:pk>/delete/', TripActivityDestroyAPIView.as_view(), name='trip-activity-delete'),

    # Ticket URLs
    path('ticket/', TicketCreateAPIView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/', TicketRetrieveAPIView.as_view(), name='ticket-retrieve'),
    path('ticket/all/', TicketListAPIView.as_view(), name='ticket-list'),
    path('ticket/<int:pk>/update/', TicketUpdateAPIView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDestroyAPIView.as_view(), name='ticket-delete'),

    # Budget URLs
    path('<int:trip_id>/budget/', BudgetCreateAPIView.as_view(), name='budget-create'),
    path('<int:trip_id>/budget/<int:pk>/', BudgetRetrieveAPIView.as_view(), name='budget-retrieve'),
    path('<int:trip_id>/budget/all/', BudgetListAPIView.as_view(), name='budget-list'),
    path('<int:trip_id>/budget/<int:pk>/update/', BudgetUpdateAPIView.as_view(), name='budget-update'),
    path('<int:trip_id>/budget/<int:pk>/delete/', BudgetDestroyAPIView.as_view(), name='budget-delete'),

    # Expense URLs
    path('<int:trip_id>/expense/', ExpenseCreateAPIView.as_view(), name='expense-create'),
    path('<int:trip_id>/expense/<int:pk>/', ExpenseRetrieveAPIView.as_view(), name='expense-retrieve'),
    path('<int:trip_id>/expense/all/', ExpenseListAPIView.as_view(), name='expense-list'),
    path('<int:trip_id>/expense/<int:pk>/update/', ExpenseUpdateAPIView.as_view(), name='expense-update'),
    path('<int:trip_id>/expense/<int:pk>/delete/', ExpenseDestroyAPIView.as_view(), name='expense-delete'),
]
