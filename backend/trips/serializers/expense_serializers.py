import pycountry

from rest_framework import serializers

from trips.models import Trip, Expense, ExpenseType
from users.models import UserProfile


class ExpenseTypeRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'name']


class ExpenseRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    currency = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateField(read_only=True, format="%d.%m.%Y")
    note = serializers.CharField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.full_name', read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Expense
        fields = [
            'title', 'amount', 'currency', 'date', 'note', 'trip', 'user', 'username', 'category'
        ]


class ExpenseListSerializer(serializers.ModelSerializer):
    id  = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    currency = serializers.CharField(read_only=True, max_length=3)
    date = serializers.DateField(read_only=True, format="%d.%m.%Y")
    note = serializers.CharField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    converted_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def get_username(self, obj):
        if obj.user:
            return obj.user.user.full_name
        return None

    class Meta:
        model = Expense
        fields = [
            'id', 'title', 'amount', 'currency', 'date', 'note', 'trip', 'user', 'username', 'category', 'converted_amount'
        ]


class ExpenseCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    date = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y"])
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=ExpenseType.objects.all())

    def validate_date(self, value):
        view = self.context['view']
        trip_pk = view.kwargs.get('trip_pk')
        trip = Trip.objects.get(pk=trip_pk)
        if not trip:
            raise serializers.ValidationError("Nie znaleziono wycieczki o podanym id.")
        if value < trip.start_date or value > trip.end_date:
            raise serializers.ValidationError("Data wydatku musi być w zakresie daty wycieczki.")
        return value

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
    currency = serializers.CharField(write_only=True, default="PLN", max_length=3)
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
