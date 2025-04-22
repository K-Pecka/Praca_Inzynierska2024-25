import 'dart:convert';
import 'package:http/http.dart' as http;
import '/core/models/itinerary_model.dart';

class ItineraryService {
  Future<List<ItineraryModel>> fetchItineraries({
    required int tripId,
    required String token,
  }) async {
    final url = Uri.parse('https://api.plannder.com/trip/$tripId/itinerary/all/');
    final response = await http.get(
      url,
      headers: {
        'accept': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);
      return data.map((json) => ItineraryModel.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load itineraries');
    }
  }
}