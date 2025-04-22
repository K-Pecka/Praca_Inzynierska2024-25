import 'package:flutter/material.dart';
import '../../features/dashboard/screens/tourist_dashboard_screen.dart';
import '../../features/itineraries/screens/itinerary_screen.dart';
import '../../features/budget/screens/tourist_budget_screen.dart';
import 'bottom_navigation.dart';

class BottomNavScaffold extends StatefulWidget {
  final String token;
  final int userProfileId;
  final int tripId;

  const BottomNavScaffold({
    super.key,
    required this.token,
    required this.userProfileId,
    required this.tripId,
  });

  @override
  State<BottomNavScaffold> createState() => _BottomNavScaffoldState();
}

class _BottomNavScaffoldState extends State<BottomNavScaffold> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    final List<Widget> screens = [
      TouristDashboard(
        token: widget.token,
        userProfileId: widget.userProfileId,
        tripId: widget.tripId,
      ),
      ItineraryScreen(
        tripId: widget.tripId,
        token: widget.token,
      ),
      TouristBudgetScreen(
        token: widget.token,
        tripId: widget.tripId,
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