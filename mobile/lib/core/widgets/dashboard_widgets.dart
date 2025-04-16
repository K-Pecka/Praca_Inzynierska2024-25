import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '/core/models/trip_model.dart';

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
    return Container(
      decoration: BoxDecoration(
        color: const Color(0x80DEDCFF),
        borderRadius: BorderRadius.circular(24),
      ),
      padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 20),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Image.asset(
            'assets/icons/location.png',
            height: 36,
            width: 36,
            color: const Color(0xB32F27CE),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: DropdownButtonHideUnderline(
              child: DropdownButton<TripModel>(
                isExpanded: true,
                value: selectedTrip,
                icon: const Icon(Icons.keyboard_arrow_down_rounded, color: Colors.black54),
                dropdownColor: Colors.white,
                borderRadius: BorderRadius.circular(16),
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                  color: Colors.black87,
                ),
                itemHeight: 48,
                elevation: 3,
                selectedItemBuilder: (context) => trips.map((trip) {
                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        'Obecna wycieczka',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w400,
                          color: Colors.black54,
                          fontFamily: 'Quicksand',
                        ),
                      ),
                      Text(
                        trip.name,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: Colors.black87,
                          fontFamily: 'Quicksand',
                        ),
                      ),
                    ],
                  );
                }).toList(),
                items: trips.map((trip) {
                  return DropdownMenuItem(
                    value: trip,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 4),
                      child: Text(
                        trip.name,
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w500,
                          color: Colors.black87,
                        ),
                      ),
                    ),
                  );
                }).toList(),
                onChanged: (TripModel? newTrip) {
                  if (newTrip != null) onTripSelected(newTrip);
                },
              ),
            ),
          ),
        ],
      ),
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

    return Container(
      decoration: BoxDecoration(
        color: const Color(0x80DEDCFF),
        borderRadius: BorderRadius.circular(24),
      ),
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Image.asset(
                'assets/icons/map.png',
                height: 36,
                width: 36,
                color: const Color(0xB32F27CE),
              ),
              const SizedBox(width: 8),
              const Text(
                'O Wycieczce',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w400,
                  color: Colors.black54,
                  fontFamily: 'Quicksand',
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            trip.name,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: Colors.black87,
            ),
          ),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '$start - $end',
                style: const TextStyle(
                  fontSize: 16,
                  color: Colors.black54,
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 12),
                decoration: BoxDecoration(
                  color: const Color(0xFF2D1ED6),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  '$duration dni',
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}