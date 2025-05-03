import 'package:flutter/material.dart';
import 'package:mobile/features/chat/screens/private_chat_screen.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/chat_service.dart';
import '../../../core/widgets/base_screen.dart';
import 'announcement_channel_screen.dart';
import '../widgets/chat_tile.dart';

class ChatOverviewScreen extends StatefulWidget {
  final TripModel trip;
  final int userProfileId;
  final int profileType;

  const ChatOverviewScreen({
    super.key,
    required this.trip,
    required this.userProfileId,
    required this.profileType,
  });

  @override
  State<ChatOverviewScreen> createState() => _ChatOverviewScreenState();
}

class _ChatOverviewScreenState extends State<ChatOverviewScreen> {
  List<ChatroomModel> chatrooms = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadChatrooms();
  }

  Future<void> loadChatrooms() async {
    try {
      final rooms = await ChatService.getUserChatrooms(widget.trip.id);
      rooms.sort((a, b) {
        final aDate = DateTime.tryParse(a.lastMessage?.created ?? '') ?? DateTime(2000);
        final bDate = DateTime.tryParse(b.lastMessage?.created ?? '') ?? DateTime(2000);
        return bDate.compareTo(aDate);
      });
      setState(() {
        chatrooms = rooms;
        isLoading = false;
      });
    } catch (e) {
      setState(() => isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Błąd ładowania: $e')));
    }
  }

  Future<String> getChatLabel(ChatroomModel room) async {
    final otherId = room.memberIds.firstWhere(
          (id) => id != widget.userProfileId,
      orElse: () => room.creatorId,
    );

    final local = widget.trip.members.firstWhere(
          (m) => m.id == otherId,
      orElse: () => Member(id: otherId, email: ''),
    );

    if ((local.firstName ?? '').isNotEmpty) {
      return '${local.firstName} ${local.lastName}'.trim();
    }

    final fetched = await ChatService.getUserByProfileId(otherId);
    return '${fetched.firstName ?? ''} ${fetched.lastName ?? ''}'.trim();
  }

  Future<String> getInitialsForRoom(ChatroomModel room) async {
    final otherId = room.memberIds.firstWhere(
          (id) => id != widget.userProfileId,
      orElse: () => room.creatorId,
    );

    final local = widget.trip.members.firstWhere(
          (m) => m.id == otherId,
      orElse: () => Member(id: otherId, email: ''),
    );

    String first = '';
    String last = '';

    if ((local.firstName ?? '').isNotEmpty) {
      first = local.firstName![0];
      last = (local.lastName?.isNotEmpty ?? false) ? local.lastName![0] : '';
    } else {
      final fetched = await ChatService.getUserByProfileId(otherId);
      first = fetched.firstName?.isNotEmpty == true ? fetched.firstName![0] : '';
      last = fetched.lastName?.isNotEmpty == true ? fetched.lastName![0] : '';
    }

    return (first + last).toUpperCase();
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    ChatroomModel? announcement;
    try {
      announcement = chatrooms.firstWhere((r) => r.type == 'group');
    } catch (_) {
      announcement = null;
    }

    final otherRooms = chatrooms.where((r) => r.type != 'group').toList();

    return BaseScreen(
      trip: widget.trip,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (announcement != null)
            ChatTile(
              label: 'Kanał ogłoszeniowy',
              message: announcement.lastMessage?.content ?? 'Brak wiadomości',
              isAnnouncement: true,
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => AnnouncementChannelScreen(
                      userProfileId: widget.userProfileId,
                      profileType: widget.profileType,
                      trip: widget.trip,
                    ),
                  ),
                );
              },
            ),
          const SizedBox(height: 8),

          for (var room in otherRooms)
            FutureBuilder(
              future: Future.wait([
                getChatLabel(room),
                getInitialsForRoom(room),
              ]),
              builder: (context, snapshot) {
                if (!snapshot.hasData) {
                  return const SizedBox(height: 60);
                }
                final label = snapshot.data![0];
                final initials = snapshot.data![1];
                return ChatTile(
                  label: label,
                  initials: initials,
                  message: room.lastMessage?.content ?? 'Brak wiadomości',
                  isAnnouncement: false,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => PrivateChatScreen(
                          userProfileId: widget.userProfileId,
                          trip: widget.trip,
                          chatroomId: room.id,
                        ),
                      ),
                    );
                  },
                );
              },
            ),
        ],
      ),
    );
  }
}