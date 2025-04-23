from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from trips.models import Expense
from trips.serializers.expense_serializers import ExpenseCreateSerializer, ExpenseRetrieveSerializer, \
    ExpenseListSerializer, ExpenseUpdateSerializer, ExpenseDeleteSerializer


@extend_schema(tags=['expense'])
class ExpenseCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
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


@extend_schema(tags=['expense'])
class ExpenseDestroyAPIView(DestroyAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseDeleteSerializer
