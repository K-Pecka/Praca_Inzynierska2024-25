import 'package:flutter/material.dart';
import '../../../../core/models/expense_model.dart';
import '../../../../core/services/budget_service.dart';
import '../../../../core/models/trip_model.dart';
import '../widgets/expense_widgets.dart';
import '../widgets/budget_widgets.dart';
import '../../../../core/widgets/base_screen.dart';

class BudgetScreen extends StatefulWidget {
  final TripModel trip;
  final int userProfileId;

  const BudgetScreen({
    super.key,
    required this.trip,
    required this.userProfileId,
  });

  @override
  State<BudgetScreen> createState() => _BudgetScreenState();
}

class _BudgetScreenState extends State<BudgetScreen> {
  List<ExpenseModel> _expenses = [];
  double _used = 0.0;
  bool _loading = true;
  bool _showForm = false;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    final data = await BudgetService.fetchExpenses(
      tripId: widget.trip.id,
    );
    final used = await _calculateUsedInPLN(data);

    setState(() {
      data.sort((a, b) {
        int dateComparison = b.date.compareTo(a.date);
        if (dateComparison != 0) {
          return dateComparison;
        } else {
          return b.id.compareTo(a.id);
        }
      });
      _expenses = data;
      _used = used;
      _loading = false;
    });
  }

  Future<double> _calculateUsedInPLN(List<ExpenseModel> expenses) async {
    double total = 0.0;
    final Map<String, double> rateCache = {};

    for (final e in expenses) {
      if (e.currency == 'PLN') {
        total += e.amount;
      } else {
        if (!rateCache.containsKey(e.currency)) {
          final rate = await BudgetService.getExchangeRate(
            from: e.currency,
            to: 'PLN',
          );
          rateCache[e.currency] = rate;
        }
        total += e.amount * rateCache[e.currency]!;
      }
    }

    return total;
  }

  @override
  Widget build(BuildContext context) {
    const double totalBudget = 5000.0;

    return Scaffold(
      resizeToAvoidBottomInset: true,
      backgroundColor: Colors.white,
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : BaseScreen(
        trip: widget.trip,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            BudgetOverviewCard(totalBudget: totalBudget, used: _used),
            const SizedBox(height: 16),
            ToggleExpenseFormButton(
              showForm: _showForm,
              onToggle: () => setState(() => _showForm = !_showForm),
            ),
            const SizedBox(height: 16),
            if (_showForm)
              ExpenseForm(
                tripId: widget.trip.id,
                userProfileId: widget.userProfileId,
                onSaved: () {
                  setState(() => _showForm = false);
                },
                onAdded: _loadData,
              ),
            const SizedBox(height: 24),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _expenses.length,
              itemBuilder: (context, index) {
                return Builder(
                  builder: (scaffoldContext) {
                    return ExpenseTile(
                      expense: _expenses[index],
                      tripId: widget.trip.id,
                      scaffoldContext: scaffoldContext,
                      onDeleted: () {
                        _loadData();
                      },
                    );
                  },
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}



