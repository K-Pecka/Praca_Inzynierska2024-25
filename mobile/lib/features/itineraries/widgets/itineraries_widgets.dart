import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '/core/models/itinerary_model.dart';
import '/core/models/activity_model.dart';
import '/core/theme/text_styles.dart';
import '/core/theme/icons.dart';

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

  bool _isInPlan(DateTime day) {
    return !day.isBefore(widget.start) && !day.isAfter(widget.end);
  }

  bool _isActive(DateTime day) {
    return widget.activeDays.any(
          (it) => !day.isBefore(it.startDate) && !day.isAfter(it.endDate),
    );
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
            final isSelected = date.day == widget.selected.day &&
                date.month == widget.selected.month &&
                date.year == widget.selected.year;
            final isInPlan = _isInPlan(date);
            final isActive = _isActive(date);

            final bgColor = isSelected
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
                  const Icon(Icons.access_time, size: 16, color: Colors.black54),
                  const SizedBox(width: 4),
                  Text(a.startTime, style: const TextStyle(color: Colors.black54)),
                  const SizedBox(width: 12),
                  const Icon(Icons.access_time_filled, size: 16, color: Colors.black54),
                  const SizedBox(width: 4),
                  Text('${a.duration} min', style: const TextStyle(color: Colors.black54)),
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
    return Container(
      decoration: BoxDecoration(
        color: const Color(0x80DEDCFF),
        borderRadius: BorderRadius.circular(24),
      ),
      padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 20),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          ColorFiltered(
            colorFilter:
            const ColorFilter.mode(Color(0xB32F27CE), BlendMode.srcIn),
            child: SizedBox(width: 32, height: 32, child: AppIcons.map),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: DropdownButtonHideUnderline(
              child: DropdownButton<ItineraryModel>(
                isExpanded: true,
                value: selectedPlan,
                icon: const Icon(Icons.keyboard_arrow_down_rounded,
                    color: Colors.black54),
                dropdownColor: Colors.white,
                borderRadius: BorderRadius.circular(16),
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                  color: Colors.black87,
                ),
                itemHeight: 48,
                elevation: 3,
                selectedItemBuilder: (context) => plans.map((plan) {
                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('Obecny plan',
                          style: TextStyles.cardTitleHeading),
                      Text(
                        plan.name,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          color: Colors.black87,
                          fontFamily: 'Quicksand',
                        ),
                      ),
                    ],
                  );
                }).toList(),
                items: plans.map((plan) {
                  return DropdownMenuItem(
                    value: plan,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 4),
                      child: Text(
                        plan.name,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w500,
                          color: Colors.black87,
                        ),
                      ),
                    ),
                  );
                }).toList(),
                onChanged: (ItineraryModel? newPlan) {
                  if (newPlan != null) onPlanSelected(newPlan);
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}

