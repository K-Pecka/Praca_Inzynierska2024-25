import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../../features/auth/screens/start_screen.dart';
import '../theme/text_styles.dart';

class TripTitleHeader extends StatefulWidget {
  final String title;
  final String token;

  const TripTitleHeader({
    super.key,
    required this.title,
    required this.token,
  });

  @override
  State<TripTitleHeader> createState() => _TripTitleHeaderState();
}

class _TripTitleHeaderState extends State<TripTitleHeader> {
  bool _showLogout = false;

  Future<void> _logout() async {
    try {
      final response = await http.post(
        Uri.parse('https://api.plannder.com/user_auth/logout/'),
        headers: {
          'accept': '*/*',
          'Authorization': 'Bearer ${widget.token}',
        },
      );

      debugPrint('Logout status: ${response.statusCode}');
      debugPrint('Logout body: ${response.body}');

      if (!mounted) return;

      if ([200, 204, 205].contains(response.statusCode)) {
        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(builder: (_) => const StartScreen()),
              (route) => false,
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Błąd podczas wylogowywania: ${response.statusCode}')),
        );
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Błąd połączenia')),
      );
      debugPrint('Logout error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 32, left: 24, right: 24, bottom: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                widget.title,
                style: TextStyles.sectionHeading,
              ),
              GestureDetector(
                onTap: () => setState(() => _showLogout = !_showLogout),
                child: const CircleAvatar(
                  radius: 18,
                  backgroundColor: Color(0x80DEDCFF),
                  child: Text(
                    'MW',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Color(0xBF2F27CE),
                    ),
                  ),
                ),
              ),
            ],
          ),
          if (_showLogout)
            Padding(
              padding: const EdgeInsets.only(top: 8),
              child: Align(
                alignment: Alignment.centerRight,
                child: TextButton(
                  onPressed: _logout,
                  style: TextButton.styleFrom(
                    foregroundColor: Colors.red,
                  ),
                  child: const Text('Wyloguj'),
                ),
              ),
            ),
        ],
      ),
    );
  }
}