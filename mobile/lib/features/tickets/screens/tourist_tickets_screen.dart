import 'package:flutter/material.dart';
import '../../../../core/models/ticket_model.dart';
import '../../../../core/services/ticket_service.dart';
import '../../../../core/widgets/base_screen.dart';
import '../../../../core/models/trip_model.dart';
import '../widgets/tickets_widgets.dart';

class TouristTicketsScreen extends StatefulWidget {
  final TripModel trip;

  const TouristTicketsScreen({super.key, required this.trip});

  @override
  State<TouristTicketsScreen> createState() => _TouristTicketsScreenState();
}

class _TouristTicketsScreenState extends State<TouristTicketsScreen> {
  late Future<List<TicketModel>> _futureTickets;

  @override
  void initState() {
    super.initState();
    _futureTickets = TicketService.getTicketsByTrip(widget.trip.id);
  }

  @override
  Widget build(BuildContext context) {
    return BaseScreen(
      trip: widget.trip,
      child: FutureBuilder<List<TicketModel>>(
        future: _futureTickets,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Błąd: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text("Brak biletów"));
          }

          final tickets = snapshot.data!;
          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: tickets.map((ticket) {
              return TicketTile(ticket: ticket);
            }).toList(),
          );
        },
      ),
    );
  }
}
