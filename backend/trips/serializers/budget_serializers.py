from rest_framework import serializers

from trips.models import Budget, Trip


class BudgetBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'amount', 'currency', 'trip']


class BudgetRetrieveSerializer(BudgetBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    currency = serializers.CharField(read_only=True, max_length=64)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class BudgetUpdateSerializer(BudgetBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=64)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class BudgetDestroySerializer(BudgetBaseSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.DecimalField(write_only=True, max_digits=10, decimal_places=2)
    currency = serializers.CharField(write_only=True, max_length=64)
    trip = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Trip.objects.all())
