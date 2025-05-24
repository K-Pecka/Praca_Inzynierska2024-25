import 'package:flutter/material.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  void _changePassword(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Zmień hasło - funkcjonalność w budowie')),
    );
  }

  void _deleteAccount(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Usuń konto - funkcjonalność w budowie')),
    );
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
          ListTile(
            leading: const Icon(Icons.lock, color: AppColors.titleText),
            title: const Text('Zmień hasło', style: TextStyles.cardTitleHeading),
            onTap: () => _changePassword(context),
          ),
          ListTile(
            leading: const Icon(Icons.delete, color: Colors.red),
            title: const Text('Usuń konto', style: TextStyle(color: Colors.red, fontWeight: FontWeight.w600, fontSize: 18)),
            onTap: () => _deleteAccount(context),
          ),
        ],
      ),
    );
  }
}