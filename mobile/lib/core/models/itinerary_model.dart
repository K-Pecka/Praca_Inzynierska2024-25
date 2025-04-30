class ItineraryModel {
  final int id;
  final String name;
  final String country;
  final DateTime startDate;
  final DateTime endDate;
  final int tripId;
  final String activitiesCount;

  ItineraryModel({
    required this.id,
    required this.name,
    required this.country,
    required this.startDate,
    required this.endDate,
    required this.tripId,
    required this.activitiesCount,
  });

  @override
  String toString() => name;

  factory ItineraryModel.fromJson(Map<String, dynamic> json) {
    return ItineraryModel(
      id: json['id'],
      name: json['name'],
      country: json['country'],
      startDate: DateTime.parse(json['start_date']),
      endDate: DateTime.parse(json['end_date']),
      tripId: json['trip'],
      activitiesCount: json['activities_count'].toString(),
    );
  }}