class ChatroomModel {
  final int id;
  final String name;
  final String type;
  final int tripId;
  final int creatorId;
  final List<int> memberIds;
  final Map<String, dynamic> settings;
  final LastMessage? lastMessage;

  ChatroomModel({
    required this.id,
    required this.name,
    required this.type,
    required this.tripId,
    required this.creatorId,
    required this.memberIds,
    required this.settings,
    required this.lastMessage,
  });

  factory ChatroomModel.fromJson(Map<String, dynamic> json) {
    return ChatroomModel(
      id: json['id'],
      name: json['name'],
      type: json['type'],
      tripId: json['trip'],
      creatorId: json['creator'],
      memberIds: List<int>.from(json['members']),
      settings: json['settings'],
      lastMessage: json['last_message'] != null
          ? LastMessage.fromJson(json['last_message'])
          : null,
    );
  }
}

class LastMessage {
  final String content;
  final String created;

  LastMessage({required this.content, required this.created});

  factory LastMessage.fromJson(Map<String, dynamic> json) {
    return LastMessage(
      content: json['content'] ?? '',
      created: json['created'] ?? '',
    );
  }
}