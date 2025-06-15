import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/themes.dart';
import '/core/models/trip_model.dart';
import '/core/theme/text_styles.dart';
import '/core/theme/icons.dart';
import 'package:animated_custom_dropdown/custom_dropdown.dart';

class TripDropdownCard extends StatelessWidget {
  final List<TripModel> trips;
  final TripModel selectedTrip;
  final ValueChanged<TripModel> onTripSelected;

  const TripDropdownCard({
    super.key,
    required this.trips,
    required this.selectedTrip,
    required this.onTripSelected,
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
              child: SizedBox(width: 36, height: 36, child: AppIcons.location),
            ),
            const SizedBox(width: 8),
            const Text(
              'Obecna wycieczka',
              style: TextStyles.cardTitleHeading,
            ),
          ],
        ),
        const SizedBox(height: 8),
        CustomDropdown<TripModel>(
          items: trips,
          initialItem: selectedTrip,
          hintText: 'Wybierz wycieczkę',
          onChanged: (TripModel? newTrip) {
            if (newTrip != null) {
              WidgetsBinding.instance.addPostFrameCallback((_) {
                onTripSelected(newTrip);
              });
            }
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

class TripDetailsCard extends StatelessWidget {
  final TripModel trip;
  final int duration;

  const TripDetailsCard({
    super.key,
    required this.trip,
    required this.duration,
  });

  @override
  Widget build(BuildContext context) {
    final start = DateFormat('dd.MM.yyyy').format(trip.startDate);
    final end = DateFormat('dd.MM.yyyy').format(trip.endDate);

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
              child: SizedBox(width: 36, height: 36, child: AppIcons.map),
            ),
            const SizedBox(width: 8),
            const Text('O Wycieczce', style: TextStyles.cardTitleHeading),
          ],
        ),
        const SizedBox(height: 8),
        Container(
          decoration: BoxDecoration(
            color: AppColors.cardsBackground,
            borderRadius: BorderRadius.circular(24),
          ),
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(trip.name, style: TextStyles.cardTitleHeading),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('$start - $end', style: TextStyles.subtitle),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      vertical: 6,
                      horizontal: 12,
                    ),
                    decoration: BoxDecoration(
                      color: AppColors.primary,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text('$duration dni', style: TextStyles.whiteSubtitle),
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
