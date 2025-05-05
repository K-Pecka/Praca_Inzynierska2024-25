import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/trip_model.dart';
import 'auth_service.dart';

class UserService{
  Future<Member> fetchUserInfoByProfileId(int profileId) async {
    final url = Uri.parse('https://api.plannder.com/user/user/by-profile/$profileId/');
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
      throw Exception("Błąd ładowania danych użytkownika: ${response.body}");
    }
  }

}