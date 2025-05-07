import 'package:flutter/material.dart';
import '../../../core/services/auth_service.dart';
import '../../../core/services/trip_service.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';
import '../../../core/widgets/menu_screen.dart';
import '/core/models/trip_model.dart';
import '../widgets/dashboard_widgets.dart';

class TouristDashboard extends StatefulWidget {
  final int userProfileId;
  final TripModel trip;
  final Function(TripModel) onTripChange;

  const TouristDashboard({
    super.key,
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
      final trips = await TripService.getAllTrips();
      setState(() {
        _trips = trips;
        _selectedTrip = trips.firstWhere(
              (e) => e.id == widget.trip.id,
          orElse: () => trips.isNotEmpty
              ? trips.first
              : TripModel(
            id: -1,
            name: 'Brak',
            creator: Member(id: 0, email: 'brak@brak.pl'),
            members: [],
            startDate: DateTime.now(),
            endDate: DateTime.now(),
            isCreator: false,
          ),
        );
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  int _calculateTripDuration(DateTime start, DateTime end) =>
      end.difference(start).inDays + 1;

  @override
  Widget build(BuildContext context) {
    final firstName = AuthService.firstName ?? '';
    final lastName = AuthService.lastName ?? '';
    final initials = ((firstName.isNotEmpty ? firstName[0] : '') +
        (lastName.isNotEmpty ? lastName[0] : ''))
        .toUpperCase();

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
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Witaj $firstName!',
                    style: TextStyles.sectionHeading,
                  ),
                  GestureDetector(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const ProfileMenuScreen()),
                      );
                    },
                    child: CircleAvatar(
                      radius: 24,
                      backgroundColor: AppColors.cardsBackground,
                      child: Text(
                        initials,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                          color: AppColors.primary,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              if (_selectedTrip != null)
                TripDropdownCard(
                  trips: _trips,
                  selectedTrip: _selectedTrip!,
                  onTripSelected: (trip) {
                    widget.onTripChange(trip);
                    setState(() => _selectedTrip = trip);
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


