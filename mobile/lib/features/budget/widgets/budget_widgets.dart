import 'package:flutter/material.dart';
import '../../../../core/theme/text_styles.dart';
import '../../../../core/theme/icons.dart';
import '../../../core/theme/themes.dart';

class BudgetOverviewCard extends StatefulWidget {
  final double totalBudget;
  final double used;

  const BudgetOverviewCard({
    super.key,
    required this.totalBudget,
    required this.used,
  });

  @override
  State<BudgetOverviewCard> createState() => _BudgetOverviewCardState();
}

class _BudgetOverviewCardState extends State<BudgetOverviewCard> {
  @override
  Widget build(BuildContext context) {
    final double percent = widget.used / widget.totalBudget;
    Color progressColor;

    if (percent <= 0.8) {
      progressColor = Colors.green;
    } else if (percent <= 1.0) {
      progressColor = Colors.amber;
    } else {
      progressColor = Colors.red;
    }

    return Column(
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
            const Text(
              'Budżet',
              style: TextStyles.cardTitleHeading,
            ),
          ],
        ),
        const SizedBox(height: 8),
        Container(
          decoration: BoxDecoration(
            color: AppColors.cardsBackground,
            borderRadius: BorderRadius.circular(20),
          ),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '${widget.totalBudget.toStringAsFixed(0)} PLN',
                style: TextStyles.totalBudgetAmount,
              ),
              const SizedBox(height: 8),
              LinearProgressIndicator(
                value: percent.clamp(0.0, 1.0),
                backgroundColor: Colors.grey[300],
                color: progressColor,
                minHeight: 6,
              ),
              const SizedBox(height: 4),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    '${widget.used.toStringAsFixed(0)} PLN',
                    style: TextStyles.usedBudget(progressColor),
                  ),
                  Text(
                    '${(percent * 100).toStringAsFixed(1)}%',
                    style: TextStyles.usedBudget(progressColor),
                  ),
                ],
              ),
            ],
          ),
        ),
      ],
    );
  }
}


class BudgetActionsRow extends StatelessWidget {
  final bool showForm;
  final VoidCallback onToggleForm;
  final VoidCallback onFilter;

  const BudgetActionsRow({
    super.key,
    required this.showForm,
    required this.onToggleForm,
    required this.onFilter,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: ElevatedButton(
            onPressed: onToggleForm,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              padding: const EdgeInsets.symmetric(vertical: 14),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            child: Text(
              showForm ? 'Anuluj' : 'Dodaj',
              style: TextStyles.whiteSubtitle,
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: ElevatedButton.icon(
            onPressed: onFilter,
            label: const Text('Filtruj', style: TextStyles.whiteSubtitle),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              padding: const EdgeInsets.symmetric(vertical: 14),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

