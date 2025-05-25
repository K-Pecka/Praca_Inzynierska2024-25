import 'dart:convert';

class TripModel {
  final int id;
  final String name;
  final Member creator;
  final List<Member> members;
  final DateTime startDate;
  final DateTime endDate;
  final bool isCreator;
  final double budgetAmount;

  TripModel({
    required this.id,
    required this.name,
    required this.creator,
    required this.members,
    required this.startDate,
    required this.endDate,
    required this.isCreator,
    required this.budgetAmount,
  });

  @override
  String toString() => name;

  factory TripModel.fromJson(Map<String, dynamic> json) {
    return TripModel(
      id: json['id'],
      name: json['name'],
      creator: Member.fromJson(json['creator']),
      members: json['members'] != null
          ? (json['members'] as List).map((m) => Member.fromJson(m)).toList()
          : [],
      startDate: DateTime.parse(json['start_date']),
      endDate: DateTime.parse(json['end_date']),
      isCreator: json['is_creator'],
      budgetAmount: double.tryParse(json['budget_amount'].toString()) ?? 5000.0,
    );
  }
}

class Member {
  final int id;
  final String email;
  final String? firstName;
  final String? lastName;
  final int? type;

  Member({
    required this.id,
    required this.email,
    this.firstName,
    this.lastName,
    this.type,
  });

  factory Member.fromJson(Map<String, dynamic> json) {
    print('👤 [DEBUG] Member JSON: ${jsonEncode(json)}');
    return Member(
      id: json['id'] as int,
      email: json['email'] ?? 'unknown@example.com',
      firstName: json['first_name'],
      lastName: json['last_name'],
      type: json['type'], // ← jeśli to się wywali, wiemy wszystko
    );
  }

  Member copyWith({
    String? email,
    String? firstName,
    String? lastName,
    int? type,
  }) {
    return Member(
      id: id,
      email: email ?? this.email,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      type: type ?? this.type,
    );
  }
}
