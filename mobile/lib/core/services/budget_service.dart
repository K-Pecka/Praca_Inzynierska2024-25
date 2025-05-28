import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:mobile/core/utils/http_handler.dart';
import '../models/expense_model.dart';

class BudgetService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<List<ExpenseModel>> fetchExpenses({
    required int tripId,
  }) async {
    List<ExpenseModel> allExpenses = [];
    String? nextUrl = '$_baseUrl/trip/$tripId/expenses/';

    while (nextUrl != null) {
      final response = await HttpHandler.request(Uri.parse(nextUrl));

      if (response.statusCode == 200) {
        final Map<String, dynamic> decoded = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = decoded['results'];
        allExpenses.addAll(results.map((e) => ExpenseModel.fromJson(e)));
        nextUrl = decoded['next'];
      } else {
        throw Exception('Błąd podczas pobierania wydatków: ${response.body}');
      }
    }

    return allExpenses;
  }

  static Future<void> addExpense({
    required int tripId,
    required int userProfileId,
    required String title,
    required double amount,
    required String date,
    required String note,
    required String currency,
    required String category,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/expenses/');
    final body = jsonEncode({
      'title': title,
      'amount': amount.toStringAsFixed(2),
      'currency': currency,
      'date': date,
      'note': note,
      'trip': tripId,
      'user': userProfileId,
      'category': category,
    });

    final response = await HttpHandler.request(
      url,
      method: 'POST',
      body: body,
    );

    if (response.statusCode != 201) {
      throw Exception('Błąd podczas dodawania wydatku: ${response.body}');
    }
  }

  static Future<void> updateExpense({
    required int tripId,
    required int expenseId,
    required Map<String, dynamic> updates,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/expenses/$expenseId/');
    final body = jsonEncode(updates);

    final response = await HttpHandler.request(
      url,
      method: 'PUT',
      body: body,
    );

    if (response.statusCode != 200) {
      throw Exception('Nie udało się zaktualizować wydatku: ${response.body}');
    }
  }

  static Future<void> deleteExpense({
    required int tripId,
    required int expenseId,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/expenses/$expenseId/');
    final response = await HttpHandler.request(
      url,
      method: 'DELETE',
    );

    if (response.statusCode != 204) {
      throw Exception('Nie udało się usunąć wydatku: ${response.body}');
    }
  }
}

