import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/widgets/base_screen.dart';
import '/core/models/itinerary_model.dart';
import '/core/services/itinerary_service.dart';
import '../widgets/itineraries_widgets.dart';

class ItineraryScreen extends StatefulWidget {
  final int tripId;
  final String token;

  const ItineraryScreen({
    super.key,
    required this.tripId,
    required this.token,
  });

  @override
  State<ItineraryScreen> createState() => _ItineraryScreenState();
}

class _ItineraryScreenState extends State<ItineraryScreen> {
  late Future<List<ItineraryModel>> _futureItineraries;
  List<ItineraryModel> _plans = [];
  ItineraryModel? _selectedPlan;
  DateTime? _selectedDate;

  @override
  void initState() {
    super.initState();
    _futureItineraries = ItineraryService().fetchItineraries(
      tripId: widget.tripId,
      token: widget.token,
    );
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: FutureBuilder<List<ItineraryModel>>(
        future: _futureItineraries,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Błąd: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Brak planów'));
          }

          _plans = snapshot.data!;
          _selectedPlan ??= _plans.first;

          final DateTime start = _plans.map((i) => i.startDate).reduce((a, b) => a.isBefore(b) ? a : b);
          final DateTime end = _plans.map((i) => i.endDate).reduce((a, b) => a.isAfter(b) ? a : b);
          _selectedDate ??= start;

          return BaseScreen(
            title: 'Majówka we Francji',
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                PlanDropdownCard(
                  plans: _plans,
                  selectedPlan: _selectedPlan!,
                  onPlanSelected: (plan) => setState(() {
                    _selectedPlan = plan;
                    _selectedDate = plan.startDate;
                  }),
                ),
                const SizedBox(height: 24),
                Center(
                  child: Text(
                    toBeginningOfSentenceCase(DateFormat('LLLL', 'pl').format(_selectedDate!))!,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.black87,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                DaySelector(
                  start: start,
                  end: end,
                  activeDays: _plans,
                  selected: _selectedDate!,
                  onSelect: (d) => setState(() => _selectedDate = d),
                ),
                const SizedBox(height: 16),
                const MockActivitiesList(), // zamiast Expanded
              ],
            ),
          );
        },
      ),
    );
  }
}

