from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from trips.models import Trip, Budget
from trips.serializers.budget_serializers import BudgetDestroySerializer, BudgetUpdateSerializer


@extend_schema(tags=['budget'])
class BudgetUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetUpdateSerializer

    def get_object(self):
        try:
            trip = Trip.objects.get(id=self.kwargs['trip_id'])
            budget = trip.budgets
            if not budget:
                raise NotFound(detail="Nie znaleziono budżetu dla tego tripu.")
            return budget
        except Trip.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wycieczki o podanym ID.")
        except Budget.DoesNotExist:
            raise NotFound(detail="Nie znaleziono budżetu o podanym ID.")


@extend_schema(tags=['budget'])
class BudgetDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetDestroySerializer

    def get_object(self):
        try:
            trip = Trip.objects.get(id=self.kwargs['trip_id'])
        except Trip.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wycieczki o podanym ID.")

        budget = trip.budgets
        if not budget:
            raise NotFound(detail="Nie znaleziono budżetu dla tej wycieczki.")

        return budget
