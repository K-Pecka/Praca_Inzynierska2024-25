import requests

from django.http import JsonResponse


def currency_rate(request):
    """
    API endpoint to get exchange rates.
    Example: /apis/currency/?from=USD&to=EUR
    """
    from_curr = request.GET.get("from", "EUR")
    to_curr = request.GET.get("to", "USD")

    try:
        url = f"https://api.frankfurter.app/latest?from={from_curr}&to={to_curr}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return JsonResponse({
            "from": from_curr,
            "to": to_curr,
            "rate": data['rates'][to_curr],
            "date": data['date']
        })

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)
    except KeyError:
        return JsonResponse({"error": "Niepławidłowy skrót waluty"}, status=400)