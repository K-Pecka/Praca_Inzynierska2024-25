import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '/core/models/itinerary_model.dart';
import '/core/models/activity_model.dart';
import '/core/theme/text_styles.dart';
import '/core/theme/icons.dart';
import 'package:animated_custom_dropdown/custom_dropdown.dart';

class DaySelector extends StatefulWidget {
  final DateTime start;
  final DateTime end;
  final List<ItineraryModel> activeDays;
  final DateTime selected;
  final ValueChanged<DateTime> onSelect;

  const DaySelector({
    super.key,
    required this.start,
    required this.end,
    required this.activeDays,
    required this.selected,
    required this.onSelect,
  });

  @override
  State<DaySelector> createState() => _DaySelectorState();
}

class _DaySelectorState extends State<DaySelector> {
  final _scrollController = ScrollController();

  List<DateTime> _generateVisibleDays() {
    return List.generate(5, (i) => widget.selected.add(Duration(days: i - 2)));
  }

  bool _isSameDay(DateTime a, DateTime b) =>
      a.year == b.year && a.month == b.month && a.day == b.day;

  bool _isInPlan(DateTime day) {
    final start = DateTime(
      widget.start.year,
      widget.start.month,
      widget.start.day,
    );
    final end = DateTime(widget.end.year, widget.end.month, widget.end.day);
    final d = DateTime(day.year, day.month, day.day);
    return !d.isBefore(start) && !d.isAfter(end);
  }

  bool _isActive(DateTime day) {
    final d = DateTime(day.year, day.month, day.day);
    return widget.activeDays.any((it) {
      final s = DateTime(
        it.startDate.year,
        it.startDate.month,
        it.startDate.day,
      );
      final e = DateTime(it.endDate.year, it.endDate.month, it.endDate.day);
      return !d.isBefore(s) && !d.isAfter(e);
    });
  }

  @override
  void didUpdateWidget(covariant DaySelector oldWidget) {
    super.didUpdateWidget(oldWidget);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final index = 2;
      final offset =
          (index * 64.0) - MediaQuery.of(context).size.width / 2 + 32;
      _scrollController.animateTo(
        offset.clamp(0, _scrollController.position.maxScrollExtent),
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    final days = _generateVisibleDays();

    return SizedBox(
      height: 64,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: ListView.separated(
          controller: _scrollController,
          scrollDirection: Axis.horizontal,
          itemCount: days.length,
          separatorBuilder: (_, __) => const SizedBox(width: 8),
          itemBuilder: (context, index) {
            final date = days[index];
            final isSelected = _isSameDay(date, widget.selected);
            final isInPlan = _isInPlan(date);
            final isActive = _isActive(date);

            final bgColor =
                isSelected
                    ? const Color(0xBF2F27CE)
                    : isInPlan && isActive
                    ? const Color(0x90DEDCFF)
                    : const Color(0x40000000);

            return GestureDetector(
              onTap: () => widget.onSelect(date),
              child: Container(
                width: 56,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: bgColor,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  DateFormat('d').format(date),
                  style: TextStyles.cardTitleHeading,
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class ActivitiesList extends StatelessWidget {
  final List<ActivityModel> activities;

  const ActivitiesList({super.key, required this.activities});

  @override
  Widget build(BuildContext context) {
    if (activities.isEmpty) {
      return const Center(child: Text('Brak aktywności na ten dzień'));
    }

    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: activities.length,
      itemBuilder: (context, index) {
        final a = activities[index];
        return Container(
          margin: const EdgeInsets.only(bottom: 12),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: const Color(0xFFF4F2FF),
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.event, color: Colors.black87),
                  const SizedBox(width: 8),
                  Text(
                    a.name,
                    style: const TextStyle(fontWeight: FontWeight.w600),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(
                    Icons.access_time,
                    size: 16,
                    color: Colors.black54,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    a.startTime,
                    style: const TextStyle(color: Colors.black54),
                  ),
                  const SizedBox(width: 12),
                  const Icon(
                    Icons.access_time_filled,
                    size: 16,
                    color: Colors.black54,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    '${a.duration} min',
                    style: const TextStyle(color: Colors.black54),
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}

class PlanDropdownCard extends StatelessWidget {
  final List<ItineraryModel> plans;
  final ItineraryModel selectedPlan;
  final ValueChanged<ItineraryModel> onPlanSelected;

  const PlanDropdownCard({
    super.key,
    required this.plans,
    required this.selectedPlan,
    required this.onPlanSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            ColorFiltered(
              colorFilter: const ColorFilter.mode(
                Color(0xB32F27CE),
                BlendMode.srcIn,
              ),
              child: SizedBox(width: 36, height: 36, child: AppIcons.itinerary),
            ),
            const SizedBox(width: 8),
            const Text('Wybrany plan', style: TextStyles.cardTitleHeading),
          ],
        ),
        const SizedBox(height: 8),
        CustomDropdown<ItineraryModel>(
          items: plans,
          initialItem: selectedPlan,
          hintText: 'Wybierz plan',
          onChanged: (ItineraryModel? newPlan) {
            if (newPlan != null) onPlanSelected(newPlan);
          },
          decoration: CustomDropdownDecoration(
            closedFillColor: const Color(0xFFF0ECFC),
            closedBorderRadius: BorderRadius.circular(16),
            closedSuffixIcon: const Icon(Icons.keyboard_arrow_down_rounded),
            headerStyle: TextStyles.cardTitleHeading,
            hintStyle: TextStyles.subtitle,
            listItemStyle: TextStyles.subtitle,
          ),
        ),
      ],
    );
  }
}
