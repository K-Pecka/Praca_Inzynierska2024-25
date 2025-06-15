import 'package:mobile/core/models/trip_model.dart';

class DebtModel {
  final int id;
  final String name;
  final Member creator;
  final String price;
  final String currency;
  final double priceInPln;
  final List<Member> members;
  final String pricePerMember;
  final double pricePerMemberInPln;

  DebtModel({
    required this.id,
    required this.name,
    required this.creator,
    required this.price,
    required this.currency,
    required this.priceInPln,
    required this.members,
    required this.pricePerMember,
    required this.pricePerMemberInPln,
  });

  factory DebtModel.fromJson(Map<String, dynamic> json) {
    return DebtModel(
      id: json['id'],
      name: json['name'],
      creator: Member.fromJson(json['creator']),
      price: json['amount'].toString(),
      currency: json['currency'],
      priceInPln: double.tryParse(json['amount_in_pln'].toString()) ?? 0.0,
      members: (json['members'] as List)
          .map((m) => Member.fromJson(m))
          .toList(),
      pricePerMember: json['amount_per_member'].toString(),
      pricePerMemberInPln:
      double.tryParse(json['amount_per_member_in_pln'].toString()) ?? 0.0,
    );
  }
}