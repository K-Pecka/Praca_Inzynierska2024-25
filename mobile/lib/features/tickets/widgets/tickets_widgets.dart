import 'package:flutter/material.dart';
import '../../../../core/models/ticket_model.dart';
import '../../../../core/theme/text_styles.dart';
import '../../../core/theme/themes.dart';
import '../screens/ticket_preview_screen.dart';

class TicketTile extends StatelessWidget {
  final TicketModel ticket;

  const TicketTile({super.key, required this.ticket});

  void _openFullScreen(BuildContext context, String imageUrl) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => TicketPreviewScreen(imageUrl: imageUrl),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.cardsBackground,
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(ticket.name, style: TextStyles.cardTitleHeading),
            const SizedBox(height: 8),

            Text(
              "${ticket.validFromDate}  ${ticket.validFromTime}",
              style: TextStyles.subtitle,
            ),
            const SizedBox(height: 8),

            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "Atrakcje Turystyczne",
                  style: TextStyles.subtitle,
                ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 20,
                      vertical: 10,
                    ),
                  ),
                  onPressed: () => _openFullScreen(context, ticket.file),
                  child: const Text(
                    "Podgląd",
                    style: TextStyles.whiteSubtitle,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
