import 'package:animated_custom_dropdown/custom_dropdown.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/models/expense_model.dart';
import '../../../core/services/budget_service.dart';
import '../../../core/services/user_service.dart';
import '../../../core/theme/themes.dart';
import '../../../core/widgets/custom_expense_input_field.dart';
import '../../../core/theme/text_styles.dart';

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
    _loadUserName();
  }

  Future<void> _loadUserName() async {
    if (widget.expense.user != null) {
      try {
        final user = await UserService().fetchUserInfoByProfileId(int.parse(widget.expense.user!));
        setState(() {
          userName = '${user.firstName} ${user.lastName}';
        });
      } catch (e) {
        debugPrint("Błąd pobierania użytkownika: $e");
      }
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
              Text("Tytuł: ${widget.expense.title}", style: TextStyles.cardTitleHeading),
              const SizedBox(height: 8),
              Text("Kwota: ${widget.expense.amount.toStringAsFixed(2)} ${widget.expense.currency}", style: TextStyles.subtitle),
              const SizedBox(height: 8),
              Text("Data: ${DateFormat('dd.MM.yyyy').format(widget.expense.date)}", style: TextStyles.subtitle),
              const SizedBox(height: 8),
              Text("Kategoria: ${widget.expense.category}", style: TextStyles.subtitle),
              const SizedBox(height: 8),
              Text("Wydający: ${userName ?? 'Ładowanie...'}", style: TextStyles.subtitle),
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
                      debugPrint('Błąd usuwania: $e');
                    }
                  },
                  icon: const Icon(Icons.delete, color: Colors.white),
                  label: const Text("Usuń wydatek", style: TextStyles.whiteSubtitle),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.redAccent,
                    padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
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
          leading: const Icon(Icons.restaurant, color: Colors.black87, size: 36),
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

  final List<String> _currencies = ['PLN', 'USD', 'EUR', 'GBP'];

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
    if (!_formKey.currentState!.validate() ||
        _selectedDate == null ||
        _selectedCurrency == null) return;

    final String title = _titleController.text.trim();
    final double amount = double.parse(_amountController.text);
    final String date = DateFormat('dd.MM.yyyy').format(_selectedDate!);
    final String currency = _selectedCurrency!;

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
      );

      widget.onAdded();

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Wydatek dodany')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Błąd dodawania: $e')),
      );
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
                const Text('Dodaj wydatek', style: TextStyles.subtitle),
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

                CustomDropdown<String>(
                  items: _currencies,
                  initialItem: _selectedCurrency,
                  hintText: 'Wybierz walutę',
                  onChanged: (String? newCurrency) {
                    if (newCurrency != null) {
                      setState(() => _selectedCurrency = newCurrency);
                    }
                  },
                  decoration: CustomDropdownDecoration(
                    closedFillColor: const Color(0xFFF4F2FF),
                    closedBorder: Border.all(
                      color: Colors.black38,
                      width: 1.2,
                    ),
                    closedBorderRadius: BorderRadius.circular(16),
                    closedSuffixIcon: const Icon(
                      Icons.keyboard_arrow_down_rounded,
                    ),
                    headerStyle: TextStyles.cardTitleHeading,
                    hintStyle: TextStyles.subtitle,
                    listItemStyle: TextStyles.subtitle,
                  ),
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
