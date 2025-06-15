import 'package:flutter/material.dart';

import '../../../core/theme/text_styles.dart';

Widget buildTitle(String text) {
  return Text(
    text,
    style: TextStyles.loginTitleHeading ,
  );
}

Widget buildLogo() {
  return Column(
    children: [
      Image.asset('assets/images/logo.png', height: 36),
      const SizedBox(height: 64),
    ],
  );
}

Widget buildChooseProfileButtons({
  required VoidCallback onTouristTap,
  required VoidCallback onGuideTap,
}) {
  return Column(
    children: [
      SizedBox(
        width: double.infinity,
        child: OutlinedButton(
          onPressed: onTouristTap,
          style: OutlinedButton.styleFrom(
            side: const BorderSide(color: Color(0xFFBFDFFF), width: 2),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 24),
          ),
          child: const Text(
            'Turysta',
            style: TextStyles.subtitle,
          ),
        ),
      ),
      const SizedBox(height: 16),
      SizedBox(
        width: double.infinity,
        child: OutlinedButton(
          onPressed: onGuideTap,
          style: OutlinedButton.styleFrom(
            side: const BorderSide(color: Color(0xFFA8E6B5), width: 2),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 24),
          ),
          child: const Text(
            'Przewodnik',
              style: TextStyles.subtitle,
          ),
        ),
      ),
    ],
  );
}

Widget buildLoginForm({
  required TextEditingController emailController,
  required TextEditingController passwordController,
  required bool isLoading,
  required VoidCallback onLogin,
  required Color borderColor,
}) {
  return Container(
    padding: const EdgeInsets.all(20),
    decoration: BoxDecoration(
      border: Border.all(color: borderColor, width: 2),
      borderRadius: BorderRadius.circular(20),
    ),
    child: Column(
      children: [
        // Email
        TextField(
          controller: emailController,
          style: TextStyles.subtitle,
          decoration: InputDecoration(
            labelText: 'Email',
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            labelStyle: TextStyles.subtitle,
            prefixIcon: const Icon(Icons.email_outlined),
          ),
        ),
        const SizedBox(height: 16),

        // Hasło
        TextField(
          controller: passwordController,
          obscureText: true,
          style: TextStyles.subtitle,
          decoration: InputDecoration(
            labelText: 'Hasło',
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            labelStyle: TextStyles.subtitle,
            prefixIcon: const Icon(Icons.lock_outline),
          ),
          onSubmitted: (_) => onLogin(),
        ),
        const SizedBox(height: 24),

        // Przycisk logowania
        SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            onPressed: isLoading ? null : onLogin,
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF2D1ED6),
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
            ),
            child: isLoading
                ? const CircularProgressIndicator(color: Colors.white)
                : const Text(
              'Zaloguj',
              style: TextStyles.whiteSubtitle,
            ),
          ),
        ),
      ],
    ),
  );
}
