from rest_framework import serializers

from trips.models import Currency


class CurrencyRetrieveSerializer(serializers.ModelSerializer):
        code = serializers.CharField(read_only=True)

        class Meta:
            model = Currency
            fields = ['id', 'code']