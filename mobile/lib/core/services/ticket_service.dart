import 'dart:convert';
import 'package:mobile/core/utils/http_handler.dart';
import '../models/ticket_model.dart';

class TicketService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<List<TicketModel>> getTicketsByTrip(int tripId) async {
    List<TicketModel> allTickets = [];
    String? nextUrl = '$_baseUrl/trip/$tripId/ticket/?page=1&page_size=5';

    while (nextUrl != null) {
      final response = await HttpHandler.request(Uri.parse(nextUrl));

      if (response.statusCode == 200) {
        final Map<String, dynamic> decoded = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = decoded['results'];
        allTickets.addAll(results.map((e) => TicketModel.fromJson(e)));

        nextUrl = decoded['next'];
      } else {
        throw Exception('Błąd podczas pobierania biletów: ${response.body}');
      }
    }

    return allTickets;
  }
}