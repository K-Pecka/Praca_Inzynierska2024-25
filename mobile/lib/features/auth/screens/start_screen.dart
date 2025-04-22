import 'package:flutter/material.dart';
import '../widgets/auth_widgets.dart';
import 'login_screen.dart';

class StartScreen extends StatelessWidget {
  const StartScreen({super.key});

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
                  buildTitle("Wybierz typ profilu"),
                  const SizedBox(height: 24),
                  buildChooseProfileButtons(
                    onTouristTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const TouristLoginScreen(),
                        ),
                      );
                    },
                    onGuideTap: () {
                    },
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