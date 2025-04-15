import 'package:flutter/material.dart';

Widget buildButtons({
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

Widget buildLogo() {
  return Column(
    children: [
      Image.asset(
        'assets/images/logo.png',
        height: 36,
      ),
      const SizedBox(height: 64),
    ],
  );
}

const Widget buildTitle = Text(
  'Wybierz typ profilu',
  style: TextStyle(
    fontSize: 18,
    fontFamily: 'Quicksand',
    fontWeight: FontWeight.w500,
    color: Colors.black87,
  ),
);