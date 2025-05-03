import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/text_styles.dart';
import '../../../core/widgets/base_screen.dart';
import '/core/models/itinerary_model.dart';
import '/core/models/activity_model.dart';
import '/core/models/trip_model.dart';
import '/core/services/itinerary_service.dart';
import '../widgets/itineraries_widgets.dart';

class ItineraryScreen extends StatefulWidget {
  final TripModel trip;

  const ItineraryScreen({
    super.key,
    required this.trip,
  });

  @override
  State<ItineraryScreen> createState() => _ItineraryScreenState();
}

class _ItineraryScreenState extends State<ItineraryScreen> {
  late Future<List<ItineraryModel>> _futureItineraries;
  List<ItineraryModel> _plans = [];
  List<ActivityModel> _activities = [];
  ItineraryModel? _selectedPlan;
  DateTime? _selectedDate;
  bool _loadingActivities = false;
  bool _hasLoadedActivitiesOnce = false;

  @override
  void initState() {
    super.initState();
    _futureItineraries = ItineraryService.fetchItineraries(tripId: widget.trip.id)
      ..then((plans) {
        if (plans.isNotEmpty) {
          setState(() {
            _plans = plans;
            _selectedPlan = plans.first;
            _selectedDate = plans.first.startDate;
          });
          _loadActivitiesForPlan(plans.first);
        }
      });
  }

  Future<void> _loadActivitiesForPlan(ItineraryModel plan) async {
    setState(() => _loadingActivities = true);

    final activities = await ItineraryService.fetchActivities(
      tripId: widget.trip.id,
      itineraryId: plan.id,
    );

    setState(() {
      _selectedPlan = plan;
      final now = DateTime.now();
      _selectedDate = (now.isAfter(plan.startDate) && now.isBefore(plan.endDate))
          ? now
          : plan.startDate;
      _activities = activities;
      _loadingActivities = false;
      _hasLoadedActivitiesOnce = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    return BaseScreen(
      trip: widget.trip,
      child: FutureBuilder<List<ItineraryModel>>(
        future: _futureItineraries,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Błąd: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Brak planów', style: TextStyles.subtitle));
          }

          _plans = snapshot.data!;
          _selectedPlan ??= _plans.first;
          _selectedDate ??= _selectedPlan!.startDate;

          if (!_hasLoadedActivitiesOnce && !_loadingActivities) {
            _loadActivitiesForPlan(_selectedPlan!);
          }

          final DateTime start = _selectedPlan!.startDate;
          final DateTime end = _selectedPlan!.endDate;

          final filteredActivities = _activities.where((a) =>
          a.date.year == _selectedDate!.year &&
              a.date.month == _selectedDate!.month &&
              a.date.day == _selectedDate!.day).toList();

          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              PlanDropdownCard(
                plans: _plans,
                selectedPlan: _selectedPlan!,
                onPlanSelected: (plan) => _loadActivitiesForPlan(plan),
              ),
              const SizedBox(height: 24),
              Center(
                child: Text(
                  toBeginningOfSentenceCase(DateFormat('LLLL', 'pl').format(_selectedDate!))!,
                  style: TextStyles.sectionHeading,
                ),
              ),
              const SizedBox(height: 16),
              DaySelector(
                start: start,
                end: end,
                activeDays: [_selectedPlan!],
                selected: _selectedDate!,
                onSelect: (d) => setState(() => _selectedDate = d),
              ),
              const SizedBox(height: 16),
              _loadingActivities
                  ? const Center(child: CircularProgressIndicator())
                  : ActivitiesList(activities: filteredActivities),
            ],
          );
        },
      ),
    );
  }
}





