import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/expense_model.dart';
import 'auth_service.dart';

class BudgetService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<http.Response> _authorizedRequest(
      Uri url, {
        String method = 'GET',
        Map<String, String>? headers,
        dynamic body,
      }) async {
    headers ??= {};
    headers['Authorization'] = 'Bearer ${AuthService.accessToken}';
    headers['accept'] ??= 'application/json';
    if (method == 'POST') headers['Content-Type'] = 'application/json';

    late http.Response response;

    if (method == 'GET') {
      response = await http.get(url, headers: headers);
    } else if (method == 'POST') {
      response = await http.post(url, headers: headers, body: body);
    }

    if (response.statusCode == 401) {
      final refreshed = await AuthService.refreshAccessToken();
      if (refreshed) {
        headers['Authorization'] = 'Bearer ${AuthService.accessToken}';
        if (method == 'GET') {
          response = await http.get(url, headers: headers);
        } else if (method == 'POST') {
          response = await http.post(url, headers: headers, body: body);
        }
      }
    }

    return response;
  }

  static Future<List<ExpenseModel>> fetchExpenses({
    required int tripId,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/expense/all/');
    final response = await _authorizedRequest(url);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
      return data.map((e) => ExpenseModel.fromJson(e)).toList();
    } else {
      throw Exception('Błąd podczas pobierania wydatków: ${response.body}');
    }
  }

  static Future<void> addExpense({
    required int tripId,
    required int userProfileId,
    required String title,
    required double amount,
    required String date,
    required String note,
    required String currency,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/expense/create/');
    final body = jsonEncode({
      'title': title,
      'amount': amount.toStringAsFixed(2),
      'currency': currency,
      'date': date,
      'note': note,
      'trip': tripId,
      'user': userProfileId,
      'category': 1,
    });

    final response = await _authorizedRequest(
      url,
      method: 'POST',
      body: body,
    );

    if (response.statusCode != 201) {
      throw Exception('Błąd podczas dodawania wydatku: ${response.body}');
    }
  }

  static Future<double> getExchangeRate({
    required String from,
    required String to,
  }) async {
    final url = Uri.parse('$_baseUrl/apis/currency/?from=$from&to=$to');
    final response = await _authorizedRequest(url);

    if (response.statusCode == 200) {
      final json = jsonDecode(response.body);
      return double.parse(json['rate'].toString());
    } else {
      throw Exception('Błąd pobierania kursu: ${response.body}');
    }
  }

  static Future<void> deleteExpense({
    required int tripId,
    required int expenseId,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/expense/$expenseId/delete/');
    final headers = {
      'Authorization': 'Bearer ${AuthService.accessToken}',
      'accept': 'application/json',
    };

    final response = await http.delete(url, headers: headers);

    if (response.statusCode != 204) {
      throw Exception('Nie udało się usunąć wydatku: ${response.body}');
    }
  }

}

