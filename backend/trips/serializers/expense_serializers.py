from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import serializers

from trips.models import Trip, Expense, ExpenseType, DetailedExpense
from users.models import UserProfile
from users.serializers.user_profile_serializers import UserProfileListSerializer


class ExpenseTypeRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'name']


class ExpenseTypeListAPIView(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = ExpenseType
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

    def validate(self, data):
        view = self.context['view']
        trip_pk = view.kwargs.get('trip_pk')
        trip = get_object_or_404(Trip, pk=trip_pk)
        if not trip:
            raise serializers.ValidationError("Nie znaleziono wycieczki o podanym id.")

        date = data['date']
        if date < trip.start_date or date > trip.end_date:
            raise serializers.ValidationError("Data wydatku musi być w zakresie daty wycieczki.")

        access_tokens = trip.access_tokens.filter(is_pending=False)
        members = [access_token.user_profile for access_token in access_tokens]
        if data['user'] not in members and data['user'] != trip.creator:
            raise serializers.ValidationError("Użytkownik nie jest uczestnikiem wycieczki.")
        return data

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


class DetailedExpenseCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    members = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), many=True)

    class Meta:
        model = DetailedExpense
        fields = ['name', 'amount', 'currency', 'members']

    def create(self, validated_data):
        request = self.context['request']
        view = self.context['view']
        trip_pk = view.kwargs.get('trip_pk')
        trip = get_object_or_404(Trip, pk=trip_pk)

        members = validated_data.pop('members')

        with transaction.atomic():
            expense = DetailedExpense(**validated_data)
            expense.creator = request.user.get_default_profile()
            expense.trip = trip
            expense.save()

            expense.members.set(members)
            expense.calculate_shares()
            expense.save()

        return expense


class DetailedExpenseRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    currency = serializers.CharField(read_only=True, max_length=3)
    amount_in_pln = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    members = UserProfileListSerializer(many=True, read_only=True)
    amount_per_member = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    amount_per_member_in_pln = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DetailedExpense
        fields = ['name', 'creator', 'amount', 'currency', 'amount_in_pln', 'members', 'amount_per_member',
                  'amount_per_member_in_pln']


class DetailedExpenseListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    currency = serializers.CharField(read_only=True, max_length=3)
    amount_in_pln = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    members = UserProfileListSerializer(many=True, read_only=True)
    amount_per_member = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    amount_per_member_in_pln = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DetailedExpense
        fields = ['id', 'name', 'creator', 'amount', 'currency', 'amount_in_pln', 'members', 'amount_per_member',
                  'amount_per_member_in_pln']


class DetailedExpenseUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    currency = serializers.CharField(max_length=3, required=False)
    amount_in_pln = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    members = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), many=True, required=False)

    class Meta:
        model = DetailedExpense
        fields = ['name', 'amount', 'currency', 'amount_in_pln', 'members']

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if members is not None:
            instance.members.set(members)

        instance.calculate_shares()
        instance.save()
        return instance


class RemoveMemberSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField(
        required=True,
        help_text="ID profilu użytkownika do usunięcia z wydatku"
    )