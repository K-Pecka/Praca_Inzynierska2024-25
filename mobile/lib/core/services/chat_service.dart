import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:mobile/core/utils/http_handler.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/chat_message_model.dart';
import '../models/chatroom_model.dart';
import 'auth_service.dart';

class ChatService {
  static const String baseUrl = 'https://api.plannder.com';
  static const String wsBaseUrl = 'wss://api.plannder.com/ws/chat';

  static WebSocketChannel? _channel;

  static Future<List<ChatroomModel>> getUserChatrooms(int tripId) async {
    List<ChatroomModel> allRooms = [];
    String? nextUrl = '$baseUrl/trip/$tripId/chat/';

    while (nextUrl != null) {
      final response = await HttpHandler.request(Uri.parse(nextUrl));

      if (response.statusCode == 200) {
        final Map<String, dynamic> decoded = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = decoded['results'];
        allRooms.addAll(results.map((e) => ChatroomModel.fromJson(e)));

        nextUrl = decoded['next'];
      } else {
        throw Exception("Błąd ładowania pokojów: ${response.body}");
      }
    }

    return allRooms;
  }

  static Future<List<MessageModel>> getMessages(int tripId, int roomId) async {
    List<MessageModel> allMessages = [];
    String? nextUrl = '$baseUrl/trip/$tripId/chat/$roomId/chat-message/?page=1&page_size=30';

    while (nextUrl != null) {
      final response = await HttpHandler.request(Uri.parse(nextUrl));

      if (response.statusCode == 200) {
        final Map<String, dynamic> decoded = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = decoded['results'];
        allMessages.addAll(results.map((e) => MessageModel.fromJson(e)));

        nextUrl = decoded['next'];
      } else {
        throw Exception("Błąd ładowania wiadomości: ${response.statusCode}");
      }
    }

    return allMessages;
  }

  static Future<void> sendHttpMessage({
    required int tripId,
    required int roomId,
    required String content,
  }) async {
    final url = Uri.parse('$baseUrl/trip/$tripId/chat/$roomId/chat-message/');
    final body = jsonEncode({'content': content});

    final response = await HttpHandler.request(
      url,
      method: 'POST',
      body: body,
    );

    if (response.statusCode != 201) {
      throw Exception("Błąd wysyłania wiadomości: ${response.body}");
    }
  }

  static void disconnectWebSocket() {
    _channel?.sink.close();
    _channel = null;
  }

  static WebSocketChannel? connectToWebSocket(int chatroomId) {
    final token = AuthService.accessToken;
    if (token == null) return null;
    final uri = Uri.parse('$wsBaseUrl/$chatroomId/?token=$token');
    return WebSocketChannel.connect(uri);
  }

  static void listenToMessages({
    required WebSocketChannel channel,
    required Function(MessageModel message) onMessage,
  }) {
    channel.stream.listen(
          (data) {
        final decoded = data is String ? data : utf8.decode(data);
        final msg = MessageModel.fromJson(jsonDecode(decoded));
        onMessage(msg);
      },
    );
  }

  static void sendMessage(WebSocketChannel channel, String content) {
    final message = jsonEncode({'content': content});
    channel.sink.add(message);
  }
}