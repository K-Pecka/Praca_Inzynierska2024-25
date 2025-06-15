class ActivityModel {
  final int id;
  final String name;
  final int type;
  final int? ticket;
  final String description;
  final String location;
  final DateTime date;
  final String startTime;
  final int duration;
  final int itinerary;

  ActivityModel({
    required this.id,
    required this.name,
    required this.type,
    required this.ticket,
    required this.description,
    required this.location,
    required this.date,
    required this.startTime,
    required this.duration,
    required this.itinerary,
  });

  factory ActivityModel.fromJson(Map<String, dynamic> json) {
    return ActivityModel(
      id: json['id'],
      name: json['name'],
      type: json['type'],
      ticket: json['ticket'],
      description: json['description'],
      location: json['location'],
      date: DateTime.parse(json['date']),
      startTime: json['start_time'],
      duration: json['duration'],
      itinerary: json['itinerary'],
    );
  }
}