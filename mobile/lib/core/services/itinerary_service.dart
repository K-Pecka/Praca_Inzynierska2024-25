import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/activity_model.dart';
import '../models/itinerary_model.dart';
import 'auth_service.dart';

class ItineraryService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<http.Response> _authorizedGet(String endpoint) async {
    final url = Uri.parse('$_baseUrl$endpoint');

    var response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer ${AuthService.accessToken}',
        'accept': 'application/json',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 401) {
      final refreshed = await AuthService.refreshAccessToken();
      if (refreshed) {
        response = await http.get(
          url,
          headers: {
            'Authorization': 'Bearer ${AuthService.accessToken}',
            'accept': 'application/json',
            'Content-Type': 'application/json',
          },
        );
      }
    }

    return response;
  }

  static Future<List<ItineraryModel>> fetchItineraries({
    required int tripId,
  }) async {
    final response = await _authorizedGet('/trip/$tripId/itinerary/all/');

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
      return data.map((json) => ItineraryModel.fromJson(json)).toList();
    } else {
      throw Exception('Nie udało się pobrać planów');
    }
  }

  static Future<List<ActivityModel>> fetchActivities({
    required int tripId,
    required int itineraryId,
  }) async {
    final response = await _authorizedGet(
      '/trip/$tripId/itinerary/$itineraryId/activities/all/',
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
      return data.map((json) => ActivityModel.fromJson(json)).toList();
    } else {
      throw Exception('Nie udało się pobrać aktywności');
    }
  }
}
