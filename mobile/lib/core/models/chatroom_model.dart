class ChatroomModel {
  final int id;
  final String name;
  final String type;
  final int tripId;
  final int creatorId;
  final List<int> memberIds;
  final String settings;

  ChatroomModel({
    required this.id,
    required this.name,
    required this.type,
    required this.tripId,
    required this.creatorId,
    required this.memberIds,
    required this.settings,
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
    );
  }
}