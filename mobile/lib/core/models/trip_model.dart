class TripModel {
  final int id;
  final String name;
  final int creatorId;
  final List<Member> members;
  final DateTime startDate;
  final DateTime endDate;
  final double budgetAmount;

  TripModel({
    required this.id,
    required this.name,
    required this.creatorId,
    required this.members,
    required this.startDate,
    required this.endDate,
    required this.budgetAmount,
  });

  factory TripModel.fromJson(Map<String, dynamic> json) {
    return TripModel(
      id: json['id'],
      name: json['name'],
      creatorId: json['creator'],
      members: (json['members'] as List<dynamic>)
          .map((member) => Member.fromJson(member))
          .toList(),
      startDate: DateTime.parse(json['start_date']),
      endDate: DateTime.parse(json['end_date']),
      budgetAmount: double.tryParse(json['budget_amount'].toString()) ?? 0.0,
    );
  }
}

class Member {
  final int id;
  final String email;

  Member({
    required this.id,
    required this.email,
  });

  factory Member.fromJson(Map<String, dynamic> json) {
    return Member(
      id: json['id'],
      email: json['email'],
    );
  }
}