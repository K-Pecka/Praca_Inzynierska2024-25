from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from server.permissions import IsTripParticipant, IsExpenseOwnerOrTripCreator
from trips.filters import ExpenseFilter
from trips.models import Expense, ExpenseType, DetailedExpense
from trips.serializers.expense_serializers import ExpenseCreateSerializer, ExpenseRetrieveSerializer, \
    ExpenseListSerializer, ExpenseUpdateSerializer, ExpenseDeleteSerializer, ExpenseTypeListAPIView, \
    DetailedExpenseCreateSerializer, DetailedExpenseRetrieveSerializer, DetailedExpenseListSerializer, \
    DetailedExpenseUpdateSerializer


@extend_schema(tags=['expense'])
class ExpenseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter

    def get_queryset(self):
        return Expense.objects.filter(trip__pk=self.kwargs['trip_pk']) \
                              .select_related('trip', 'user', 'category')

    def get_serializer_class(self):
        if self.action == 'create':
            return ExpenseCreateSerializer
        elif self.action == 'retrieve':
            return ExpenseRetrieveSerializer
        elif self.action == 'list':
            return ExpenseListSerializer
        elif self.action in ['update', 'partial_update']:
            return ExpenseUpdateSerializer
        elif self.action == 'destroy':
            return ExpenseDeleteSerializer
        return ExpenseRetrieveSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list' or self.action == 'retrieve':
            return [IsAuthenticated(), IsTripParticipant()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsExpenseOwnerOrTripCreator()]
        return [IsAuthenticated()]


@extend_schema(tags=['model_type'])
class ExpenseTypeListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseTypeListAPIView

    def get_queryset(self):
        """
        This view should return a list of all the itinerary activity types
        for the currently authenticated user.
        """
        return ExpenseType.objects.all()


@extend_schema(tags=['expense'])
class DetailedExpenseViewSet(ModelViewSet):
    def get_queryset(self):
        trip_pk = self.kwargs.get('trip_pk')
        return DetailedExpense.objects.filter(trip__id=trip_pk)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsTripParticipant()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTripParticipant(), IsExpenseOwnerOrTripCreator()]
        return [IsAuthenticated(), IsTripParticipant()]

    def get_serializer_class(self):
        if self.action == 'create':
            return DetailedExpenseCreateSerializer
        elif self.action == 'retrieve':
            return DetailedExpenseRetrieveSerializer
        elif self.action == 'list':
            return DetailedExpenseListSerializer
        elif self.action in ['update', 'partial_update']:
            return DetailedExpenseUpdateSerializer
        return DetailedExpenseRetrieveSerializer