import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../../../core/services/trip_service.dart';
import '../../../core/theme/text_styles.dart';
import '/core/models/trip_model.dart';
import '../widgets/dashboard_widgets.dart';

class TouristDashboard extends StatefulWidget {
  final String token;
  final int userProfileId;
  final TripModel trip; // Received the trip model
  final Function(TripModel) onTripChange;

  const TouristDashboard({
    super.key,
    required this.token,
    required this.userProfileId,
    required this.trip,
    required this.onTripChange,
  });

  @override
  State<TouristDashboard> createState() => _TouristDashboardState();
}

class _TouristDashboardState extends State<TouristDashboard> {
  List<TripModel> _trips = [];
  TripModel? _selectedTrip;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchTrips();
  }

  Future<void> _fetchTrips() async {
    try {
      final trips = await TripService().fetchTrips(widget.token);
      setState(() {
        _trips = trips;
        _selectedTrip = trips.firstWhere(
              (e) => e.id == widget.trip.id,
          orElse: () => trips.isNotEmpty
              ? trips.first
              : TripModel(
            id: -1,
            name: 'Brak',
            creatorId: 0,
            members: [],
            startDate: DateTime.now(),
            endDate: DateTime.now(),
          ),
        );
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      debugPrint('Błąd pobierania wycieczek: $e');
    }
  }

  int _calculateTripDuration(DateTime start, DateTime end) =>
      end.difference(start).inDays + 1;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 32),
              const Text(
                'Witaj! Mateusz',
                style: TextStyles.sectionHeading,
              ),
              const SizedBox(height: 24),
              if (_selectedTrip != null)
                TripDropdownCard(
                  trips: _trips,
                  selectedTrip: _selectedTrip!,
                  onTripSelected: (trip) {
                    widget.onTripChange(trip); // Update trip on selection
                    setState(() {
                      _selectedTrip = trip;
                    });
                  },
                ),
              const SizedBox(height: 16),
              if (_selectedTrip != null)
                TripDetailsCard(
                  trip: _selectedTrip!,
                  duration: _calculateTripDuration(
                    _selectedTrip!.startDate,
                    _selectedTrip!.endDate,
                  ),
                ),
              const Spacer(),
            ],
          ),
        ),
      ),
    );
  }
}


