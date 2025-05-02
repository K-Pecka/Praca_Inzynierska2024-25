class TripModel {
  final int id;
  final String name;
  final int creatorId;
  final List<Member> members;
  final DateTime startDate;
  final DateTime endDate;

  TripModel({
    required this.id,
    required this.name,
    required this.creatorId,
    required this.members,
    required this.startDate,
    required this.endDate,
  });

  @override
  String toString() => name;

  factory TripModel.fromJson(Map<String, dynamic> json) {
    return TripModel(
      id: json['id'],
      name: json['name'],
      creatorId: json['creator'],
      members: (json['members'] as List)
          .map((id) => Member(id: id, email: ''))
          .toList(),
      startDate: DateTime.parse(json['start_date']),
      endDate: DateTime.parse(json['end_date']),
    );
  }
}

class Member {
  final int id;
  final String email;
  final String? firstName;
  final String? lastName;

  Member({
    required this.id,
    required this.email,
    this.firstName,
    this.lastName,
  });

  factory Member.fromJson(Map<String, dynamic> json) {
    return Member(
      id: json['id'],
      email: json['email'],
      firstName: json['first_name'],
      lastName: json['last_name'],
    );
  }

  Member copyWith({
    String? email,
    String? firstName,
    String? lastName,
  }) {
    return Member(
      id: id,
      email: email ?? this.email,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
    );
  }
}