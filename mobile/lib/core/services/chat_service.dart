import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart';

import '../models/chat_message_model.dart';
import '../models/chatroom_model.dart';
import '../models/trip_model.dart';
import 'auth_service.dart';

class ChatService {
  static const String baseUrl = 'https://api.plannder.com';
  static const String wsBaseUrl = 'wss://api.plannder.com/ws/chat';

  static WebSocketChannel? _channel;

  static Future<List<ChatroomModel>> getUserChatrooms(int tripId) async {
    final url = Uri.parse('$baseUrl/trip/$tripId/chat/chatroom/all/');
    final response = await http.get(url, headers: {
      'Authorization': 'Bearer ${AuthService.accessToken}',
      'accept': 'application/json',
    });

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);
      return data.map((e) => ChatroomModel.fromJson(e)).toList();
    } else {
      throw Exception("Błąd ładowania pokojów: ${response.body}");
    }
  }

  static Future<List<MessageModel>> getMessages(int tripId, int chatroomId) async {
    final url = Uri.parse('$baseUrl/trip/$tripId/chat/$chatroomId/chat-message/all/');

    final response = await http.get(url, headers: {
      'Authorization': 'Bearer ${AuthService.accessToken}',
      'accept': 'application/json',
    });

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);
      return data.map((e) => MessageModel.fromJson(e)).toList();
    } else {
      throw Exception("Błąd ładowania wiadomości: ${response.statusCode}");
    }
  }

  static void disconnectWebSocket() {
    _channel?.sink.close();
    _channel = null;
  }

  static Future<Member> getUserByProfileId(int profileId) async {
    final url = Uri.parse('$baseUrl/user/user/by-profile/$profileId/');
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

  static WebSocketChannel? connectToWebSocket(int chatroomId) {
    final token = AuthService.accessToken;
    if (token == null) {
      return null;
    }

    final uri = Uri.parse('wss://api.plannder.com/ws/chat/$chatroomId/?token=$token');

    return WebSocketChannel.connect(uri);
  }

  static void listenToMessages({
    required WebSocketChannel channel,
    required Function(MessageModel message) onMessage,
  }) {
    channel.stream.listen(
          (data) {
        final msg = MessageModel.fromJson(jsonDecode(data));
        onMessage(msg);
      },
    );
  }

  static void sendMessage(WebSocketChannel channel, String content) {
    final message = jsonEncode({'content': content});
    channel.sink.add(message);
  }
}