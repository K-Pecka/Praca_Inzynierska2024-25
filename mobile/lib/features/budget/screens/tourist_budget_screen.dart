import 'package:flutter/material.dart';
import '../../../../core/models/expense_model.dart';
import '../../../../core/services/budget_service.dart';
import '../../../core/widgets/title_header.dart';
import '../widgets/expense_widgets.dart';
import '../widgets/budget_widgets.dart';
import '../../../../core/widgets/base_screen.dart';

class TouristBudgetScreen extends StatefulWidget {
  final String token;
  final int tripId;
  final int userProfileId;

  const TouristBudgetScreen({
    super.key,
    required this.token,
    required this.tripId,
    required this.userProfileId,
  });

  @override
  State<TouristBudgetScreen> createState() => _TouristBudgetScreenState();
}

class _TouristBudgetScreenState extends State<TouristBudgetScreen> {
  List<ExpenseModel> _expenses = [];
  bool _loading = true;
  bool _showForm = false;

  @override
  void initState() {
    super.initState();
    _loadExpenses();
  }

  Future<void> _loadExpenses() async {
    final data = await BudgetService().fetchExpenses(
      tripId: widget.tripId,
      token: widget.token,
    );
    setState(() {
      _expenses = data;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final double totalBudget = 5000.0;
    final double used = _expenses.fold(0, (sum, e) => sum + e.amount);

    return Scaffold(
      resizeToAvoidBottomInset: true,
      backgroundColor: Colors.white,
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : BaseScreen(
        title: 'Majówka we Francji',
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            BudgetOverviewCard(totalBudget: totalBudget, used: used),
            const SizedBox(height: 16),
            ToggleExpenseFormButton(
              showForm: _showForm,
              onToggle: () =>
                  setState(() => _showForm = !_showForm),
            ),
            const SizedBox(height: 16),
            if (_showForm)
              ExpenseForm(
                token: widget.token,
                tripId: widget.tripId,
                userProfileId: widget.userProfileId,
                onSaved: _loadExpenses,
              ),
            const SizedBox(height: 24),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _expenses.length,
              itemBuilder: (context, index) {
                return ExpenseTile(expense: _expenses[index]);
              },
            ),
          ],
        ),
      ),
    );
  }
}
