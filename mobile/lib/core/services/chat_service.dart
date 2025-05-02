import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import '../models/chat_message_model.dart';
import '../models/chatroom_model.dart';
import '../../core/services/auth_service.dart';

import 'package:flutter/foundation.dart';
import '../models/trip_model.dart';

class ChatService {
  static const String baseUrl = 'https://api.plannder.com';

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

  static Future<void> sendMessage(int tripId, int chatroomId, String text) async {
    final url = Uri.parse('$baseUrl/trip/$tripId/chat/$chatroomId/chat-message/create/');
    final response = await http.post(url,
      headers: {
        'Authorization': 'Bearer ${AuthService.accessToken}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'content': text}),
    );

    if (response.statusCode != 201) {
      throw Exception("Nie udało się wysłać wiadomości: ${response.body}");
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