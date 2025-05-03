class TicketModel {
  final int id;
  final String name;
  final String file;
  final int type;
  final int owner;
  final List<int> profiles;
  final String? validFromDate;
  final String? validFromTime;
  final int trip;

  TicketModel({
    required this.id,
    required this.name,
    required this.file,
    required this.type,
    required this.owner,
    required this.profiles,
    this.validFromDate,
    this.validFromTime,
    required this.trip,
  });

  factory TicketModel.fromJson(Map<String, dynamic> json) {
    return TicketModel(
      id: json['id'],
      name: json['name'],
      file: json['file'],
      type: json['type'],
      owner: json['owner'],
      profiles: List<int>.from(json['profiles'] ?? []),
      validFromDate: json['valid_from_date'],
      validFromTime: json['valid_from_time'],
      trip: json['trip'],
    );
  }
}