import 'package:flutter/material.dart';
import '../../core/models/trip_model.dart';
import '../../features/dashboard/screens/tourist_dashboard_screen.dart';
import '../../features/itineraries/screens/itinerary_screen.dart';
import '../../features/budget/screens/tourist_budget_screen.dart';
import '../../core/widgets/bottom_navigation.dart';

class BottomNavScaffold extends StatefulWidget {
  final int userProfileId;
  final TripModel trip;

  const BottomNavScaffold({
    super.key,
    required this.userProfileId,
    required this.trip,
  });

  @override
  State<BottomNavScaffold> createState() => _BottomNavScaffoldState();
}

class _BottomNavScaffoldState extends State<BottomNavScaffold> {
  int _currentIndex = 0;
  late TripModel _currentTrip;

  @override
  void initState() {
    super.initState();
    _currentTrip = widget.trip;
  }

  void _updateTrip(TripModel newTrip) {
    setState(() {
      _currentTrip = newTrip;
    });
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> screens = [
      TouristDashboard(
        userProfileId: widget.userProfileId,
        trip: _currentTrip,
        onTripChange: _updateTrip,
      ),
      ItineraryScreen(
        trip: _currentTrip,
      ),
      TouristBudgetScreen(
        trip: _currentTrip,
        userProfileId: widget.userProfileId,
      ),
      const Placeholder(),
      const Placeholder(),
    ];

    return Scaffold(
      body: screens[_currentIndex],
      bottomNavigationBar: CustomBottomNavBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
      ),
    );
  }
}




