import 'package:flutter/material.dart';
import '../../core/models/trip_model.dart';
import '../../features/dashboard/screens/dashboard_screen.dart';
import '../../features/itineraries/screens/itinerary_screen.dart';
import '../../features/budget/screens/budget_screen.dart';
import '../../core/widgets/bottom_navigation.dart';
import '../../features/tickets/screens/tickets_screen.dart';
import '../../features/chat/screens/chat_overview_screen.dart';

class BottomNavScaffold extends StatefulWidget {
  final int userProfileId;
  final int profileType;
  final TripModel trip;

  const BottomNavScaffold({
    super.key,
    required this.userProfileId,
    required this.profileType,
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
        trip: _currentTrip,
        userProfileId: widget.userProfileId,
        onTripChange: _updateTrip,
      ),
      ItineraryScreen(
        trip: _currentTrip,
      ),
      BudgetScreen(
        trip: _currentTrip,
        userProfileId: widget.userProfileId,
      ),
      TouristTicketsScreen(
        trip: _currentTrip,
      ),
      ChatOverviewScreen(
        trip: _currentTrip,
        userProfileId: widget.userProfileId,
        profileType: widget.profileType,
      ),
    ];

    return Scaffold(
      body: screens[_currentIndex],
      bottomNavigationBar: CustomBottomNavBar(
        currentIndex: _currentIndex,
        trip: _currentTrip,
        onTap: (index) {
          final isChatTab = index == 4;
          final isGuide = _currentTrip.creator.type == 2;

          if (isChatTab && !isGuide) return;
          setState(() => _currentIndex = index);
        },
      ),
    );
  }
}


