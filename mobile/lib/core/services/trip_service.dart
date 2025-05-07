import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/trip_model.dart';
import 'auth_service.dart';

class TripService {
  static final String _baseUrl = 'https://api.plannder.com';

  static Future<http.Response> _authorizedGet(String endpoint) async {
    final url = Uri.parse('$_baseUrl$endpoint');

    var response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer ${AuthService.accessToken}',
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
    );

    if (response.statusCode == 401) {
      final refreshed = await AuthService.refreshAccessToken();
      if (refreshed) {
        response = await http.get(
          url,
          headers: {
            'Authorization': 'Bearer ${AuthService.accessToken}',
            'Content-Type': 'application/json',
            'accept': 'application/json',
          },
        );
      }
    }

    return response;
  }

  static Future<List<TripModel>> getAllTrips() async {
    final response = await _authorizedGet('/trip/all/');

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      final trips = data.map((e) => TripModel.fromJson(e)).toList();

      for (final trip in trips) {
        for (int i = 0; i < trip.members.length; i++) {
          final member = trip.members[i];
          try {
            final enriched = await _fetchUserInfoByProfileId(member.id);
            trip.members[i] = member.copyWith(
              email: enriched.email,
              firstName: enriched.firstName,
              lastName: enriched.lastName,
            );
          } catch (e) {
          }
        }
      }

      return trips;
    } else {
      throw Exception('Błąd podczas pobierania wycieczek');
    }
  }

  static Future<TripModel?> getTripById(int tripId) async {
    final trips = await getAllTrips();

    return trips.firstWhere(
          (trip) => trip.id == tripId,
      orElse: () => trips.isNotEmpty
          ? trips.first
          : TripModel(
        id: -1,
        name: 'Brak',
        creator: Member(id: 0, email: 'brak@brak.pl'),
        members: [],
        startDate: DateTime.now(),
        endDate: DateTime.now(),
        isCreator: false,
      ),
    );
  }

  static Future<Member> _fetchUserInfoByProfileId(int profileId) async {
    final url = Uri.parse('$_baseUrl/user/user/by-profile/$profileId/');
    final response = await http.get(url, headers: {
      'Authorization': 'Bearer ${AuthService.accessToken}',
      'accept': 'application/json',
    });

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return Member(
        id: profileId,
        email: data['email'],
        firstName: data['first_name'],
        lastName: data['last_name'],
      );
    } else {
      throw Exception('Błąd pobierania użytkownika $profileId');
    }
  }
}
