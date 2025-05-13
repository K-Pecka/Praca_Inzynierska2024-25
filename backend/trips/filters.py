import django_filters
from trips.models import Trip

class TripFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    start_date_after = django_filters.DateFilter(field_name="start_date", lookup_expr="gte")
    start_date_before = django_filters.DateFilter(field_name="start_date", lookup_expr="lte")

    end_date_after = django_filters.DateFilter(field_name="end_date", lookup_expr="gte")
    end_date_before = django_filters.DateFilter(field_name="end_date", lookup_expr="lte")

    is_creator = django_filters.BooleanFilter(method="filter_is_creator")

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
