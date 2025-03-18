from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from trips.models import Expense
from trips.serializers.expense_serializers import ExpenseSerializer


@extend_schema(tags=['expense'])
class ExpenseCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer


@extend_schema(tags=['expense'])
class ExpenseRetrieveAPIView(RetrieveAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer


@extend_schema(tags=['expense'])
class ExpenseListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return (Expense.objects
            .filter(trip=self.kwargs['trip_id'])
            .select_related('trip', 'user', 'category','currency')
        )


@extend_schema(tags=['expense'])
class ExpenseUpdateAPIView(UpdateAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer


@extend_schema(tags=['expense'])
class ExpenseDestroyAPIView(DestroyAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
