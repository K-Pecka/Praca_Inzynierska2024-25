import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/chat_message_model.dart';
import '../models/chatroom_model.dart';
import '../../core/services/auth_service.dart';

class ChatService {
  static const String baseUrl = 'https://api.plannder.com';

  static Future<List<ChatroomModel>> getUserChatrooms() async {
    final url = Uri.parse('$baseUrl/chats/chatroom/list/');
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

  static Future<List<MessageModel>> getMessages(int chatroomId) async {
    final url = Uri.parse('$baseUrl/chats/message/list/?chatroom=$chatroomId');
    final response = await http.get(url, headers: {
      'Authorization': 'Bearer ${AuthService.accessToken}',
      'accept': 'application/json',
    });

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);
      return data.map((e) => MessageModel.fromJson(e)).toList();
    } else {
      throw Exception("Błąd ładowania wiadomości");
    }
  }

  static Future<void> sendMessage(int chatroomId, String text) async {
    final url = Uri.parse('$baseUrl/chats/message/create/');
    final response = await http.post(url,
      headers: {
        'Authorization': 'Bearer ${AuthService.accessToken}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'chatroom': chatroomId,
        'content': text,
      }),
    );

    if (response.statusCode != 201) {
      throw Exception("Nie udało się wysłać wiadomości");
    }
  }
}