import 'package:http/http.dart' as http;
import '../services/auth_service.dart';

class HttpHandler {
  static Future<http.Response> request(
      Uri url, {
        String method = 'GET',
        Map<String, String>? headers,
        dynamic body,
      }) async {
    headers ??= {};
    headers['Authorization'] = 'Bearer ${AuthService.accessToken}';
    headers['accept'] ??= 'application/json';
    if (['POST', 'PUT', 'PATCH'].contains(method)) {
      headers['Content-Type'] = 'application/json';
    }

    late http.Response response;

    Future<http.Response> send() async {
      switch (method) {
        case 'GET':
          return await http.get(url, headers: headers);
        case 'POST':
          return await http.post(url, headers: headers, body: body);
        case 'PUT':
          return await http.put(url, headers: headers, body: body);
        case 'PATCH':
          return await http.patch(url, headers: headers, body: body);
        case 'DELETE':
          return await http.delete(url, headers: headers);
        default:
          throw Exception('Unsupported HTTP method: $method');
      }
    }

    response = await send();

    if (response.statusCode == 401) {
      final refreshed = await AuthService.refreshAccessToken();
      if (refreshed) {
        headers['Authorization'] = 'Bearer ${AuthService.accessToken}';
        response = await send();
      }
    }

    return response;
  }
}