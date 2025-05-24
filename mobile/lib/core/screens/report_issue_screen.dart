import 'package:flutter/material.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';

class ReportIssueScreen extends StatefulWidget {
  const ReportIssueScreen({super.key});

  @override
  State<ReportIssueScreen> createState() => _ReportIssueScreenState();
}

class _ReportIssueScreenState extends State<ReportIssueScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _messageController = TextEditingController();

  void _submit() {
    if (_formKey.currentState?.validate() ?? false) {
      _titleController.clear();
      _messageController.clear();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Wysłano zgłoszenie')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.screenBackground,
      appBar: AppBar(
        title: const Text('Zgłoś problem', style: TextStyles.sectionHeading),
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
                controller: _titleController,
                decoration: const InputDecoration(labelText: 'Tytuł'),
                validator: (val) => val == null || val.isEmpty ? 'Wpisz tytuł' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _messageController,
                decoration: const InputDecoration(labelText: 'Wiadomość'),
                maxLines: 5,
                validator: (val) => val == null || val.isEmpty ? 'Wpisz wiadomość' : null,
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _submit,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 32),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('Wyślij', style: TextStyles.whiteSubtitle),
              ),
            ],
          ),
        ),
      ),
    );
  }
}