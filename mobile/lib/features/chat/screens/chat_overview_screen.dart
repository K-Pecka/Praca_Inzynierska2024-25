// import 'package:flutter/material.dart';
// import '../../../core/models/chatroom_model.dart';
// import '../../../core/models/trip_model.dart';
// import '../../../core/services/chat_service.dart';
//
// class ChatOverviewScreen extends StatefulWidget {
//   final TripModel trip;
//
//   const ChatOverviewScreen({
//     super.key,
//     required this.trip,
//   });
//
//   @override
//   State<ChatOverviewScreen> createState() => _ChatOverviewScreenState();
// }
//
// class _ChatOverviewScreenState extends State<ChatOverviewScreen> {
//   List<ChatroomModel> chatrooms = [];
//   bool isLoading = true;
//
//   @override
//   void initState() {
//     super.initState();
//     loadChatrooms();
//   }
//
//   Future<void> loadChatrooms() async {
//     try {
//       final rooms = await ChatService.getUserChatrooms(widget.trip.id);
//       rooms.sort((a, b) => b.created.compareTo(a.created));
//       setState(() {
//         chatrooms = rooms;
//         isLoading = false;
//       });
//     } catch (e) {
//       setState(() => isLoading = false);
//       ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Błąd ładowania: $e')));
//     }
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     if (isLoading) {
//       return const Scaffold(
//         body: Center(child: CircularProgressIndicator()),
//       );
//     }
//
//     final announcement = chatrooms.firstWhere(
//           (r) => r.type == 'group',
//       orElse: () => ChatroomModel(
//         id: 0,
//         name: 'Ogłoszenia',
//         type: 'group',
//         tripId: widget.trip.id,
//         creatorId: 0,
//         memberIds: [],
//         settings: {},
//         created: DateTime.now().toIso8601String(),
//       ),
//     );
//
//     final otherRooms = chatrooms.where((r) => r.type != 'group').toList();
//
//     return Scaffold(
//       appBar: AppBar(
//         title: Text(widget.trip.name),
//       ),
//       body: ListView(
//         padding: const EdgeInsets.all(16),
//         children: [
//           ChatTile(
//             label: 'Pamiętajcie że dzisiaj...',
//             icon: Icons.info_outline,
//             onTap: () {
//               // Navigator.push to AnnouncementChannelScreen
//             },
//           ),
//           const SizedBox(height: 8),
//           for (var room in otherRooms)
//             ChatTile(
//               label: 'Hej, Pamiętasz o tym co...',
//               initials: 'MW',
//               onTap: () {
//                 // Navigator.push to ChatDetailScreen
//               },
//             ),
//         ],
//       ),
//     );
//   }
// }
//
// class ChatTile extends StatelessWidget {
//   final String label;
//   final IconData? icon;
//   final String? initials;
//   final VoidCallback onTap;
//
//   const ChatTile({
//     super.key,
//     required this.label,
//     this.icon,
//     this.initials,
//     required this.onTap,
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
//             child: icon != null
//                 ? Icon(icon, color: Colors.deepPurple)
//                 : Text(initials ?? '', style: const TextStyle(color: Colors.deepPurple)),
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
//                 child: Text(
//                   label,
//                   overflow: TextOverflow.ellipsis,
//                   style: const TextStyle(fontSize: 15),
//                 ),
//               ),
//             ),
//           ),
//         ],
//       ),
//     );
//   }
// }