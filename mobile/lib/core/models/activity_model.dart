class ActivityModel {
  final String name;
  final DateTime date;
  final String startTime;
  final int duration;

  ActivityModel({
    required this.name,
    required this.date,
    required this.startTime,
    required this.duration,
  });

  factory ActivityModel.fromJson(Map<String, dynamic> json) {
    return ActivityModel(
      name: json['name'],
      date: DateTime.parse(json['date']),
      startTime: json['start_time'],
      duration: json['duration'],
    );
  }
}