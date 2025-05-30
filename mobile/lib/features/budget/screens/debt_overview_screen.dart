import 'package:flutter/material.dart';
import 'package:mobile/core/models/trip_model.dart';
import 'package:mobile/core/models/debt_model.dart';
import 'package:mobile/core/services/debt_service.dart';
import 'package:mobile/core/screens/base_screen.dart';
import '../widgets/debt_widgets.dart';
import 'debt_detail_screen.dart';

class DebtOverviewScreen extends StatefulWidget {
  final TripModel trip;

  const DebtOverviewScreen({super.key, required this.trip});

  @override
  State<DebtOverviewScreen> createState() => _DebtOverviewScreenState();
}

class _DebtOverviewScreenState extends State<DebtOverviewScreen> {
  List<DebtModel> _debts = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadDebts();
  }

  Future<void> _loadDebts() async {
    try {
      final debts = await DebtService.fetchDebts(tripId: widget.trip.id);
      setState(() {
        _debts = debts;
        _loading = false;
      });
    } catch (e) {
      setState(() => _loading = false);
      // Możesz dodać handleError tutaj
    }
  }

  void _showAddDebtForm() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (ctx) {
        final bottomInset = MediaQuery.of(ctx).viewInsets.bottom;
        return Padding(
          padding: EdgeInsets.only(bottom: bottomInset),
          child: DebtForm(
            trip: widget.trip,
            onAdded: () {
              Navigator.pop(ctx);
              _loadDebts();
            },
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final total = _debts.fold<double>(0.0, (sum, d) => sum + d.priceInPln);

    return _loading
        ? const Center(child: CircularProgressIndicator())
        : BaseScreen(
      trip: widget.trip,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          DebtOverviewCard(totalBudget: total, used: 0),
          const SizedBox(height: 16),
          DebtActionsRow(
            showForm: false,
            onToggleForm: _showAddDebtForm,
            onFilter: () {},
          ),
          const SizedBox(height: 24),
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _debts.length,
            itemBuilder: (context, index) {
              final debt = _debts[index];
              return DebtTile(
                debt: debt,
                trip: widget.trip,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => DebtDetailScreen(debt: debt, trip: widget.trip),
                    ),
                  ).then((_) => _loadDebts());
                },
              );
            },
          ),
        ],
      ),
    );
  }
}