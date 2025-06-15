import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/auth_response_model.dart';

class AuthService {
  static final String _baseUrl = 'https://api.plannder.com';
  static String? _accessToken;
  static String? _refreshToken;
  static String? _firstName;
  static String? _lastName;
  static String? _email;

  static String? get accessToken => _accessToken;

  static String? get refreshToken => _refreshToken;

  static String? get firstName => _firstName;

  static String? get lastName => _lastName;

  static String? get email => _email;

  static void logout() {
    _accessToken = null;
    _refreshToken = null;
    _firstName = null;
    _lastName = null;
    _email = null;
  }

  static Future<AuthResponseModel> login({
    required String email,
    required String password,
  }) async {
    final url = Uri.parse('$_baseUrl/user_auth/login/');
    final headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json',
    };
    final body = jsonEncode({'email': email, 'password': password});

    final response = await http.post(url, headers: headers, body: body);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      _accessToken = data['access'];
      _refreshToken = data['refresh'];
      _firstName = data['first_name'];
      _lastName = data['last_name'];
      _email = data['email'];

      return AuthResponseModel.fromJson(data);
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

  static Future<void> setDefaultProfile({
    required int profileId,
    required String token,
  }) async {
    final url = Uri.parse('$_baseUrl/user/profile/$profileId/update/');
    final headers = {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    };
    final body = jsonEncode({'is_default': true});

    final response = await http.patch(url, headers: headers, body: body);

    if (response.statusCode != 200) {
      throw Exception(
        'Nie udało się ustawić profilu jako domyślny: ${response.body}',
      );
    }
  }

  static Future<void> changePassword({
    required String newPassword,
    required String confirmPassword,
  }) async {
    final url = Uri.parse('$_baseUrl/user/update/');
    final headers = {
      'Authorization': 'Bearer $_accessToken',
      'Content-Type': 'application/json',
    };

    final body = jsonEncode({
      'password': newPassword,
      'password_confirm': confirmPassword,
    });

    final response = await http.put(url, headers: headers, body: body);

    if (response.statusCode != 200) {
      print(response.body);
      throw Exception('Nie udało się zmienić hasła.');

    }
  }
}
