import 'package:flutter/material.dart';

class ChatTile extends StatelessWidget {
  final String label;
  final String message;
  final String? initials;
  final VoidCallback onTap;
  final bool isAnnouncement;

  const ChatTile({
    super.key,
    required this.label,
    required this.message,
    required this.onTap,
    this.initials,
    this.isAnnouncement = false,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        children: [
          CircleAvatar(
            radius: 20,
            backgroundColor: const Color(0xFFDEDCFF).withOpacity(0.5),
            child: isAnnouncement
                ? const Icon(Icons.info_outline, color: Color(0xFF6A5AE0))
                : Text(
              initials ?? '',
              style: const TextStyle(color: Color(0xFF6A5AE0)),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: GestureDetector(
              onTap: onTap,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  color: const Color(0xFFDEDCFF).withOpacity(0.2),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      label,
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                      ),
                    ),
                    Text(
                      message,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontSize: 15),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}