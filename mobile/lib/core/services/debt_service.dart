import 'dart:convert';
import 'package:mobile/core/utils/http_handler.dart';
import '../models/debt_model.dart';

class DebtService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<List<DebtModel>> fetchDebts({required int tripId}) async {
    List<DebtModel> allDebts = [];
    String? nextUrl = '$_baseUrl/trip/$tripId/debt/?page=1&page_size=10';

    while (nextUrl != null) {
      final response = await HttpHandler.request(Uri.parse(nextUrl));

      if (response.statusCode == 200) {
        final Map<String, dynamic> decoded = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = decoded['results'];
        allDebts.addAll(results.map((e) => DebtModel.fromJson(e)));

        nextUrl = decoded['next'];
      } else {
        throw Exception('Błąd podczas pobierania zaległości: ${response.body}');
      }
    }

    return allDebts;
  }

  static Future<void> addDebt({
    required int tripId,
    required String name,
    required String price,
    required String currency,
    required List<int> members,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/debt/');
    final body = jsonEncode({
      'name': name,
      'amount': price,
      'currency': currency,
      'members': members,
    });

    final response = await HttpHandler.request(
      url,
      method: 'POST',
      body: body,
    );

    if (response.statusCode != 201) {
      throw Exception('Błąd podczas dodawania zaległości: ${response.body}');
    }
  }
  static Future<void> removeMemberFromDebt({
    required int tripId,
    required int debtId,
    required int memberId,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/debt/$debtId/remove-member/');
    final body = jsonEncode({'profile_id': memberId});

    final response = await HttpHandler.request(
      url,
      method: 'POST',
      body: body,
    );

    if (response.statusCode != 200) {
      throw Exception('Błąd podczas usuwania dłużnika: ${response.body}');
    }
  }

  static Future<void> deleteDebt({
    required int tripId,
    required int debtId,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/debt/$debtId/');
    final response = await HttpHandler.request(
      url,
      method: 'DELETE',
    );

    if (response.statusCode != 204) {
      throw Exception('Błąd podczas usuwania długu: ${response.body}');
    }
  }

  static Future<DebtModel> getDebtById({
    required int tripId,
    required int debtId,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/debt/$debtId/');
    final response = await HttpHandler.request(url);
    if (response.statusCode == 200) {
      final data = jsonDecode(utf8.decode(response.bodyBytes));
      return DebtModel.fromJson(data);
    } else {
      throw Exception('Błąd podczas pobierania długu: ${response.body}');
    }
  }

}