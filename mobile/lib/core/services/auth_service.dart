import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService {
  static final String _baseUrl = 'https://api.plannder.com';
  static String? _accessToken;
  static String? _refreshToken;

  static String? get accessToken => _accessToken;
  static String? get refreshToken => _refreshToken;

  static void logout() {
    _accessToken = null;
    _refreshToken = null;
  }

  /// Logowanie – zwraca dane użytkownika i zapisuje tokeny
  static Future<Map<String, dynamic>> login({
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
      final data = jsonDecode(response.body);

      _accessToken = data['access'];
      _refreshToken = data['refresh'];

      return data;
    } else {
      throw Exception('Błąd logowania: ${response.statusCode}');
    }
  }

  static Future<bool> refreshAccessToken() async {
    if (_refreshToken == null) return false;

    final url = Uri.parse('$_baseUrl/user_auth/token/refresh/');
    final headers = {'Content-Type': 'application/json'};
    final body = jsonEncode({'refresh': _refreshToken});

    final response = await http.post(url, headers: headers, body: body);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _accessToken = data['access'];
      if (data.containsKey('refresh')) {
        _refreshToken = data['refresh'];
      }
      return true;
    } else {
      logout();
      return false;
    }
  }
}