class UserModel {
  final int id;
  final String email;
  final String firstName;
  final String lastName;

  UserModel({
    required this.id,
    required this.email,
    required this.firstName,
    required this.lastName,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      email: json['user']['email'],
      firstName: json['user']['first_name'],
      lastName: json['user']['last_name'],
    );
  }

  String get fullName => "$firstName $lastName";
}