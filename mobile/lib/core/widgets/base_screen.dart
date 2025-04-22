import 'package:flutter/material.dart';
import 'title_header.dart';

class BaseScreen extends StatelessWidget {
  final String title;
  final Widget child;
  final bool scrollable;

  const BaseScreen({
    super.key,
    required this.title,
    required this.child,
    this.scrollable = true,
  });

  @override
  Widget build(BuildContext context) {
    final content = Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TripTitleHeader(title: title),
        const SizedBox(height: 16),
        child,
      ],
    );

    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: scrollable
            ? SingleChildScrollView(
          padding: const EdgeInsets.only(bottom: 24),
          child: content,
        )
            : content,
      ),
    );
  }
}