import 'package:flutter/material.dart';
import 'package:mobile/core/models/trip_model.dart';
import 'package:mobile/core/models/debt_model.dart';
import 'package:mobile/core/services/debt_service.dart';
import 'package:mobile/core/screens/base_screen.dart';
import 'package:mobile/core/theme/themes.dart';
import '../../../core/theme/text_styles.dart';
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

  String _sortOption = 'Kwota malejąco';

  final List<String> _sortOptions = [
    'Kwota malejąco',
    'Kwota rosnąco',
  ];

  void _applySorting() {
    setState(() {
      switch (_sortOption) {
        case 'Kwota rosnąco':
          _debts.sort((a, b) => a.priceInPln.compareTo(b.priceInPln));
          break;
        case 'Kwota malejąco':
        default:
          _debts.sort((a, b) => b.priceInPln.compareTo(a.priceInPln));
      }
    });
  }

  Future<void> _loadDebts() async {
    try {
      final debts = await DebtService.fetchDebts(tripId: widget.trip.id);
      setState(() {
        _debts = debts;
        _loading = false;
      });
      _applySorting();
    } catch (e) {
      setState(() => _loading = false);
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
            onFilter: _showFilterDialog,
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
                child: Text('Filtruj długi', style:  TextStyles.cardTitleHeading),
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

              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pop(context);
                    _applySorting();
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
}