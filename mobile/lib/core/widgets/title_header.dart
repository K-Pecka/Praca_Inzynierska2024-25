import 'package:flutter/material.dart';

class TripTitleHeader extends StatelessWidget {
  final String title;

  const TripTitleHeader({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 32, left: 24, right: 24, bottom: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w600,
              color: Colors.black87,
            ),
          ),
          const CircleAvatar(
            radius: 18,
            backgroundColor: Color(0x80DEDCFF),
            child: Text(
              'MW',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: Color(0xBF2F27CE),
              ),
            ),
          ),
        ],
      ),
    );
  }
}