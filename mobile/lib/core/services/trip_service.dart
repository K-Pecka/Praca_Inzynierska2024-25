import 'dart:convert';
import 'package:mobile/core/utils/http_handler.dart';
import '../models/trip_model.dart';

class TripService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<List<TripModel>> getAllTrips() async {
    final url = Uri.parse('$_baseUrl/trip/');
    final response = await HttpHandler.request(url);

    if (response.statusCode == 200) {
      final Map<String, dynamic> decoded =
      jsonDecode(utf8.decode(response.bodyBytes));

      final List<dynamic> results = decoded['results'];
      return results.map((e) => TripModel.fromJson(e)).toList();
    } else {
      throw Exception('Błąd podczas pobierania wycieczek: ${response.body}');
    }
  }

  static Future<TripModel> getTripById(int tripId) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/');
    final response = await HttpHandler.request(url);

    if (response.statusCode == 200) {
      final data = jsonDecode(utf8.decode(response.bodyBytes));
      return TripModel.fromJson(data);
    } else {
      throw Exception('Błąd podczas pobierania wycieczki o ID $tripId: ${response.body}');
    }
  }
}
