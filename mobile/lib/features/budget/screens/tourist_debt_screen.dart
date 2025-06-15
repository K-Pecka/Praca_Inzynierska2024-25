import 'package:flutter/material.dart';
import 'package:mobile/core/models/trip_model.dart';
import 'package:mobile/core/models/debt_model.dart';
import 'package:mobile/core/services/debt_service.dart';
import 'package:mobile/core/screens/base_screen.dart';
import 'package:mobile/core/theme/text_styles.dart';
import 'package:mobile/core/theme/themes.dart';
import 'package:mobile/core/theme/icons.dart';

class TouristDebtScreen extends StatefulWidget {
  final TripModel trip;
  final int userProfileId;

  const TouristDebtScreen({
    super.key,
    required this.trip,
    required this.userProfileId,
  });

  @override
  State<TouristDebtScreen> createState() => _TouristDebtScreenState();
}

class _TouristDebtScreenState extends State<TouristDebtScreen> {
  List<DebtModel> _userDebts = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadUserDebts();
  }

  Future<void> _loadUserDebts() async {
    final allDebts = await DebtService.fetchDebts(tripId: widget.trip.id);
    final filtered = allDebts
        .where((d) => d.members.any((m) => m.id == widget.userProfileId))
        .toList();

    setState(() {
      _userDebts = filtered;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final total = _userDebts.fold<double>(0.0, (sum, d) => sum + d.pricePerMemberInPln);

    return _loading
        ? const Center(child: CircularProgressIndicator())
        : BaseScreen(
      trip: widget.trip,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              ColorFiltered(
                colorFilter: const ColorFilter.mode(
                  AppColors.primary,
                  BlendMode.srcIn,
                ),
                child: SizedBox(width: 36, height: 36, child: AppIcons.money),
              ),
              const SizedBox(width: 8),
              const Text('Zaległości', style: TextStyles.cardTitleHeading),
            ],
          ),
          const SizedBox(height: 12),
          Container(
            width: double.infinity,
            decoration: BoxDecoration(
              color: AppColors.cardsBackground,
              borderRadius: BorderRadius.circular(20),
            ),
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Łączna kwota do spłaty:', style: TextStyles.cardTitleHeading),
                const SizedBox(height: 8),
                Text('${total.toStringAsFixed(2)} PLN', style: TextStyles.sectionHeading),
              ],
            ),
          ),
          const SizedBox(height: 16),
          const Text('Długi:', style: TextStyles.cardTitleHeading),
          const SizedBox(height: 16),
          _userDebts.isEmpty
              ? const Text('Brak zaległości', style: TextStyles.subtitle)
              : ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _userDebts.length,
            itemBuilder: (context, index) {
              final d = _userDebts[index];
              return Card(
                color: AppColors.cardsBackground,
                elevation: 0,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  title: Text(d.name, style: TextStyles.cardTitleHeading),
                  subtitle: Text(
                    '${d.pricePerMemberInPln.toStringAsFixed(2)} PLN',
                    style: TextStyles.subtitle,
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}