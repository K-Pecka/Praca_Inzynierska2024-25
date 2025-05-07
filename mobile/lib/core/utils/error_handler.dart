import 'package:flutter/material.dart';
import 'package:mobile/core/theme/themes.dart';

import '../theme/text_styles.dart';

void handleError(BuildContext context, Object error, {String? userMessage}) {
  debugPrint('Błąd: $error');

  if (!context.mounted) return;

  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text(
        userMessage ?? 'Coś poszło nie tak. Spróbuj ponownie.',
        style: TextStyles.errorMessage,
      ),
      backgroundColor: AppColors.errorBackground,
    ),
  );
}
