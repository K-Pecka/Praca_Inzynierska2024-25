from drf_spectacular.utils import extend_schema, OpenApiExample
from requests.models import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError

from server.permissions import IsTripParticipant, IsExpenseOwnerOrTripCreator
from trips.filters import ExpenseFilter
from trips.models import Expense, ExpenseType, DetailedExpense
from trips.serializers.expense_serializers import ExpenseCreateSerializer, ExpenseRetrieveSerializer, \
    ExpenseListSerializer, ExpenseUpdateSerializer, ExpenseDeleteSerializer, ExpenseTypeListAPIView, \
    DetailedExpenseCreateSerializer, DetailedExpenseRetrieveSerializer, DetailedExpenseListSerializer, \
    DetailedExpenseUpdateSerializer, RemoveMemberSerializer


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

    def get_object(self):
        trip_pk = self.kwargs.get('trip_pk')
        pk = self.kwargs.get('pk')
        return DetailedExpense.objects.filter(trip__id=trip_pk, pk=pk).first()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsTripParticipant()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsExpenseOwnerOrTripCreator()]
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

    @extend_schema(
        request=RemoveMemberSerializer,
        responses={200: OpenApiExample('Sukces', value={"detail": "Użytkownik usunięty z wydatku"})},
        tags=["expense"]
    )
    @action(detail=True, methods=['post'], url_path='remove-member', permission_classes=[IsAuthenticated, IsTripParticipant])
    def remove_member(self, request, trip_pk=None, pk=None):
        user_profile = request.data.get('profile_id')
        if not user_profile:
            return ValidationError("Nie podano profilu użytkownika")

        expense = self.get_object()
        if not expense:
            return ValidationError("Wydatek o podanym id nie istnieje")

        member_to_remove = expense.members.filter(id=user_profile).first()
        if not member_to_remove:
            return ValidationError("Wybrany użytkownik nie znajduje się na liście do spłaty długu lub nie istnieje")

        expense.amount -= expense.amount_per_member

        expense.members.remove(member_to_remove)

        expense.calculate_shares()
        expense.save()

        return expense