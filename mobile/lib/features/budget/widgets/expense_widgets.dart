import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/models/expense_model.dart';
import '../../../core/services/budget_service.dart';
import '../../../core/widgets/custom_expense_input_field.dart';
import '../../../core/theme/text_styles.dart';

class ExpenseTile extends StatelessWidget {
  final ExpenseModel expense;

  const ExpenseTile({super.key, required this.expense});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFFF4F2FF),
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      margin: const EdgeInsets.only(bottom: 16),
      child: ListTile(
        leading: const Icon(Icons.restaurant, color: Colors.black87, size: 36),
        title: Text(
          expense.title,
          style: TextStyles.cardTitleHeading,
        ),
        subtitle: Text(
          DateFormat('dd.MM.yyyy').format(expense.date),
          style: TextStyles.subtitle,
        ),
        trailing: Text(
          '${expense.amount.toStringAsFixed(0)} ${expense.currency}',
          style: TextStyles.subtitle,
        ),
      ),
    );
  }
}

class ExpenseForm extends StatefulWidget {
  final String token;
  final int tripId;
  final int userProfileId;
  final VoidCallback onSaved;

  const ExpenseForm({
    super.key,
    required this.token,
    required this.tripId,
    required this.userProfileId,
    required this.onSaved,
  });

  @override
  State<ExpenseForm> createState() => _ExpenseFormState();
}

class _ExpenseFormState extends State<ExpenseForm> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _amountController = TextEditingController();
  final _noteController = TextEditingController();
  final _dateController = TextEditingController();
  DateTime? _selectedDate;

  final border = OutlineInputBorder(
    borderRadius: BorderRadius.circular(16),
    borderSide: const BorderSide(color: Color(0xFF6C55ED), width: 1.2),
  );

  Future<void> _pickDate() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      locale: const Locale('pl', 'PL'),
      firstDate: DateTime(2020),
      lastDate: DateTime(2100),
      helpText: 'Wybierz datę wydatku',
    );
    if (picked != null) {
      setState(() {
        _selectedDate = picked;
        _dateController.text = DateFormat('dd.MM.yyyy').format(picked);
      });
    }
  }

  Future<void> _submitForm() async {
    if (!_formKey.currentState!.validate() || _selectedDate == null) return;

    final String title = _titleController.text.trim();
    final double amount = double.parse(_amountController.text);
    final String date = DateFormat('yyyy-MM-dd').format(_selectedDate!);
    final String note = _noteController.text.trim();

    try {
      await BudgetService().addExpense(
        token: widget.token,
        tripId: widget.tripId,
        userProfileId: widget.userProfileId,
        title: title,
        amount: amount,
        date: date,
        note: note,
      );

      widget.onSaved();
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('Wydatek dodany')));

      _formKey.currentState!.reset();
      _titleController.clear();
      _amountController.clear();
      _noteController.clear();
      _dateController.clear();
      setState(() => _selectedDate = null);
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Błąd dodawania: \$e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Form(
        key: _formKey,
        child: Card(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          color: const Color(0xFFF4F2FF),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                const Text(
                  'Dodaj wydatek',
                  style: TextStyles.subtitle,
                ),
                const SizedBox(height: 16),
                buildInputField(
                  controller: _titleController,
                  label: 'Tytuł',
                  keyboardType: TextInputType.text,
                  style: TextStyles.cardTitleHeading,
                  border: border,
                  validator:
                      (val) =>
                          val == null || val.isEmpty ? 'Podaj tytuł' : null,
                ),
                const SizedBox(height: 12),
                buildInputField(
                  controller: _amountController,
                  label: 'Kwota',
                  keyboardType: TextInputType.number,
                  style: TextStyles.cardTitleHeading,
                  border: border,
                  validator: (val) {
                    if (val == null || val.isEmpty) return 'Podaj kwotę';
                    if (double.tryParse(val) == null) {
                      return 'Niepoprawna liczba';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 12),
                buildInputField(
                  controller: _dateController,
                  label: 'Data',
                  readOnly: true,
                  onTap: _pickDate,
                  keyboardType: TextInputType.text,
                  style: TextStyles.cardTitleHeading,
                  border: border,
                  validator:
                      (_) => _selectedDate == null ? 'Wybierz datę' : null,
                ),
                const SizedBox(height: 12),
                buildInputField(
                  controller: _noteController,
                  label: 'Notatka (opcjonalnie)',
                  keyboardType: TextInputType.text,
                  maxLines: 2,
                  style: TextStyles.cardTitleHeading,
                  border: border,
                ),
                const SizedBox(height: 16),
                Align(
                  alignment: Alignment.centerRight,
                  child: ElevatedButton(
                    onPressed: _submitForm,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF6C55ED),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: const Text(
                      'Zapisz',
                      style: TextStyles.whiteSubtitle,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
