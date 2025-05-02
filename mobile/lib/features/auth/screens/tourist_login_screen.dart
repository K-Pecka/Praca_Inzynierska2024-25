import 'package:flutter/material.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/widgets/bottom_navigation_scaffold.dart';
import '../widgets/auth_widgets.dart';
import '../../../core/services/auth_service.dart';
import '../../../core/services/trip_service.dart';
import '../../../core/models/auth_response_model.dart'; // Upewnij się, że ścieżka jest poprawna

class TouristLoginScreen extends StatefulWidget {
  const TouristLoginScreen({super.key});

  @override
  State<TouristLoginScreen> createState() => _TouristLoginScreenState();
}

class _TouristLoginScreenState extends State<TouristLoginScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false;

  Future<void> _handleLogin() async {
    setState(() => _isLoading = true);
    try {
      final AuthResponseModel response = await AuthService.login(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );

      final touristProfile = response.profiles.firstWhere(
            (p) => p.type == 1,
        orElse: () => throw Exception("Nie znaleziono profilu typu turysta."),
      );

      await AuthService.setDefaultProfile(
        profileId: touristProfile.id,
        token: response.access,
      );

      final trips = await TripService.getAllTrips();
      if (trips.isEmpty) throw Exception("Brak wycieczek");

      final trip = trips.first;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => BottomNavScaffold(
            userProfileId: touristProfile.id,
            profileType: 1,
            trip: trip,
          ),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Błąd logowania: ${e.toString()}')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(height: 60),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  buildLogo(),
                  buildTitle("Logowanie: Turysta"),
                  const SizedBox(height: 24),
                  buildTouristLoginForm(
                    emailController: _emailController,
                    passwordController: _passwordController,
                    isLoading: _isLoading,
                    onLogin: _handleLogin,
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text(
                      'powrót',
                      style: TextStyles.loginReturnButton,
                    ),
                  ),
                ],
              ),
            ),
            const Spacer(),
          ],
        ),
      ),
    );
  }
}
