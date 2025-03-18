from rest_framework import serializers

from trips.models import Trip, Currency, Expense
from users.models import UserProfile


class ExpenseSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(required=True, queryset=Trip.objects.all())
    user = serializers.PrimaryKeyRelatedField(required=False, queryset=UserProfile.objects.all())
    currency = serializers.PrimaryKeyRelatedField(required=True, queryset=Currency.objects.all())

    class Meta:
        model = Expense
        fields = [
            'id', 'title', 'amount', 'currency', 'date', 'note', 'trip', 'user', 'category'
        ]
