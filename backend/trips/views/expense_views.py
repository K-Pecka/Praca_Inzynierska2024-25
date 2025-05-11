from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from server.permissions import IsTripParticipant
from trips.models import Expense, ExpenseType
from trips.serializers.expense_serializers import ExpenseCreateSerializer, ExpenseRetrieveSerializer, \
    ExpenseListSerializer, ExpenseUpdateSerializer, ExpenseDeleteSerializer


@extend_schema(tags=['expense'])
class ExpenseCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ExpenseCreateSerializer


@extend_schema(tags=['expense'])
class ExpenseRetrieveAPIView(RetrieveAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseRetrieveSerializer


@extend_schema(tags=['expense'])
class ExpenseListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseListSerializer

    def get_queryset(self):
        return (Expense.objects
                .filter(trip=self.kwargs['trip_pk'])
                .select_related('trip', 'user', 'category')
                )


@extend_schema(tags=['expense'])
class ExpenseUpdateAPIView(UpdateAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseUpdateSerializer


@method_decorator(csrf_exempt, name='dispatch')
@extend_schema(tags=['expense'])
class ExpenseDestroyAPIView(DestroyAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseDeleteSerializer


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

