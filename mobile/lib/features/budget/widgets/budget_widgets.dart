import 'package:flutter/material.dart';
import '../../../../core/theme/text_styles.dart';
import '../../../../core/theme/icons.dart';

class BudgetOverviewCard extends StatelessWidget {
  final double totalBudget;
  final double used;

  const BudgetOverviewCard({
    super.key,
    required this.totalBudget,
    required this.used,
  });

  @override
  Widget build(BuildContext context) {
    final double percent = (used / totalBudget).clamp(0, 1);

    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFFF4F2FF),
        borderRadius: BorderRadius.circular(20),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              ColorFiltered(
                colorFilter: const ColorFilter.mode(Color(0xFF6C55ED), BlendMode.srcIn),
                child: SizedBox(width: 32, height: 32, child: AppIcons.money),
              ),
              const SizedBox(width: 8),
              const Text(
                'Budżet',
                style: TextStyles.cardTitleHeading,
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            '${totalBudget.toStringAsFixed(0)} PLN',
            style: TextStyles.totalBudgetAmount,
          ),
          const SizedBox(height: 8),
          LinearProgressIndicator(
            value: percent,
            backgroundColor: Colors.grey[300],
            color: Colors.green,
            minHeight: 6,
          ),
          const SizedBox(height: 4),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '${used.toStringAsFixed(0)} PLN',
                style: TextStyles.usedBudget,
              ),
              Text(
                '${(percent * 100).toStringAsFixed(1)}%',
                style: TextStyles.usedBudget,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class ToggleExpenseFormButton extends StatelessWidget {
  final bool showForm;
  final VoidCallback onToggle;

  const ToggleExpenseFormButton({
    super.key,
    required this.showForm,
    required this.onToggle,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: IconButton(
        icon: Icon(
          showForm ? Icons.remove_circle_outline : Icons.add_circle_outline,
          size: 48,
          color: const Color(0xFF6C55ED),
        ),
        onPressed: onToggle,
      ),
    );
  }
}

