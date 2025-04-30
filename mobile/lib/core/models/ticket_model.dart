class TicketModel {
  final int id;
  final String name;
  final String file;
  final int type;
  final int profile;
  final String validFromDate;
  final String validFromTime;
  final int trip;

  TicketModel({
    required this.id,
    required this.name,
    required this.file,
    required this.type,
    required this.profile,
    required this.validFromDate,
    required this.validFromTime,
    required this.trip,
  });

  factory TicketModel.fromJson(Map<String, dynamic> json) {
    return TicketModel(
      id: json['id'],
      name: json['name'],
      file: json['file'],
      type: json['type'],
      profile: json['profile'],
      validFromDate: json['valid_from_date'],
      validFromTime: json['valid_from_time'],
      trip: json['trip'],
    );
  }
}