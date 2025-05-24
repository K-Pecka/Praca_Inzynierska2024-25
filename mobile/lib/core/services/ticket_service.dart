import 'dart:convert';
import 'package:mobile/core/utils/http_handler.dart';
import '../models/ticket_model.dart';

class TicketService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<List<TicketModel>> getTicketsByTrip(int tripId) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/ticket/');
    final response = await HttpHandler.request(url);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
      return data.map((e) => TicketModel.fromJson(e)).toList();
    } else {
      throw Exception('Błąd podczas pobierania biletów: ${response.body}');
    }
  }
}