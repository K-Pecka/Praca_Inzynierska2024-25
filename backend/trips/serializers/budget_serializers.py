from pycountry import currencies

from rest_framework import serializers

from trips.models import Budget, Trip, Currency


class BudgetBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'amount', 'currency', 'trip']


class BudgetRetrieveSerializer(BudgetBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    currency = serializers.CharField(read_only=True, max_length=3)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class BudgetUpdateSerializer(BudgetBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_currency(self, value):
        if not currencies.get(alpha_3=value):
            available = [c.alpha_3 for c in currencies]
            raise serializers.ValidationError(
                f"Nieprawidłowy kod waluty. Dostepne: {', '.join(available)}"
            )
        return value


class BudgetDestroySerializer(BudgetBaseSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.DecimalField(write_only=True, max_digits=10, decimal_places=2)
    currency = serializers.CharField(write_only=True, max_length=3)
    trip = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Trip.objects.all())
