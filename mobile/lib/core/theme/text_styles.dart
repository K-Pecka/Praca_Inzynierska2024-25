import 'package:flutter/material.dart';
import 'package:mobile/core/theme/themes.dart';

class TextStyles {
  static const loginTitleHeading = TextStyle(
    fontSize: 26,
    fontWeight: FontWeight.w600,
    color: Colors.black87,
  );

  static const loginReturnButton = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: Color(0xFF7C4DFF),
  );

  static const sectionHeading = TextStyle(
    fontSize: 22,
    fontWeight: FontWeight.w600,
    color: Colors.black87,
  );

  static const cardTitleHeading = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: Colors.black87,
  );

  static const subtitle = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: Colors.black54,
  );

  static const subtitle18Light = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: Colors.black38,
  );

  static const whiteSubtitle = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: Colors.white,
  );

  static const totalBudgetAmount = TextStyle(
    fontSize: 20,
    fontWeight: FontWeight.w600,
    color: Colors.black87,
  );

  static TextStyle usedBudget(Color color) {
    return TextStyle(color: color, fontSize: 18, fontWeight: FontWeight.w600);
  }

  static const TextStyle textHint = TextStyle(
    color: Colors.black38,
    fontWeight: FontWeight.w600,
    fontSize: 18,
  );

  static const TextStyle initials = TextStyle(
    fontWeight: FontWeight.bold,
    fontSize: 18,
    color: AppColors.primary,
  );

  static const TextStyle menuInitials = TextStyle(
    fontWeight: FontWeight.bold,
    fontSize: 24,
    color: AppColors.primary,
  );

  static const TextStyle errorMessage = TextStyle(
    fontWeight: FontWeight.bold,
    fontSize: 18,
    color: Colors.white,
  );
}
