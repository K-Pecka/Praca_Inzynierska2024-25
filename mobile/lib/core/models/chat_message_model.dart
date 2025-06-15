class MessageModel {
  final int id;
  final String content;
  final int senderId;
  final String created;

  MessageModel({
    required this.id,
    required this.content,
    required this.senderId,
    required this.created,
  });

  factory MessageModel.fromJson(Map<String, dynamic> json) {
    return MessageModel(
      id: json['id'],
      content: json['message'] ?? json['content'],
      senderId: json['sender_id'] ?? json['profile'],
      created: json['created'],
    );
  }
}