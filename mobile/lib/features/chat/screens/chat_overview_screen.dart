import 'package:flutter/material.dart';
import 'package:mobile/features/chat/screens/private_chat_screen.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/models/user_model.dart';
import '../../../core/services/chat_service.dart';
import '../widgets/new_message_dropdown.dart';
import 'announcement_channel_screen.dart';
import '../../../core/services/auth_service.dart';
import 'chat_tile.dart';

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

  List<UserModel> get userParticipants {
    return widget.trip.members.map((m) => UserModel(
      id: m.id,
      email: m.email,
      firstName: '', // lub m.firstName jeśli masz
      lastName: '',  // lub m.lastName jeśli masz
    )).toList();
  }

  String getChatLabel(ChatroomModel room) {
    final otherIds = room.memberIds.where((id) => id != widget.userProfileId);
    try {
      final other = widget.trip.members.firstWhere((m) => otherIds.contains(m.id));
      final fullName = '${other.firstName} ${other.lastName}'.trim();
      return fullName.isNotEmpty ? fullName : other.email;
    } catch (_) {
      return 'Nieznany użytkownik';
    }
  }

  String getInitialsForRoom(ChatroomModel room) {
    final otherIds = room.memberIds.where((id) => id != widget.userProfileId);
    try {
      final other = widget.trip.members.firstWhere((m) => otherIds.contains(m.id));
      final first = (other.firstName ?? '').isNotEmpty ? other.firstName![0] : '';
      final last = (other.lastName ?? '').isNotEmpty ? other.lastName![0] : '';
      return (first + last).toUpperCase();
    } catch (_) {
      return '??';
    }
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

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.trip.name),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // 🔽 Dropdown na górze ekranu
          // NewMessageDropdown(
          //   participants: userParticipants,
          //   trip: widget.trip,
          //   currentUserId: widget.userProfileId,
          //   token: AuthService.accessToken ?? '', // ✅ TO MUSI BYĆ TUTAJ
          //   onChatroomCreated: (newRoom) {
          //     setState(() {
          //       chatrooms.insert(0, newRoom);
          //     });
          //   },
          // ),
          const SizedBox(height: 16),

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
              message: room.lastMessage?.content ?? 'Brak wiadomości',
              isAnnouncement: false,
              initials: getInitialsForRoom(room),
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

// class ChatTile extends StatelessWidget {
//   final String label;
//   final String message;
//   final VoidCallback onTap;
//   final bool isAnnouncement;
//
//   const ChatTile({
//     super.key,
//     required this.label,
//     required this.message,
//     required this.onTap,
//     this.isAnnouncement = false, required String initials,
//   });
//
//   @override
//   Widget build(BuildContext context) {
//     return Padding(
//       padding: const EdgeInsets.symmetric(vertical: 6),
//       child: Row(
//         children: [
//           CircleAvatar(
//             radius: 20,
//             backgroundColor: const Color(0xFFDEDCFF).withOpacity(0.5),
//             child: isAnnouncement
//                 ? const Icon(Icons.info_outline, color: Color(0xFF6A5AE0))
//                 : const Text("MW", style: TextStyle(color: Color(0xFF6A5AE0))),
//           ),
//           const SizedBox(width: 12),
//           Expanded(
//             child: GestureDetector(
//               onTap: onTap,
//               child: Container(
//                 padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
//                 decoration: BoxDecoration(
//                   color: const Color(0xFFDEDCFF).withOpacity(0.2),
//                   borderRadius: BorderRadius.circular(16),
//                 ),
//                 child: Column(
//                   crossAxisAlignment: CrossAxisAlignment.start,
//                   children: [
//                     Text(
//                       label,
//                       style: const TextStyle(
//                         fontWeight: FontWeight.bold,
//                         fontSize: 14,
//                       ),
//                     ),
//                     Text(
//                       message,
//                       overflow: TextOverflow.ellipsis,
//                       style: const TextStyle(fontSize: 15),
//                     ),
//                   ],
//                 ),
//               ),
//             ),
//           ),
//         ],
//       ),
//     );
//   }
// }