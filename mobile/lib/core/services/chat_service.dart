import 'dart:convert';
import 'package:flutter/cupertino.dart';
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
    debugPrint('➡️ GET $url');

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

  static void connectToWebSocket(int chatroomId, Function(String) onMessageReceived) {
    final uri = Uri.parse('$wsBaseUrl/$chatroomId/');
    _channel = WebSocketChannel.connect(uri);

    _channel!.stream.listen(
          (message) => onMessageReceived(message),
      onError: (error) => debugPrint('❌ WebSocket error: $error'),
      onDone: () => debugPrint('🛑 WebSocket connection closed.'),
    );
  }

  static void disconnectWebSocket() {
    _channel?.sink.close();
    _channel = null;
  }

  static void sendWebSocketMessage(String content) {
    if (_channel != null) {
      _channel!.sink.add(jsonEncode({"content": content}));
    } else {
      debugPrint('⚠️ WebSocket channel is not connected.');
    }
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
}