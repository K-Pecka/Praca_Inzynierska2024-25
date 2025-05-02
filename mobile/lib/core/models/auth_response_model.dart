class AuthResponseModel {
  final String access;
  final String refresh;
  final String email;
  final String fullname;
  final List<UserProfile> profiles;

  AuthResponseModel({
    required this.access,
    required this.refresh,
    required this.email,
    required this.fullname,
    required this.profiles,
  });

  factory AuthResponseModel.fromJson(Map<String, dynamic> json) {
    return AuthResponseModel(
      access: json['access'],
      refresh: json['refresh'],
      email: json['email'],
      fullname: json['fullname'],
      profiles: (json['profiles'] as List)
          .map((p) => UserProfile.fromJson(p))
          .toList(),
    );
  }
}

class UserProfile {
  final int id;
  final int type;
  final bool isDefault;

  UserProfile({
    required this.id,
    required this.type,
    required this.isDefault,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id'],
      type: json['type'],
      isDefault: json['is_default'],
    );
  }
}