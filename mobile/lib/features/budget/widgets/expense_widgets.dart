import 'package:animated_custom_dropdown/custom_dropdown.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:mobile/core/models/expense_model.dart';
import 'package:mobile/core/services/budget_service.dart';
import 'package:mobile/core/theme/icons.dart';
import 'package:mobile/core/theme/themes.dart';
import 'package:mobile/core/widgets/custom_expense_input_field.dart';
import 'package:mobile/core/theme/text_styles.dart';
import 'package:mobile/core/utils/error_handler.dart';

class ExpenseTile extends StatefulWidget {
  final ExpenseModel expense;
  final int tripId;
  final VoidCallback onDeleted;
  final BuildContext scaffoldContext;

  const ExpenseTile({
    super.key,
    required this.expense,
    required this.tripId,
    required this.onDeleted,
    required this.scaffoldContext,
  });

  @override
  State<ExpenseTile> createState() => _ExpenseTileState();
}

class _ExpenseTileState extends State<ExpenseTile> {
  String? userName;

  @override
  void initState() {
    super.initState();
  }

  Widget _getCategoryIcon(String category) {
    switch (category) {
      case '1':
        return ExpenseIcons.food;
      case '2':
        return ExpenseIcons.transport;
      case '3':
        return ExpenseIcons.attraction;
      case '4':
        return ExpenseIcons.other;
      default:
        return ExpenseIcons.other;
    }
  }

  void _showExpenseDetails(BuildContext modalContext) {
    showModalBottomSheet(
      context: modalContext,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      isScrollControlled: true,
      builder: (modalCtx) {
        return Padding(
          padding: const EdgeInsets.fromLTRB(24, 24, 24, 32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: Colors.grey[400],
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Text(
                "Tytuł: ${widget.expense.title}",
                style: TextStyles.cardTitleHeading,
              ),
              const SizedBox(height: 8),
              Text(
                "Kwota: ${widget.expense.amount.toStringAsFixed(2)} ${widget.expense.currency}",
                style: TextStyles.subtitle,
              ),
              if (widget.expense.currency != 'PLN')
                const SizedBox(height: 8),
                Text(
                  "Kwota w PLN: ${widget.expense.convertedAmount.toStringAsFixed(2)} PLN",
                  style: TextStyles.subtitle,
                ),
              const SizedBox(height: 8),
              Text(
                "Data: ${DateFormat('dd.MM.yyyy').format(widget.expense.date)}",
                style: TextStyles.subtitle,
              ),
              const SizedBox(height: 8),
              Text(
                "Kategoria: ${widget.expense.category}",
                style: TextStyles.subtitle,
              ),
              const SizedBox(height: 8),
              Text(
                "Wydający: ${widget.expense.username}",
                style: TextStyles.subtitle,
              ),
              const SizedBox(height: 24),
              Center(
                child: ElevatedButton.icon(
                  onPressed: () async {
                    Navigator.of(modalContext).pop();
                    try {
                      await BudgetService.deleteExpense(
                        tripId: widget.tripId,
                        expenseId: widget.expense.id,
                      );
                      widget.onDeleted();
                    } catch (e) {
                      handleError(context, e, userMessage: 'Nie udało się usunąć wydatku.');
                    }
                  },
                  icon: const Icon(Icons.delete, color: Colors.white),
                  label: const Text(
                    "Usuń wydatek",
                    style: TextStyles.whiteSubtitle,
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.redAccent,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 32,
                      vertical: 12,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.cardsBackground,
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: () => _showExpenseDetails(context),
        child: ListTile(
          leading: SizedBox(
            height: 36,
            width: 36,
            child: ColorFiltered(
              colorFilter: const ColorFilter.mode(
                AppColors.titleText,
                BlendMode.srcIn,
              ),
              child: _getCategoryIcon(widget.expense.category),
            ),
          ),
          title: Text(widget.expense.title, style: TextStyles.cardTitleHeading),
          subtitle: Text(
            DateFormat('dd.MM.yyyy').format(widget.expense.date),
            style: TextStyles.subtitle,
          ),
          trailing: Text(
            '${widget.expense.amount.toStringAsFixed(0)} ${widget.expense.currency}',
            style: TextStyles.subtitle,
          ),
        ),
      ),
    );
  }
}

class ExpenseForm extends StatefulWidget {
  final int tripId;
  final int userProfileId;
  final VoidCallback onSaved;
  final VoidCallback onAdded;

  const ExpenseForm({
    super.key,
    required this.tripId,
    required this.userProfileId,
    required this.onSaved,
    required this.onAdded,
  });

  @override
  State<ExpenseForm> createState() => _ExpenseFormState();
}

class _ExpenseFormState extends State<ExpenseForm> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _amountController = TextEditingController();
  final _dateController = TextEditingController();
  DateTime? _selectedDate;
  String? _selectedCurrency = 'PLN';
  String? _selectedCategoryLabel = 'Jedzenie';

  final List<String> _currencies = ['PLN', 'USD', 'EUR', 'GBP'];
  final List<String> _categoryLabels = ['Jedzenie', 'Transport', 'Atrakcja', 'Inne'];

  final border = OutlineInputBorder(
    borderRadius: BorderRadius.circular(16),
    borderSide: const BorderSide(color: Color(0xFF6C55ED), width: 1.2),
  );

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
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

    final title = _titleController.text.trim();
    final amount = double.parse(_amountController.text);
    final date = DateFormat('dd.MM.yyyy').format(_selectedDate!);
    final currency = _selectedCurrency!;
    final category = (_categoryLabels.indexOf(_selectedCategoryLabel!) + 1).toString();

    widget.onSaved();

    try {
      await BudgetService.addExpense(
        tripId: widget.tripId,
        userProfileId: widget.userProfileId,
        title: title,
        amount: amount,
        currency: currency,
        date: date,
        note: '',
        category: category,
      );
      widget.onAdded();
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Wydatek dodany')));
    } catch (e) {
      handleError(context, e, userMessage: 'Nie udało się dodać elementu.');
    }

    _formKey.currentState!.reset();
    _titleController.clear();
    _amountController.clear();
    _dateController.clear();
    setState(() {
      _selectedDate = null;
      _selectedCurrency = 'PLN';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
      child: SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Center(child: Text('Dodaj wydatek', style: TextStyles.cardTitleHeading)),
                const SizedBox(height: 16),

                buildInputField(
                  controller: _titleController,
                  label: 'Tytuł',
                  keyboardType: TextInputType.text,
                  style: TextStyles.cardTitleHeading,
                  border: border,
                  validator: (val) => val == null || val.isEmpty ? 'Podaj tytuł' : null,
                ),

                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(
                      child: buildInputField(
                        controller: _amountController,
                        label: 'Kwota',
                        keyboardType: TextInputType.number,
                        style: TextStyles.cardTitleHeading,
                        border: border,
                        validator: (val) {
                          if (val == null || val.isEmpty) return 'Podaj kwotę';
                          if (double.tryParse(val) == null) return 'Niepoprawna liczba';
                          return null;
                        },
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: CustomDropdown<String>(
                        items: _currencies,
                        initialItem: _selectedCurrency,
                        onChanged: (val) => setState(() => _selectedCurrency = val),
                        decoration: CustomDropdownDecoration(
                          closedFillColor: AppColors.cardsBackground,
                          closedBorder: Border.all(color: Colors.black38, width: 1.2),
                          closedBorderRadius: BorderRadius.circular(16),
                          closedSuffixIcon: const Icon(Icons.keyboard_arrow_down_rounded),
                          headerStyle: TextStyles.cardTitleHeading,
                          listItemStyle: TextStyles.subtitle
                        ),
                      ),
                    ),
                  ],
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
                  validator: (_) => _selectedDate == null ? 'Wybierz datę' : null,
                ),

                const SizedBox(height: 12),
                CustomDropdown<String>(
                  items: _categoryLabels,
                  initialItem: _selectedCategoryLabel,
                  onChanged: (val) => setState(() => _selectedCategoryLabel = val),
                  decoration: CustomDropdownDecoration(
                    closedFillColor: AppColors.cardsBackground,
                    closedBorder: Border.all(color: Colors.black38, width: 1.2),
                    closedBorderRadius: BorderRadius.circular(16),
                    closedSuffixIcon: const Icon(Icons.keyboard_arrow_down_rounded),
                    headerStyle: TextStyles.cardTitleHeading,
                      listItemStyle: TextStyles.subtitle
                  ),
                ),

                const SizedBox(height: 20),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _submitForm,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF6C55ED),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                    child: const Text('Zapisz', style: TextStyles.whiteSubtitle),
                  ),
                ),
                SizedBox(height: MediaQuery.of(context).viewInsets.bottom + 24),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
