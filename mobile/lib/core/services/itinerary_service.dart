import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:mobile/core/utils/http_handler.dart';
import '../models/activity_model.dart';
import '../models/itinerary_model.dart';

class ItineraryService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<List<ItineraryModel>> fetchItineraries({
    required int tripId,
  }) async {
    final url = Uri.parse('$_baseUrl/trip/$tripId/itinerary/');
    final response = await HttpHandler.request(url);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
      return data.map((json) => ItineraryModel.fromJson(json)).toList();
    } else {
      throw Exception('Nie udało się pobrać planów: ${response.body}');
    }
  }

  static Future<List<ActivityModel>> fetchActivities({
    required int tripId,
    required int itineraryId,
  }) async {
    final url = Uri.parse(
      '$_baseUrl/trip/$tripId/itinerary/$itineraryId/activities/',
    );
    final response = await HttpHandler.request(url);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
      return data.map((json) => ActivityModel.fromJson(json)).toList();
    } else {
      throw Exception('Nie udało się pobrać aktywności: ${response.body}');
    }
  }
}
