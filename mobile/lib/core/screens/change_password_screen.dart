import 'package:flutter/material.dart';
import '../../../core/services/auth_service.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';
import '../../../core/utils/error_handler.dart';

class ChangePasswordScreen extends StatefulWidget {
  const ChangePasswordScreen({super.key});

  @override
  State<ChangePasswordScreen> createState() => _ChangePasswordScreenState();
}

class _ChangePasswordScreenState extends State<ChangePasswordScreen> {
  final _formKey = GlobalKey<FormState>();
  final _passwordController = TextEditingController();
  final _confirmController = TextEditingController();

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    try {
      await AuthService.changePassword(
        newPassword: _passwordController.text.trim(),
        confirmPassword: _confirmController.text.trim(),
      );

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Hasło zostało zmienione")),
      );

      _formKey.currentState?.reset();
      _passwordController.clear();
      _confirmController.clear();
    } catch (e) {
      handleError(context, e, userMessage: "Nie udało się zmienić hasła");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.screenBackground,
      appBar: AppBar(
        title: const Text('Zmień hasło', style: TextStyles.sectionHeading),
        backgroundColor: AppColors.screenBackground,
        foregroundColor: AppColors.titleText,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _passwordController,
                obscureText: true,
                decoration: const InputDecoration(labelText: 'Nowe hasło'),
                validator: (val) =>
                val != null && val.length >= 6 ? null : 'Minimum 6 znaków',
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _confirmController,
                obscureText: true,
                decoration: const InputDecoration(labelText: 'Powtórz hasło'),
                validator: (val) => val == _passwordController.text
                    ? null
                    : 'Hasła się nie zgadzają',
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _submit,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text("Zmień hasło", style: TextStyles.whiteSubtitle),
              ),
            ],
          ),
        ),
      ),
    );
  }
}