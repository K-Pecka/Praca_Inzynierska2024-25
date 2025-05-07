import 'package:flutter/material.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/utils/error_handler.dart';
import '../../../core/widgets/bottom_navigation_scaffold.dart';
import '../widgets/auth_widgets.dart';
import '../../../core/services/auth_service.dart';
import '../../../core/services/trip_service.dart';
import '../../../core/models/auth_response_model.dart';

class LoginScreen extends StatefulWidget {
  final int profileType;
  final String title;
  final Color borderColor;

  const LoginScreen({
    super.key,
    required this.profileType,
    required this.title,
    required this.borderColor,
  });

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
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

      final profile = response.profiles.firstWhere(
            (p) => p.type == widget.profileType,
        orElse: () => throw Exception("Nie znaleziono profilu."),
      );

      await AuthService.setDefaultProfile(
        profileId: profile.id,
        token: response.access,
      );

      final trips = await TripService.getAllTrips();
      if (trips.isEmpty) throw Exception("Brak wycieczek");

      final trip = trips.first;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => BottomNavScaffold(
            userProfileId: profile.id,
            profileType: widget.profileType,
            trip: trip,
          ),
        ),
      );
    } catch (e) {
      if (mounted) {
        handleError(context, e, userMessage: 'Błąd logowania. Spróbuj ponownie.');
      }
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
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
                  buildTitle(widget.title),
                  const SizedBox(height: 24),
                  buildLoginForm(
                    emailController: _emailController,
                    passwordController: _passwordController,
                    isLoading: _isLoading,
                    onLogin: _handleLogin,
                    borderColor: widget.borderColor,
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
