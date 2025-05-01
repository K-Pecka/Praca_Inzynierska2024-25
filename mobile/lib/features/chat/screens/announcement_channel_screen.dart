import 'package:flutter/material.dart';
import 'package:collection/collection.dart'; // ✅ potrzebne do firstWhereOrNull
import '../../../core/models/chat_message_model.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/chat_service.dart';
import 'message_bubble.dart';
import 'chat_input_field.dart';

class AnnouncementChannelScreen extends StatefulWidget {
  final int userProfileId;
  final int profileType; // 1 = turysta, 2 = przewodnik
  final TripModel trip;

  const AnnouncementChannelScreen({
    super.key,
    required this.userProfileId,
    required this.profileType,
    required this.trip,
  });

  @override
  State<AnnouncementChannelScreen> createState() =>
      _AnnouncementChannelScreenState();
}

class _AnnouncementChannelScreenState
    extends State<AnnouncementChannelScreen> {
  ChatroomModel? _announcementRoom;
  List<MessageModel> _messages = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadAnnouncementChannel();
  }

  Future<void> _loadAnnouncementChannel() async {
    try {
      final rooms = await ChatService.getUserChatrooms(widget.trip.id);
      print("🔍 Wszystkie pokoje: ${rooms.map((r) => 'id: ${r.id}, trip: ${r.tripId}, type: ${r.type}').join(', ')}");
      print("🎯 Szukamy kanału ogłoszeniowego dla tripId: ${widget.trip.id}");

      final ChatroomModel? room = rooms.firstWhereOrNull(
            (r) => r.type == 'group' && r.tripId == widget.trip.id,
      );

      if (room == null) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Nie znaleziono kanału ogłoszeniowego.")),
        );
        return;
      }

      final messages = await ChatService.getMessages(widget.trip.id, room.id);

      setState(() {
        _announcementRoom = room;
        _messages = messages;
        _isLoading = false;
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
    await ChatService.sendMessage(
      widget.trip.id,
      _announcementRoom!.id,
      content,
    );
    _loadAnnouncementChannel(); // refresh
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
