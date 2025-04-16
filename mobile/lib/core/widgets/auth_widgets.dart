import 'package:flutter/material.dart';

Widget buildTitle(String text) {
  return Text(
    text,
    style: const TextStyle(
      fontSize: 18,
      fontFamily: 'Quicksand',
      fontWeight: FontWeight.w500,
      color: Colors.black87,
    ),
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
            style: TextStyle(
              fontFamily: 'Quicksand',
              fontSize: 16,
              fontWeight: FontWeight.w500,
              color: Colors.black,
            ),
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
            style: TextStyle(
              fontFamily: 'Quicksand',
              fontSize: 16,
              fontWeight: FontWeight.w500,
              color: Colors.black,
            ),
          ),
        ),
      ),
    ],
  );
}

Widget buildTouristLoginForm({
  required TextEditingController emailController,
  required TextEditingController passwordController,
  required bool isLoading,
  required VoidCallback onLogin,
}) {
  return Container(
    padding: const EdgeInsets.all(20),
    decoration: BoxDecoration(
      border: Border.all(color: Color(0xFFBFDFFF), width: 2),
      borderRadius: BorderRadius.circular(20),
    ),
    child: Column(
      children: [
        TextField(
          controller: emailController,
          decoration: InputDecoration(
            labelText: 'Email',
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          ),
        ),
        const SizedBox(height: 16),
        TextField(
          controller: passwordController,
          obscureText: true,
          decoration: InputDecoration(
            labelText: 'Hasło',
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          ),
        ),
        const SizedBox(height: 24),
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
              style: TextStyle(
                fontFamily: 'Quicksand',
                fontSize: 16,
                color: Colors.white,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ),
      ],
    ),
  );
}