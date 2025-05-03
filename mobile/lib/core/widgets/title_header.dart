import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../../features/auth/screens/start_screen.dart';
import '../theme/text_styles.dart';
import '../services/auth_service.dart';
import 'menu_screen.dart';

class TripTitleHeader extends StatelessWidget {
  final String title;

  const TripTitleHeader({
    super.key,
    required this.title,
  });

  String _getInitials() {
    final f = AuthService.firstName?.isNotEmpty == true ? AuthService.firstName![0] : '';
    final l = AuthService.lastName?.isNotEmpty == true ? AuthService.lastName![0] : '';
    return (f + l).toUpperCase();
  }

  @override
  Widget build(BuildContext context) {
    final initials = _getInitials();

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.only(top: 32, left: 0, right: 0, bottom: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            title,
            style: TextStyles.sectionHeading,
          ),
          GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const ProfileMenuScreen()),
              );
            },
            child: CircleAvatar(
              radius: 20,
              backgroundColor: const Color(0x80DEDCFF),
              child: Text(
                initials,
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                  color: Color(0xBF2F27CE),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}