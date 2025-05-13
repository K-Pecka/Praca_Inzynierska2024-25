import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/ticket_model.dart';
import 'auth_service.dart';

class TicketService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<List<TicketModel>> getTicketsByTrip(int tripId) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/ticket/all/');

    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer ${AuthService.accessToken}',
        'accept': 'application/json; charset=utf-8',
      },
    );

    if (response.statusCode == 401) {
      final refreshed = await AuthService.refreshAccessToken();
      if (refreshed) {
        return getTicketsByTrip(tripId);
      } else {
        throw Exception("Nieautoryzowany – token nie działa");
      }
    }

    if (response.statusCode == 200) {
      final List data = jsonDecode(utf8.decode(response.bodyBytes));
      return data.map((e) => TicketModel.fromJson(e)).toList();
    } else {
      throw Exception('Błąd pobierania biletów: ${response.body}');
    }
  }
}