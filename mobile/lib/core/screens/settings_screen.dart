import 'package:flutter/material.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';
import 'change_password_screen.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  void _changePassword(BuildContext context) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Zmień hasło')));
  }

  void _deleteAccount(BuildContext context) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Usuń konto')));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.screenBackground,
      appBar: AppBar(
        title: const Text('Ustawienia', style: TextStyles.sectionHeading),
        backgroundColor: AppColors.screenBackground,
        foregroundColor: AppColors.titleText,
      ),
      body: ListView(
        children: [
          _buildSettingsItem(Icons.lock, 'Zmień hasło', () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ChangePasswordScreen()),
            );
          }, color: AppColors.titleText),
          _buildSettingsItem(
            Icons.delete,
            'Usuń konto',
            () => _deleteAccount(context),
            color: AppColors.logout,
          ),
        ],
      ),
    );
  }
}

Widget _buildSettingsItem(
  IconData icon,
  String label,
  VoidCallback onTap, {
  Color color = Colors.white,
}) {
  return ListTile(
    leading: Icon(icon, color: color),
    title: Text(
      label,
      style: TextStyle(color: color, fontSize: 18, fontWeight: FontWeight.w600),
    ),
    trailing: const Icon(Icons.chevron_right, color: Colors.white),
    onTap: onTap,
  );
}
