import 'package:flutter/material.dart';
import 'package:mobile/core/screens/profile_screen.dart';
import 'package:mobile/core/screens/report_issue_screen.dart';
import 'package:mobile/core/screens/settings_screen.dart';
import 'package:mobile/core/theme/themes.dart';
import '../../features/auth/screens/start_screen.dart';
import '../services/auth_service.dart';
import '../theme/text_styles.dart';

class ProfileMenuScreen extends StatelessWidget {
  const ProfileMenuScreen({super.key});

  void _logout(BuildContext context) async {
    AuthService.logout();
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const StartScreen()),
      (route) => false,
    );
  }

  String _getInitials() {
    final f =
        AuthService.firstName?.isNotEmpty == true
            ? AuthService.firstName![0]
            : '';
    final l =
        AuthService.lastName?.isNotEmpty == true
            ? AuthService.lastName![0]
            : '';
    return (f + l).toUpperCase();
  }

  @override
  Widget build(BuildContext context) {
    final initials = _getInitials();
    return Scaffold(
      backgroundColor: AppColors.screenBackground,
      appBar: AppBar(
        backgroundColor: AppColors.screenBackground,
        foregroundColor: AppColors.titleText,
      ),
      body: ListView(
        children: [
          const SizedBox(height: 16),
          Center(
            child: Column(
              children: [
                CircleAvatar(
                  radius: 40,
                  backgroundColor: AppColors.cardsBackground,
                  child: Text(initials, style: TextStyles.menuInitials),
                ),
                const SizedBox(height: 16),
                Text(
                  "${AuthService.firstName ?? ''} ${AuthService.lastName ?? ''}",
                  style: TextStyles.sectionHeading,
                ),
                const SizedBox(height: 12),
              ],
            ),
          ),
          const SizedBox(height: 24),
          const Divider(color: Colors.grey),

          _buildMenuItem(
            Icons.person,
            "Profil",
            () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ProfileScreen()),
            ),
            color: AppColors.titleText,
          ),
          _buildMenuItem(
            Icons.settings,
            "Ustawienia",
            () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const SettingsScreen()),
            ),
            color: AppColors.titleText,
          ),
          _buildMenuItem(
            Icons.report_problem,
            "Zgłoś problem",
            () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ReportIssueScreen()),
            ),
            color: AppColors.titleText,
          ),
          _buildMenuItem(
            Icons.logout,
            "Wyloguj się",
            () => _logout(context),
            color: AppColors.logout,
          ),
        ],
      ),
    );
  }

  Widget _buildMenuItem(
    IconData icon,
    String label,
    VoidCallback onTap, {
    Color color = Colors.white,
  }) {
    return ListTile(
      leading: Icon(icon, color: color),
      title: Text(label, style: TextStyle(color: color, fontSize: 18, fontWeight: FontWeight.w600)),
      trailing: const Icon(Icons.chevron_right, color: Colors.white),
      onTap: onTap,
    );
  }
}
