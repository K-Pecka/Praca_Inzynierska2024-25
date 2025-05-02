import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;

import '../../../core/models/chat_message_model.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/auth_service.dart';
import '../../../core/services/chat_service.dart';
import 'chat_input_field.dart';
import 'message_bubble.dart';

class PrivateChatScreen extends StatefulWidget {
  final int userProfileId;
  final TripModel trip;
  final int chatroomId;

  const PrivateChatScreen({
    super.key,
    required this.userProfileId,
    required this.trip,
    required this.chatroomId,
  });

  @override
  State<PrivateChatScreen> createState() => _PrivateChatScreenState();
}

class _PrivateChatScreenState extends State<PrivateChatScreen> {
  List<MessageModel> _messages = [];
  bool _isLoading = true;
  final ScrollController _scrollController = ScrollController();
  ChatroomModel? _chatroom;
  String? _otherUserName;
  WebSocketChannel? _channel;

  @override
  void initState() {
    super.initState();
    _loadChat();
    _connectWebSocket();
  }

  void _connectWebSocket() {
    final token = AuthService.accessToken;
    if (token == null) {
      print('❌ Brak tokena – nie łączę z WebSocketem.');
      return;
    }

    final uri = Uri.parse('wss://api.plannder.com/ws/chat/${widget.chatroomId}/?token=$token');
    print('🔌 URI WebSocket: $uri');

    _channel = WebSocketChannel.connect(uri);

    _channel!.stream.listen(
          (data) {
        print('📥 Odebrano wiadomość: $data');
        final msg = MessageModel.fromJson(jsonDecode(data));
        setState(() {
          _messages.add(msg);
        });
        _scrollToBottom();
      },
      onError: (error) {
        print('❌ Błąd WebSocket: $error');
      },
      onDone: () {
        print('🔌 WebSocket zamknięty.');
      },
    );
  }

  Future<void> _loadChat() async {
    try {
      final chatrooms = await ChatService.getUserChatrooms(widget.trip.id);
      final room = chatrooms.firstWhere(
            (r) => r.id == widget.chatroomId && r.type == 'private',
        orElse: () => throw Exception("Nie znaleziono czatu prywatnego."),
      );

      final messages = (await ChatService.getMessages(widget.trip.id, room.id)).reversed.toList();

      final isCurrentUserCreator = room.creatorId == widget.userProfileId;
      final otherId = isCurrentUserCreator
          ? (room.memberIds.isNotEmpty ? room.memberIds.first : null)
          : room.creatorId;

      String fullName = 'Nieznany użytkownik';

      if (otherId != null) {
        final localMember = widget.trip.members.firstWhere(
              (m) => m.id == otherId,
          orElse: () => Member(id: otherId, email: ''),
        );

        if (localMember.firstName != null && localMember.firstName!.isNotEmpty) {
          fullName = '${localMember.firstName} ${localMember.lastName}'.trim();
        } else {
          final fetched = await ChatService.getUserByProfileId(otherId);
          fullName = '${fetched.firstName ?? ''} ${fetched.lastName ?? ''}'.trim();
        }
      }

      setState(() {
        _chatroom = room;
        _messages = messages;
        _otherUserName = fullName.isNotEmpty ? fullName : 'Nieznany użytkownik';
        _isLoading = false;
      });

      WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToBottom());
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Błąd ładowania: $e")),
      );
    }
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      _scrollController.jumpTo(_scrollController.position.maxScrollExtent);
    }
  }

  void _sendMessage(String content) {
    if (_channel != null) {
      final message = jsonEncode({'content': content});
      print('📤 Wysyłam wiadomość: $message');
      _channel!.sink.add(message);
    } else {
      print('⚠️ WebSocket channel jest null!');
    }
  }

  @override
  void dispose() {
    _channel?.sink.close(status.goingAway);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_otherUserName ?? 'Czat prywatny'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
        children: [
          Expanded(
            child: ListView.separated(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                final msgDate = DateTime.parse(msg.created).toLocal();
                final formattedDate = DateFormat("d MMMM y", 'pl_PL').format(msgDate);

                final isFirstMessage = index == 0;
                final previousDate = isFirstMessage
                    ? null
                    : DateTime.parse(_messages[index - 1].created).toLocal();

                final isNewDay = isFirstMessage ||
                    previousDate!.day != msgDate.day ||
                    previousDate.month != msgDate.month ||
                    previousDate.year != msgDate.year;

                return Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    if (isNewDay)
                      Center(
                        child: Padding(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          child: Text(
                            formattedDate,
                            style: const TextStyle(
                              color: Colors.grey,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                    MessageBubble(
                      message: msg,
                      isMine: msg.senderId == widget.userProfileId,
                    ),
                  ],
                );
              },
              separatorBuilder: (_, __) => const SizedBox(height: 8),
            ),
          ),
          ChatInputField(onSend: _sendMessage),
        ],
      ),
    );
  }
}