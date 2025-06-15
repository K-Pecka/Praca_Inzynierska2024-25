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
    List<ItineraryModel> allItineraries = [];
    String? nextUrl = '$_baseUrl/trip/$tripId/itinerary/?page=1&page_size=10';

    while (nextUrl != null) {
      final response = await HttpHandler.request(Uri.parse(nextUrl));

      if (response.statusCode == 200) {
        final Map<String, dynamic> decoded = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = decoded['results'];
        allItineraries.addAll(results.map((json) => ItineraryModel.fromJson(json)));

        nextUrl = decoded['next'];
      } else {
        throw Exception('Nie udało się pobrać planów: ${response.body}');
      }
    }

    return allItineraries;
  }

  static Future<List<ActivityModel>> fetchActivities({
    required int tripId,
    required int itineraryId,
  }) async {
    List<ActivityModel> allActivities = [];
    String? nextUrl = '$_baseUrl/trip/$tripId/itinerary/$itineraryId/activities/';

    while (nextUrl != null) {
      final response = await HttpHandler.request(Uri.parse(nextUrl));

      if (response.statusCode == 200) {
        final Map<String, dynamic> decoded = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = decoded['results'];
        allActivities.addAll(results.map((json) => ActivityModel.fromJson(json)));

        nextUrl = decoded['next'];
      } else {
        throw Exception('Nie udało się pobrać aktywności: ${response.body}');
      }
    }

    return allActivities;
  }
}
