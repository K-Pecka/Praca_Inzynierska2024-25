import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/trip_model.dart';

class TripService {
  final String baseUrl = 'https://api.plannder.com';

  Future<List<TripModel>> fetchTrips(String token) async {
    final response = await http.get(
      Uri.parse('$baseUrl/trip/all/'),
      headers: {
        'accept': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((e) => TripModel.fromJson(e)).toList();
    } else {
      throw Exception('Błąd podczas pobierania wycieczek');
    }
  }

  Future<TripModel?> fetchTripById(String token, int tripId) async {
    final trips = await fetchTrips(token);
    return trips.firstWhere(
          (trip) => trip.id == tripId,
      orElse: () => trips.isNotEmpty
          ? trips.first
          : TripModel(
        id: -1,
        name: 'Brak',
        creatorId: 0,
        members: [],
        startDate: DateTime.now(),
        endDate: DateTime.now(),
      ),
    );
  }
}
