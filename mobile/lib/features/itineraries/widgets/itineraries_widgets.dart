import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/services/ticket_service.dart';
import '../../../core/theme/themes.dart';
import '../../tickets/screens/ticket_preview_screen.dart';
import '/core/models/itinerary_model.dart';
import '/core/models/activity_model.dart';
import '/core/theme/text_styles.dart';
import '/core/theme/icons.dart';
import 'package:animated_custom_dropdown/custom_dropdown.dart';
import 'package:url_launcher/url_launcher.dart';

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
      child: Align(
        alignment: Alignment.center,
        child: ListView.separated(
          controller: _scrollController,
          scrollDirection: Axis.horizontal,
          shrinkWrap: true,
          itemCount: days.length,
          separatorBuilder: (_, __) => const SizedBox(width: 8),
          itemBuilder: (context, index) {
            final date = days[index];
            final isSelected = _isSameDay(date, widget.selected);
            final isInPlan = _isInPlan(date);
            final isActive = _isActive(date);

            final bgColor =
                isSelected
                    ? AppColors.primary
                    : isInPlan && isActive
                    ? AppColors.cardsBackground
                    : AppColors.subtitleText;

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
  final int tripId;

  const ActivitiesList({
    super.key,
    required this.activities,
    required this.tripId,
  });

  Widget _getActivityIcon(int type) {
    switch (type) {
      case 1:
        return ActivityIcons.culture;
      case 2:
        return ActivityIcons.relax;
      case 3:
        return ActivityIcons.explore;
      case 4:
      default:
        return ActivityIcons.other;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (activities.isEmpty) {
      return const Center(
        child: Text('Brak aktywności na ten dzień', style: TextStyles.subtitle),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: activities.length,
      itemBuilder: (context, index) {
        final a = activities[index];
        return InkWell(
          onTap: () => showActivityDetailsModal(context, a, tripId),
          child: Container(
            margin: const EdgeInsets.only(bottom: 12),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.cardsBackground,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    SizedBox(
                      height: 24,
                      width: 24,
                      child: ColorFiltered(
                        colorFilter: const ColorFilter.mode(
                          AppColors.titleText,
                          BlendMode.srcIn,
                        ),
                        child: _getActivityIcon(a.type),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(a.name, style: TextStyles.cardTitleHeading),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    const Icon(
                      Icons.access_time,
                      size: 18,
                      color: AppColors.subtitleText,
                    ),
                    const SizedBox(width: 4),
                    Text(a.startTime, style: TextStyles.subtitle),
                    const SizedBox(width: 12),
                    const Icon(
                      Icons.access_time_filled,
                      size: 18,
                      color: AppColors.subtitleText,
                    ),
                    const SizedBox(width: 4),
                    Text('${a.duration} min', style: TextStyles.subtitle),
                  ],
                ),
              ],
            ),
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
                AppColors.primary,
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
            closedFillColor: AppColors.cardsBackground,
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

void showActivityDetailsModal(
  BuildContext context,
  ActivityModel activity,
  int tripId,
) {
  showModalBottomSheet(
    context: context,
    isScrollControlled: true,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
    ),
    builder:
        (_) => Padding(
          padding: const EdgeInsets.fromLTRB(24, 24, 24, 32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: AppColors.subtitleText,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Text(
                "Tytuł: ${activity.name}",
                style: TextStyles.cardTitleHeading,
              ),
              const SizedBox(height: 8),
              Text("Opis: ${activity.description}", style: TextStyles.subtitle),
              const SizedBox(height: 8),
              Text("Data: ${activity.date}", style: TextStyles.subtitle),
              const SizedBox(height: 8),
              Text(
                "Godzina: ${activity.startTime}",
                style: TextStyles.subtitle,
              ),
              const SizedBox(height: 8),
              Text(
                "Lokalizacja: ${activity.location}",
                style: TextStyles.subtitle,
              ),
              const SizedBox(height: 24),
              if (activity.ticket != null)
                Center(
                  child: ElevatedButton.icon(
                    onPressed: () async {
                      try {
                        final tickets = await TicketService.getTicketsByTrip(
                          tripId,
                        );
                        final ticket = tickets.firstWhere(
                          (t) => t.id == activity.ticket,
                        );
                        Navigator.pop(context);
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder:
                                (_) =>
                                    TicketPreviewScreen(imageUrl: ticket.file),
                          ),
                        );
                      } catch (e) {
                        debugPrint('Nie udało się pobrać biletu: $e');
                      }
                    },
                    icon: const Icon(
                      Icons.airplane_ticket,
                      color: AppColors.cardsBackground,
                    ),
                    label: const Text("Bilet", style: TextStyles.whiteSubtitle),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primary,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 32,
                        vertical: 12,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
              const SizedBox(height: 8),
              if (activity.location.isNotEmpty)
                Center(
                  child: ElevatedButton.icon(
                    onPressed: () async {
                      final encoded = Uri.encodeComponent(activity.location);
                      final uri = Uri.parse(
                        'https://www.google.com/maps/dir/?api=1&destination=$encoded',
                      );

                      if (await canLaunchUrl(uri)) {
                        await launchUrl(
                          uri,
                          mode: LaunchMode.externalApplication,
                        );
                      } else {
                        debugPrint('Nie można otworzyć Google Maps');
                      }
                    },
                    icon: const Icon(
                      Icons.location_on,
                      color: AppColors.cardsBackground,
                    ),
                    label: const Text(
                      "Lokalizacja",
                      style: TextStyles.whiteSubtitle,
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primary,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 32,
                        vertical: 12,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
  );
}
