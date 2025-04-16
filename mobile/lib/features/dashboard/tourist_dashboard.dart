import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import '/core/models/trip_model.dart';
import '/core/widgets/dashboard_widgets.dart';

class TouristDashboard extends StatefulWidget {
  final String token;

  const TouristDashboard({super.key, required this.token});

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
    final response = await http.get(
      Uri.parse('https://api.plannder.com/trip/all/'),
      headers: {
        'accept': 'application/json',
        'Authorization': 'Bearer ${widget.token}',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      setState(() {
        _trips = data.map((e) => TripModel.fromJson(e)).toList();
        _selectedTrip = _trips.isNotEmpty ? _trips.first : null;
        _isLoading = false;
      });
    } else {
      setState(() => _isLoading = false);
    }
  }

  int _calculateTripDuration(DateTime start, DateTime end) => end.difference(start).inDays + 1;

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
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w500,
                  color: Colors.black87,
                ),
              ),
              const SizedBox(height: 24),
              if (_selectedTrip != null)
                TripDropdownCard(
                  trips: _trips,
                  selectedTrip: _selectedTrip!,
                  onTripSelected: (trip) => setState(() => _selectedTrip = trip),
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