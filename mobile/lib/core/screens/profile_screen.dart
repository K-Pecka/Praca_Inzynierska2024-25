import 'package:flutter/material.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';
import '../../../core/services/auth_service.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final email = AuthService.email ?? '';
    final firstName = AuthService.firstName ?? 'Nieznane';
    final lastName = AuthService.lastName ?? '';

    return Scaffold(
      backgroundColor: AppColors.screenBackground,
      appBar: AppBar(
        title: const Text('Profil', style: TextStyles.sectionHeading),
        backgroundColor: AppColors.screenBackground,
        foregroundColor: AppColors.titleText,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
        child: Column(
          children: [
            _buildProfileItem(label: 'Imię', value: firstName),
            const SizedBox(height: 12),
            _buildProfileItem(label: 'Nazwisko', value: lastName),
            const SizedBox(height: 12),
            _buildProfileItem(label: 'E-mail', value: email),
          ],
        ),
      ),
    );
  }

  Widget _buildProfileItem({required String label, required String value}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      decoration: BoxDecoration(
        color: AppColors.cardsBackground,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          Expanded(
            flex: 2,
            child: Text(label, style: TextStyles.cardTitleHeading),
          ),
          const VerticalDivider(
            color: Colors.black26,
            thickness: 1,
            width: 24,
          ),
          Expanded(
            flex: 3,
            child: Text(
              value,
              style: TextStyles.subtitle,
              textAlign: TextAlign.right,
            ),
          ),
        ],
      ),
    );
  }
}