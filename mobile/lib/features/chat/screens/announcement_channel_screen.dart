import 'package:flutter/material.dart';
import '../../../core/models/chat_message_model.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/chat_service.dart';
import 'message_bubble.dart';
import 'chat_input_field.dart';
import 'package:intl/intl.dart';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;

import '../../../core/models/chat_message_model.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/chat_service.dart';
import 'chat_input_field.dart';
import 'message_bubble.dart';

class AnnouncementChannelScreen extends StatefulWidget {
  final int userProfileId;
  final int profileType;
  final TripModel trip;

  const AnnouncementChannelScreen({
    super.key,
    required this.userProfileId,
    required this.profileType,
    required this.trip,
  });

  @override
  State<AnnouncementChannelScreen> createState() => _AnnouncementChannelScreenState();
}

class _AnnouncementChannelScreenState extends State<AnnouncementChannelScreen> {
  ChatroomModel? _announcementRoom;
  List<MessageModel> _messages = [];
  bool _isLoading = true;
  final ScrollController _scrollController = ScrollController();
  WebSocketChannel? _channel;

  @override
  void initState() {
    super.initState();
    _loadAnnouncementChannel();
  }

  void _connectWebSocket(int roomId) {
    final uri = Uri.parse('wss://api.plannder.com/ws/chat/$roomId/');
    _channel = WebSocketChannel.connect(uri);

    _channel!.stream.listen((data) {
      final msg = MessageModel.fromJson(jsonDecode(data));
      setState(() {
        _messages.add(msg);
      });
      _scrollToBottom();
    });
  }

  Future<void> _loadAnnouncementChannel() async {
    try {
      final rooms = await ChatService.getUserChatrooms(widget.trip.id);
      final room = rooms.firstWhere(
            (r) => r.type == 'group' && r.tripId == widget.trip.id,
        orElse: () => throw Exception("Brak kanału ogłoszeniowego dla tej wycieczki"),
      );
      final messages = (await ChatService.getMessages(widget.trip.id, room.id)).reversed.toList();

      setState(() {
        _announcementRoom = room;
        _messages = messages;
        _isLoading = false;
      });

      _connectWebSocket(room.id);

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
      _channel!.sink.add(jsonEncode({'content': content}));
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
      appBar: AppBar(title: Text("Kanał: ${widget.trip.name}")),
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
          if (widget.profileType == 2)
            ChatInputField(onSend: _sendMessage),
        ],
      ),
    );
  }
}
