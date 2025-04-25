import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/expense_model.dart';

class BudgetService {
  final String baseUrl = 'https://api.plannder.com';

  Future<List<ExpenseModel>> fetchExpenses({
    required int tripId,
    required String token,
  }) async {
    final response = await http.get(
      Uri.parse('$baseUrl/trip/$tripId/expense/all/'),
      headers: {
        'accept': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
      return data.map((e) => ExpenseModel.fromJson(e)).toList();
    } else {
      throw Exception('Błąd podczas pobierania wydatków');
    }
  }

  Future<void> addExpense({
    required String token,
    required int tripId,
    required int userProfileId,
    required String title,
    required double amount,
    required String date,
    required String note,
  }) async {
    final url = Uri.parse('$baseUrl/trip/$tripId/expense/create/');

    final headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };

    final body = jsonEncode({
      'title': title,
      'amount': amount.toStringAsFixed(2),
      'currency': "USD",
      'date': date,
      'note': note,
      'trip': tripId,
      'user': userProfileId,
      'category': 1,
    });

    final response = await http.post(url, headers: headers, body: body);

    if (response.statusCode != 201) {
      throw Exception('Błąd podczas dodawania wydatku: ${response.body}');
    }
  }

  Future<double> getExchangeRate({
    required String from,
    required String to,
    required String token,
  }) async {
    final url = Uri.parse('$baseUrl/apis/currency/?from=$from&to=$to');
    final response = await http.get(
      url,
      headers: {
        'accept': '*/*',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final json = jsonDecode(response.body);
      return double.parse(json['rate'].toString());
    } else {
      throw Exception('Błąd pobierania kursu: ${response.body}');
    }
  }
}

