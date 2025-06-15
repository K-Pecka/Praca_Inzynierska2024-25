// import 'package:animated_custom_dropdown/custom_dropdown.dart';
// import 'package:flutter/material.dart';
// import 'package:http/http.dart' as http;
// import 'dart:convert';
//
// import '../../../core/models/chatroom_model.dart';
// import '../../../core/models/trip_model.dart';
// import '../../../core/models/user_model.dart';
// import '../screens/chat_screen.dart'; // import ChatScreen
//
// class NewMessageDropdown extends StatelessWidget {
//   final List<UserModel> participants;
//   final TripModel trip;
//   final int currentUserId;
//   final String token;
//   final void Function(ChatroomModel)? onChatroomCreated;
//
//   const NewMessageDropdown({
//     super.key,
//     required this.participants,
//     required this.trip,
//     required this.currentUserId,
//     required this.token,
//     this.onChatroomCreated,
//   });
//
//   @override
//   Widget build(BuildContext context) {
//     return CustomDropdown<UserModel>.search(
//       hintText: 'Nowa wiadomość',
//       items: participants,
//       initialItem: null,
//       overlayHeight: 300,
//       onChanged: (UserModel? selectedUser) async {
//         if (selectedUser == null) return;
//
//         final url = Uri.parse('https://api.plannder.com/chatroom/create_or_get/');
//         final payload = {
//           "trip_id": trip.id,
//           "creator_id": currentUserId,
//           "receiver_id": selectedUser.id,
//         };
//
//         print("➡️ Tworzenie czatu z payloadem:");
//         print(payload);
//         print("➡️ Token: $token");
//
//         final response = await http.post(
//           url,
//           headers: {
//             'Authorization': 'Bearer $token',
//             'Content-Type': 'application/json',
//           },
//           body: jsonEncode(payload),
//         );
//
//         print("⬅️ Response status: ${response.statusCode}");
//         print("⬅️ Response body: ${response.body}");
//
//         if (response.statusCode == 200 || response.statusCode == 201) {
//           final data = jsonDecode(response.body);
//           print("✅ Chatroom utworzony/pobrany: $data");
//
//           final chatroom = ChatroomModel.fromJson(data);
//
//           if (onChatroomCreated != null) {
//             onChatroomCreated!(chatroom);
//           }
//
//           Navigator.push(
//             context,
//             MaterialPageRoute(
//               builder: (_) => ChatScreen(
//                 trip: trip,
//                 chatroom: chatroom,
//                 userProfileId: currentUserId,
//               ),
//             ),
//           );
//         } else {
//           print("❌ Błąd odpowiedzi: ${response.statusCode}");
//           ScaffoldMessenger.of(context).showSnackBar(
//             SnackBar(content: Text("❌ Błąd tworzenia czatu: ${response.body}")),
//           );
//         }
//       },
//     );
//   }
// }
