import 'package:flutter/material.dart';
import 'package:mobile/features/chat/screens/private_chat_screen.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/chat_service.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';
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

    final otherRooms = chatrooms
        .where((r) => r.type != 'group' && r.lastMessage != null)
        .toList();

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
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primary,
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              label: const Text('Nowa wiadomość', style: TextStyles.whiteSubtitle),
              onPressed: () => _showNewMessageDialog(context),
            ),
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

  void _showNewMessageDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (_) {
        return AlertDialog(
          title: const Text('Wybierz odbiorcę'),
          content: SizedBox(
            width: double.maxFinite,
            height: 300,
            child: Column(
              children: [
                Expanded(
                  child: ListView.builder(
                    itemCount: widget.trip.members.length,
                    itemBuilder: (_, i) {
                      final m = widget.trip.members[i];
                      final name = '${m.firstName ?? ''} ${m.lastName ?? ''}'.trim();
                      return ListTile(
                        leading: CircleAvatar(
                          child: Text(
                              (m.firstName?.substring(0,1) ?? m.email[0]).toUpperCase()
                          ),
                        ),
                        title: Text(name.isNotEmpty ? name : m.email),
                        onTap: () async {
                          Navigator.pop(context);

                          try {
                            final chatroom = chatrooms.firstWhere((r) =>
                            r.type == 'private' &&
                                ((r.creatorId == widget.userProfileId && r.memberIds.contains(m.id)) ||
                                    (r.creatorId == m.id && r.memberIds.contains(widget.userProfileId)))
                            );

                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => PrivateChatScreen(
                                  userProfileId: widget.userProfileId,
                                  trip: widget.trip,
                                  chatroomId: chatroom.id,
                                ),
                              ),
                            ).then((_) => loadChatrooms());
                          } catch (_) {
                            handleError(context, Exception("Nie znaleziono czatu z tym użytkownikiem."));
                          }
                        },
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}