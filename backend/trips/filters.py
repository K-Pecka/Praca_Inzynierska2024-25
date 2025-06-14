from django_filters import rest_framework as filters
from trips.models import Expense, Trip, ExpenseType, DetailedExpense
from users.models import UserProfile


class TripFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    start_date_after = filters.DateFilter(field_name="start_date", lookup_expr="gte")
    start_date_before = filters.DateFilter(field_name="start_date", lookup_expr="lte")

    end_date_after = filters.DateFilter(field_name="end_date", lookup_expr="gte")
    end_date_before = filters.DateFilter(field_name="end_date", lookup_expr="lte")

    is_creator = filters.BooleanFilter(method="filter_is_creator")


    class Meta:
        model = Trip
        fields = [
            "name", "start_date_after", "start_date_before", "end_date_after", "end_date_before",
            "is_creator",
        ]

    def filter_is_creator(self, queryset, name, value):
        profile = self.request.user.get_default_profile()
        if value:
            return queryset.filter(creator=profile)
        return queryset.exclude(creator=profile)


class ExpenseFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains', label="Tytuł")
    amount_min = filters.NumberFilter(field_name="amount", lookup_expr='gte', label="Kwota od")
    amount_max = filters.NumberFilter(field_name="amount", lookup_expr='lte', label="Kwota do")
    currency = filters.CharFilter(field_name="currency", label="Waluta")
    date = filters.DateFilter(field_name="date", label="Dokładna data")
    date_from = filters.DateFilter(field_name="date", lookup_expr='gte', label="Data od")
    date_to = filters.DateFilter(field_name="date", lookup_expr='lte', label="Data do")
    trip = filters.ModelChoiceFilter(queryset=Trip.objects.all(), label="Wycieczka")
    user = filters.ModelChoiceFilter(queryset=UserProfile.objects.all(), label="Użytkownik")
    category = filters.ModelChoiceFilter(queryset=ExpenseType.objects.all(), label="Kategoria")

    class Meta:
        model = Expense
        fields = [
            "title",
            "amount_min",
            "amount_max",
            "currency",
            "date",
            "date_from",
            "date_to",
            "trip",
            "user",
            "category"
        ]

class DetailedExpenseFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', label="Nazwa")
    creator = filters.NumberFilter(field_name='creator', label="Twórca")

    amount_from = filters.NumberFilter(field_name="amount", lookup_expr='gte', label="Kwota od")
    amount_to = filters.NumberFilter(field_name="amount", lookup_expr='lte', label="Kwota do")

    amount_in_pln_from = filters.NumberFilter(field_name="amount_in_pln", lookup_expr='gte', label="Kwota PLN od")
    amount_in_pln_to = filters.NumberFilter(field_name="amount_in_pln", lookup_expr='lte', label="Kwota PLN do")

    amount_per_member_from = filters.NumberFilter(field_name="amount_per_member", lookup_expr='gte', label="Na osobę od")
    amount_per_member_to = filters.NumberFilter(field_name="amount_per_member", lookup_expr='lte', label="Na osobę do")

    amount_per_member_in_pln_from = filters.NumberFilter(field_name="amount_per_member_in_pln", lookup_expr='gte', label="Na osobę PLN od")
    amount_per_member_in_pln_to = filters.NumberFilter(field_name="amount_per_member_in_pln", lookup_expr='lte', label="Na osobę PLN do")

    currency = filters.CharFilter(field_name="currency", label="Waluta")
    trip = filters.ModelChoiceFilter(queryset=Trip.objects.all(), label="Wycieczka")
    user = filters.ModelChoiceFilter(queryset=UserProfile.objects.all(), label="Użytkownik")
    members = filters.ModelChoiceFilter(queryset=UserProfile.objects.all(), label="Uczestnicy")

    class Meta:
        model = DetailedExpense
        fields = [
            "name",
            "creator",
            "amount_from",
            "amount_to",
            "amount_in_pln_from",
            "amount_in_pln_to",
            "amount_per_member_from",
            "amount_per_member_to",
            "amount_per_member_in_pln_from",
            "amount_per_member_in_pln_to",
            "currency",
            "trip",
            "user",
            "members"
        ]

