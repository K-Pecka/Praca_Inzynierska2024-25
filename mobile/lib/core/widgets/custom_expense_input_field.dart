import 'package:flutter/material.dart';

import '../theme/text_styles.dart';

Widget buildInputField({
  required TextEditingController controller,
  required String label,
  required TextInputType keyboardType,
  required TextStyle style,
  required OutlineInputBorder border,
  String? Function(String?)? validator,
  VoidCallback? onTap,
  bool readOnly = false,
  int maxLines = 1,
}) {
  return TextFormField(
    controller: controller,
    readOnly: readOnly,
    keyboardType: keyboardType,
    style: style,
    maxLines: maxLines,
    onTap: onTap,
    decoration: InputDecoration(
      labelText: label,
      labelStyle: TextStyles.textHint,
      border: border,
      focusedBorder: border,
    ),
    validator: validator,
  );
}