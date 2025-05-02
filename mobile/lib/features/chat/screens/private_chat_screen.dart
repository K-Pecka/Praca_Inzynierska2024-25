import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/models/chat_message_model.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
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

  @override
  void initState() {
    super.initState();
    _loadChat();
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

      final other = isCurrentUserCreator
          ? widget.trip.members.firstWhere(
            (m) => room.memberIds.contains(m.id),
        orElse: () => Member(id: 0, email: 'Nieznany użytkownik'),
      )
          : widget.trip.members.firstWhere(
            (m) => m.id == room.creatorId,
        orElse: () => Member(id: 0, email: 'Nieznany użytkownik'),
      );

      setState(() {
        _chatroom = room;
        _messages = messages;
        _otherUserName = other.email;
        _isLoading = false;
      });

      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (_scrollController.hasClients) {
          _scrollController.jumpTo(_scrollController.position.maxScrollExtent);
        }
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Błąd ładowania: $e")),
      );
    }
  }

  Future<void> _sendMessage(String content) async {
    if (_chatroom == null) return;
    await ChatService.sendMessage(widget.trip.id, _chatroom!.id, content);
    _loadChat();
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