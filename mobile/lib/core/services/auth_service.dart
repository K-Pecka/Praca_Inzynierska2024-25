import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService {
  final String _baseUrl = 'https://api.plannder.com';

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final url = Uri.parse('$_baseUrl/user_auth/login/');
    final headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json',
    };

    final body = jsonEncode({
      'email': email,
      'password': password,
    });

    final response = await http.post(url, headers: headers, body: body);

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Błąd: ${response.statusCode}');
    }
  }
}