import 'package:intl/intl.dart';

class ExpenseModel {
  final int id;
  final String title;
  final double amount;
  final String currency;
  final DateTime date;
  final String? note;
  final String category;
  final String? user;
  final String? username;

  ExpenseModel({
    required this.id,
    required this.title,
    required this.amount,
    required this.currency,
    required this.date,
    required this.category,
    this.note,
    this.user,
    this.username
  });

  factory ExpenseModel.fromJson(Map<String, dynamic> json) {
    return ExpenseModel(
      id: json['id'],
      title: json['title'],
      amount: double.parse(json['amount'].toString()),
      currency: json['currency'].toString(),
      date: DateFormat('dd.MM.yyyy').parse(json['date']),
      category: json['category'].toString(),
      note: json['note'],
      user: json['user']?.toString(),
      username: json['username']?.toString(),
    );
  }
}