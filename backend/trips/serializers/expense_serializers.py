from rest_framework import serializers

from trips.models import Trip, Currency, Expense, ExpenseType
from trips.serializers.currency_serializers import CurrencyRetrieveSerializer
from trips.serializers.trip_serializers import TripRetrieveSerializer
from users.models import UserProfile
from users.serializers.user_serializers import UserRetrieveSerializer


class ExpenseTypeRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'name']


class ExpenseRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    currency = CurrencyRetrieveSerializer(read_only=True)
    date = serializers.DateField(read_only=True, format="%d.%m.%Y")
    note = serializers.CharField(read_only=True)
    trip = TripRetrieveSerializer(read_only=True)
    user = UserRetrieveSerializer(read_only=True)
    category = ExpenseTypeRetrieveSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = [
            'title', 'amount', 'currency', 'date', 'note', 'trip', 'user', 'category'
        ]

class ExpenseListSerializer(serializers.ModelSerializer):
    id  = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    currency = CurrencyRetrieveSerializer(read_only=True)
    date = serializers.DateField(read_only=True, format="%d.%m.%Y")
    note = serializers.CharField(read_only=True)
    trip = TripRetrieveSerializer(read_only=True)
    user = UserRetrieveSerializer(read_only=True)
    category = ExpenseTypeRetrieveSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'title', 'amount', 'currency', 'date', 'note', 'trip', 'user', 'category'
        ]

class ExpenseCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())
    date = serializers.DateField(format="%d.%m.%Y")
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=ExpenseType.objects.all())

    def create(self, validated_data):
        view = self.context['view']
        trip_pk = view.kwargs.get('trip_pk')
        validated_data['trip'] = Trip.objects.get(pk=trip_pk)
        return Expense.objects.create(**validated_data)

    class Meta:
        model = Expense
        fields = [
            'title', 'amount', 'currency', 'date', 'user', 'category'
        ]

class ExpenseUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, write_only=True)
    amount = serializers.DecimalField(required=False, write_only=True, max_digits=10, decimal_places=2)
    currency = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=Currency.objects.all())
    date = serializers.DateField(required=False, write_only=True, format="%d.%m.%Y")
    note = serializers.CharField(required=False, write_only=True)
    category = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=ExpenseType.objects.all())

    class Meta:
        model = Expense
        fields = [
            'title', 'amount', 'currency', 'date', 'note', 'category'
        ]

class ExpenseDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id']