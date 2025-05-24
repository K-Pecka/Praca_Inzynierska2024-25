from django.urls import path, include
from trips.views.expense_views import DetailedExpenseViewSet, ExpenseViewSet
from trips.views.ticket_views import TicketViewSet
from trips.views.trip_participant_views import JoinTripAPIView, TripParticipantsUpdateAPIView

from rest_framework_nested.routers import NestedDefaultRouter

from rest_framework.routers import DefaultRouter

from trips.views.trip_views import TripViewSet


router = DefaultRouter()
router.register(r'', TripViewSet, basename='trip')

trips_router = NestedDefaultRouter(router, r'trips', lookup='trip')
trips_router.register(r'expenses', ExpenseViewSet, basename='trip-expense')
trips_router.register(r'debt', DetailedExpenseViewSet, basename='detailed-expense')

urlpatterns = [
    # Trip participants URLs
    path('<int:trip_pk>/participants/manage/', TripParticipantsUpdateAPIView.as_view(),
         name='trip-participants-manage-no-account'),
    path('join/', JoinTripAPIView.as_view(), name='trip_join'),

    # Ticket URLs
    path('<int:trip_pk>/ticket/', TicketViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='ticket-list-create'),

    # retrieve + update + delete
    path('<int:trip_pk>/ticket/<int:pk>/', TicketViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='ticket-detail'),

    # all (dla trip creatora)
    path('<int:trip_pk>/ticket/all/', TicketViewSet.as_view({
        'get': 'by_trip'
    }), name='ticket-list-all'),

    # Expense URLs
    path('', include(router.urls)),
    path('', include(trips_router.urls)),
]
