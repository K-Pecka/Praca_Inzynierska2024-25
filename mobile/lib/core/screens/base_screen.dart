import 'package:flutter/material.dart';
import '../models/trip_model.dart';
import '../widgets/title_header.dart';

class BaseScreen extends StatelessWidget {
  final TripModel trip;
  final Widget child;
  final bool scrollable;

  const BaseScreen({
    super.key,
    required this.trip,
    required this.child,
    this.scrollable = true,
  });

  @override
  Widget build(BuildContext context) {
    final content = Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TripTitleHeader(title: trip.name),
        const SizedBox(height: 16),
        child,
      ],
    );

    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: scrollable
              ? SingleChildScrollView(
            padding: const EdgeInsets.only(bottom: 24),
            child: content,
          )
              : content,
        ),
      ),
    );
  }
}