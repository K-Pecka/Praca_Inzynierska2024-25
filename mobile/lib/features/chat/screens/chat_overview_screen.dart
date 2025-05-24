import 'package:flutter/material.dart';
import 'package:mobile/features/chat/screens/private_chat_screen.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/chat_service.dart';
import '../../../core/utils/error_handler.dart';
import '../../../core/screens/base_screen.dart';
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

      if (!mounted) return;

      setState(() {
        chatrooms = rooms;
        isLoading = false;
      });
    } catch (e) {
      if (mounted) {
        setState(() => isLoading = false);
        handleError(context, e, userMessage: 'Nie udało się załadować czatów.');
      }
    }
  }

  String getChatLabel(ChatroomModel room) {
    final otherId = room.memberIds.firstWhere(
          (id) => id != widget.userProfileId,
      orElse: () => room.creatorId,
    );

    Member member;

    try {
      member = widget.trip.members.firstWhere((m) => m.id == otherId);
    } catch (_) {
      member = widget.trip.creator.id == otherId
          ? widget.trip.creator
          : Member(id: otherId, email: '');
    }

    final name = '${member.firstName ?? ''} ${member.lastName ?? ''}'.trim();
    return name.isNotEmpty ? name : member.email;
  }

  String getInitialsForRoom(ChatroomModel room) {
    final otherId = room.memberIds.firstWhere(
          (id) => id != widget.userProfileId,
      orElse: () => room.creatorId,
    );

    Member member;

    try {
      member = widget.trip.members.firstWhere((m) => m.id == otherId);
    } catch (_) {
      member = widget.trip.creator.id == otherId
          ? widget.trip.creator
          : Member(id: otherId, email: '');
    }

    final first = (member.firstName?.isNotEmpty ?? false) ? member.firstName![0] : '';
    final last = (member.lastName?.isNotEmpty ?? false) ? member.lastName![0] : '';

    final initials = (first + last).toUpperCase();
    return initials.isNotEmpty ? initials : member.email.characters.first.toUpperCase();
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
            ChatTile(
              label: getChatLabel(room),
              initials: getInitialsForRoom(room),
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
            ),
        ],
      ),
    );
  }
}