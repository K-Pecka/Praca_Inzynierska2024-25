import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../../../core/models/chat_message_model.dart';
import '../../../core/models/chatroom_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/chat_service.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/utils/error_handler.dart';
import '../widgets/chat_input_field.dart';
import '../widgets/message_bubble.dart';

class PrivateChatScreen extends StatefulWidget {
  final int userProfileId;
  final TripModel trip;
  final int? chatroomId;

  const PrivateChatScreen({
    super.key,
    required this.userProfileId,
    required this.trip,
    required this.chatroomId,
  });

  @override
  State<PrivateChatScreen> createState() => _PrivateChatScreenState();
}

class _PrivateChatScreenState extends State<PrivateChatScreen> {
  List<MessageModel> _messages = [];
  bool _isLoading = true;
  final ScrollController _scrollController = ScrollController();
  ChatroomModel? _chatroom;
  String? _otherUserName;
  late WebSocketChannel _channel;

  @override
  void initState() {
    super.initState();
    _loadChat();
  }

  Future<void> _loadChat() async {
    try {
      final chatrooms = await ChatService.getUserChatrooms(widget.trip.id);
      final room = chatrooms.firstWhere(
        (r) => r.id == widget.chatroomId && r.type == 'private',
        orElse: () => throw Exception("Nie znaleziono czatu prywatnego."),
      );

      final messages =
          (await ChatService.getMessages(
            widget.trip.id,
            room.id,
          )).reversed.toList();

      final isCurrentUserCreator = room.creatorId == widget.userProfileId;
      final otherId =
          isCurrentUserCreator
              ? (room.memberIds.isNotEmpty ? room.memberIds.first : null)
              : room.creatorId;

      String fullName = 'Nieznany użytkownik';

      if (otherId != null) {
        Member member;

        try {
          member = widget.trip.members.firstWhere((m) => m.id == otherId);
        } catch (_) {
          member = widget.trip.creator.id == otherId
              ? widget.trip.creator
              : Member(id: otherId, email: '');
        }

        fullName = '${member.firstName ?? ''} ${member.lastName ?? ''}'.trim();
        if (fullName.isEmpty) fullName = member.email;
      }

      setState(() {
        _chatroom = room;
        _messages = messages;
        _otherUserName = fullName.isNotEmpty ? fullName : 'Nieznany użytkownik';
        _isLoading = false;
      });

      _channel = ChatService.connectToWebSocket(room.id)!;

      ChatService.listenToMessages(
        channel: _channel,
        onMessage: (msg) {
          setState(() => _messages.add(msg));
          _scrollToBottom();
        },
      );

      WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToBottom());
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        handleError(context, e, userMessage: 'Nie udało się załadować danych.');
      }
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _sendMessage(String content) {
    ChatService.sendMessage(_channel, content);
  }

  @override
  void dispose() {
    ChatService.disconnectWebSocket();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          _otherUserName ?? 'Czat prywatny',
          style: TextStyles.sectionHeading,
        ),
      ),
      body:
          _isLoading
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
                        final formattedDate = DateFormat(
                          "d MMMM y",
                          'pl_PL',
                        ).format(msgDate);

                        final isFirstMessage = index == 0;
                        final previousDate =
                            isFirstMessage
                                ? null
                                : DateTime.parse(
                                  _messages[index - 1].created,
                                ).toLocal();

                        final isNewDay =
                            isFirstMessage ||
                            previousDate!.day != msgDate.day ||
                            previousDate.month != msgDate.month ||
                            previousDate.year != msgDate.year;

                        return Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            if (isNewDay)
                              Center(
                                child: Padding(
                                  padding: const EdgeInsets.symmetric(
                                    vertical: 10,
                                  ),
                                  child: Text(
                                    formattedDate,
                                    style: TextStyles.subtitle,
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
