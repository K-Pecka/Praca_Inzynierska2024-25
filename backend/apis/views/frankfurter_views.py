import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
        parameters=[
            OpenApiParameter("from", type=str, description="Waluta, z której konwertujemy (np. USD)", required=True),
            OpenApiParameter("to", type=str, description="Waluta, na którą konwertujemy (np. EUR)", required=True),
        ]
    )
class CurrencyRateView(APIView):
    """
    API endpoint to get exchange rates.
    Example: /apis/currency/?from=USD&to=EUR
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        from_curr = request.GET.get("from", "EUR")
        to_curr = request.GET.get("to", "USD")

        try:
            url = f"https://api.frankfurter.app/latest?from={from_curr}&to={to_curr}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            return Response({
                "from": from_curr,
                "to": to_curr,
                "rate": data['rates'][to_curr],
                "date": data['date']
            })

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "Niepławidłowy skrót waluty"}, status=status.HTTP_400_BAD_REQUEST)