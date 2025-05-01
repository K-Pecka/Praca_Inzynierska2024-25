import 'package:flutter/material.dart';
import '../../../core/models/chat_message_model.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/chat_service.dart';
import 'message_bubble.dart';
import 'chat_input_field.dart';

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

  @override
  void initState() {
    super.initState();
    _loadAnnouncementChannel();
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
    if (_announcementRoom == null) return;
    await ChatService.sendMessage(widget.trip.id, _announcementRoom!.id, content);
    _loadAnnouncementChannel();
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
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return MessageBubble(
                  message: msg,
                  isMine: msg.senderId == widget.userProfileId,
                );
              },
            ),
          ),
          if (widget.profileType == 2)
            ChatInputField(onSend: _sendMessage),
        ],
      ),
    );
  }
}
