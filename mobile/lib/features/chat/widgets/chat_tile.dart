import 'package:flutter/material.dart';

import '../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';

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
            backgroundColor: AppColors.cardsBackground,
            child: isAnnouncement
                ? const Icon(Icons.info_outline, color: AppColors.primary)
                : Text(
              initials ?? '',
              style: const TextStyle(color: AppColors.primary),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: GestureDetector(
              onTap: onTap,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  color: AppColors.cardsBackground,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      label,
                      style: TextStyles.cardTitleHeading,
                    ),
                    Text(
                      message,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyles.subtitle,
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