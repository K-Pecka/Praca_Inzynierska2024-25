import 'package:flutter/material.dart';

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
      labelStyle: const TextStyle(
        color: Colors.black38,
        fontWeight: FontWeight.w600,
        fontSize: 18,
      ),
      border: border,
      focusedBorder: border,
    ),
    validator: validator,
  );
}