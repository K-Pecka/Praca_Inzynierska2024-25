import 'package:flutter/material.dart';
import '../../features/auth/screens/start_screen.dart';
import '../services/auth_service.dart';

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
    final f = AuthService.firstName?.isNotEmpty == true ? AuthService.firstName![0] : '';
    final l = AuthService.lastName?.isNotEmpty == true ? AuthService.lastName![0] : '';
    return (f + l).toUpperCase();
  }

  @override
  Widget build(BuildContext context) {
    final initials = _getInitials();
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
      ),
      body: ListView(
        children: [
          const SizedBox(height: 16),
          Center(
            child: Column(
              children: [
                CircleAvatar(
                  radius: 40,
                  backgroundColor: const Color(0x80DEDCFF),
                  child: Text(
                    initials,
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 28,
                      color: Color(0xBF2F27CE),
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  "${AuthService.firstName ?? ''} ${AuthService.lastName ?? ''}",
                  style: const TextStyle(
                    color: Colors.black87,
                    fontWeight: FontWeight.bold,
                  ),
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
            () => _logout(context),
            color: Colors.black87,
          ),
          _buildMenuItem(
            Icons.settings,
            "Ustawienia",
            () => _logout(context),
            color: Colors.black87,
          ),
          _buildMenuItem(
            Icons.report_problem,
            "Zgłoś problem",
            () => _logout(context),
            color: Colors.black87,
          ),
          _buildMenuItem(
            Icons.logout,
            "Wyloguj się",
            () => _logout(context),
            color: Colors.red,
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
      title: Text(label, style: TextStyle(color: color)),
      trailing: const Icon(Icons.chevron_right, color: Colors.white),
      onTap: onTap,
    );
  }
}
