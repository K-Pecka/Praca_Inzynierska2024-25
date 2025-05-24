import 'package:flutter/material.dart';
import '../../../../core/models/expense_model.dart';
import '../../../../core/services/budget_service.dart';
import '../../../../core/models/trip_model.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';
import '../widgets/expense_widgets.dart';
import '../widgets/budget_widgets.dart';
import '../../../core/screens/base_screen.dart';

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
  String _sortOption = 'Data malejąco';
  int _userFilterIndex = 0;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  List<Map<String, dynamic>> get _memberOptions {
    return [
      {'id': null, 'fullName': 'Wszyscy'},
      ...[widget.trip.creator, ...widget.trip.members].map((m) => {
        'id': m.id,
        'fullName': '${m.firstName ?? ''} ${m.lastName ?? ''}'.trim(),
      }),
    ];
  }

  int? get _selectedUserId => _memberOptions[_userFilterIndex]['id'];
  String get _selectedUserLabel => _memberOptions[_userFilterIndex]['fullName'];

  final List<String> _sortOptions = [
    'Data malejąco',
    'Data rosnąco',
    'Kwota malejąco',
    'Kwota rosnąco',
  ];

  void _showExpenseFormModal(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (ctx) => Padding(
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(ctx).viewInsets.bottom,
          top: 24,
          left: 24,
          right: 24,
        ),
        child: ExpenseForm(
          tripId: widget.trip.id,
          userProfileId: widget.userProfileId,
          onSaved: () => Navigator.pop(ctx),
          onAdded: _loadData,
        ),
      ),
    );
  }

  void _showFilterDialog() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.fromLTRB(24, 24, 24, 0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Center(
                child: Text('Filtruj wydatki', style: TextStyles.cardTitleHeading),
              ),
              const SizedBox(height: 24),

              const Text('Sortuj po:', style: TextStyles.subtitle),
              const SizedBox(height: 8),
              StatefulBuilder(
                builder: (context, setModalState) {
                  return SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () {
                        setState(() {
                          final currentIndex = _sortOptions.indexOf(_sortOption);
                          _sortOption = _sortOptions[(currentIndex + 1) % _sortOptions.length];
                        });
                        setModalState(() {});
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: Text(_sortOption, style: TextStyles.whiteSubtitle),
                    ),
                  );
                },
              ),

              const SizedBox(height: 16),
              const Text('Uczestnik:', style: TextStyles.subtitle),
              const SizedBox(height: 8),
              StatefulBuilder(
                builder: (context, setModalState) {
                  return SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () {
                        setState(() {
                          _userFilterIndex = (_userFilterIndex + 1) % _memberOptions.length;
                        });
                        setModalState(() {});
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: Text(_selectedUserLabel, style: TextStyles.whiteSubtitle),
                    ),
                  );
                },
              ),

              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pop(context);
                    _loadData();
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text('Zastosuj filtry', style: TextStyles.whiteSubtitle),
                ),
              ),
              const SizedBox(height: 20),
              SizedBox(height: MediaQuery.of(context).viewInsets.bottom + 24),
            ],
          ),
        );
      },
    );
  }

  Future<void> _loadData() async {
    var data = await BudgetService.fetchExpenses(tripId: widget.trip.id);
    final used = _calculateUsedInPLN(data);

    setState(() {
      final selectedId = _selectedUserId;
      if (selectedId != null) {
        data = data.where((e) => e.user == selectedId).toList();
      }

      switch (_sortOption) {
        case 'Data rosnąco':
          data.sort((a, b) => a.date.compareTo(b.date));
          break;
        case 'Kwota malejąco':
          data.sort((a, b) => b.convertedAmount.compareTo(a.convertedAmount));
          break;
        case 'Kwota rosnąco':
          data.sort((a, b) => a.convertedAmount.compareTo(b.convertedAmount));
          break;
        case 'Data malejąco':
        default:
          data.sort((a, b) {
            int dateComp = b.date.compareTo(a.date);
            return dateComp != 0 ? dateComp : b.id.compareTo(a.id);
          });
      }

      _expenses = data;
      _used = used;
      _loading = false;
    });
  }

  double _calculateUsedInPLN(List<ExpenseModel> expenses) {
    return expenses.fold(0.0, (sum, e) => sum + e.convertedAmount);
  }

  @override
  Widget build(BuildContext context) {
    final totalBudget =
    widget.trip.budgetAmount != 0.0 ? widget.trip.budgetAmount : 5000.0;
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
            BudgetActionsRow(
              showForm: false,
              onToggleForm: () => _showExpenseFormModal(context),
              onFilter: _showFilterDialog,
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
                      onDeleted: _loadData,
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
