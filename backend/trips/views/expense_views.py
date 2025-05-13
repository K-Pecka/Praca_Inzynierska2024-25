from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters

from server.permissions import IsTripParticipant, IsExpenseOwnerOrTripCreator
from trips.filters import ExpenseFilter
from trips.models import Expense, ExpenseType
from trips.serializers.expense_serializers import ExpenseCreateSerializer, ExpenseRetrieveSerializer, \
    ExpenseListSerializer, ExpenseUpdateSerializer, ExpenseDeleteSerializer, ExpenseTypeListAPIView


@extend_schema(tags=['expense'])
class ExpenseCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ExpenseCreateSerializer


@extend_schema(tags=['expense'])
class ExpenseRetrieveAPIView(RetrieveAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseRetrieveSerializer


@extend_schema(
    tags=['expense'],
    filters=True,
    parameters=[
        OpenApiParameter(name="title", type=OpenApiTypes.STR, location='query',
                         description="Tytuł (zawiera)"),
        OpenApiParameter(name="amount_min", type=OpenApiTypes.NUMBER, location='query',
                         description="Kwota od"),
        OpenApiParameter(name="amount_max", type=OpenApiTypes.NUMBER, location='query',
                         description="Kwota do"),
        OpenApiParameter(name="currency", type=OpenApiTypes.STR, location='query', description="Waluta"),
        OpenApiParameter(name="date", type=OpenApiTypes.DATE, location='query',
                         description="Dokładna data"),
        OpenApiParameter(name="date_from", type=OpenApiTypes.DATE, location='query',
                         description="Data od"),
        OpenApiParameter(name="date_to", type=OpenApiTypes.DATE, location='query',
                         description="Data do"),
    ]
)
class ExpenseListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ExpenseFilter

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
    permission_classes = [IsAuthenticated, IsExpenseOwnerOrTripCreator]
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

