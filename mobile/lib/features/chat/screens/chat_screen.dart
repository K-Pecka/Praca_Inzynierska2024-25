import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/models/chat_message_model.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/chat_service.dart';
import 'chat_input_field.dart';
import 'message_bubble.dart';

class ChatScreen extends StatefulWidget {
  final TripModel trip;
  final ChatroomModel chatroom;
  final int userProfileId;

  const ChatScreen({
    super.key,
    required this.trip,
    required this.chatroom,
    required this.userProfileId,
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  List<MessageModel> _messages = [];
  bool _isLoading = true;
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _loadMessages();
  }

  Future<void> _loadMessages() async {
    try {
      final messages = await ChatService.getMessages(widget.trip.id, widget.chatroom.id);
      setState(() {
        _messages = messages.reversed.toList();
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
    await ChatService.sendMessage(widget.trip.id, widget.chatroom.id, content);
    _loadMessages();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.chatroom.name)),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
        children: [
          Expanded(
            child: ListView.separated(
              padding: const EdgeInsets.all(16),
              controller: _scrollController,
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