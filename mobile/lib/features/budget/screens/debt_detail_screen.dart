import 'package:flutter/material.dart';
import 'package:mobile/core/models/debt_model.dart';
import 'package:mobile/core/models/trip_model.dart';
import 'package:mobile/core/theme/text_styles.dart';
import 'package:mobile/core/theme/themes.dart';
import 'package:mobile/core/services/debt_service.dart';

class DebtDetailScreen extends StatefulWidget {
  final DebtModel debt;
  final TripModel trip;

  const DebtDetailScreen({super.key, required this.debt, required this.trip});

  @override
  State<DebtDetailScreen> createState() => _DebtDetailScreenState();
}

class _DebtDetailScreenState extends State<DebtDetailScreen> {
  late DebtModel _debt;

  @override
  void initState() {
    super.initState();
    _debt = widget.debt;
  }

  void _showRepaymentModal(BuildContext context, int memberId, String memberName) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (ctx) {
        final bottomInset = MediaQuery.of(ctx).viewInsets.bottom;
        return Padding(
          padding: EdgeInsets.fromLTRB(24, 24, 24, bottomInset + 24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Spłata długu', style: TextStyles.cardTitleHeading),
              const SizedBox(height: 16),
              Text('Czy $memberName spłacił już zaległości?', style: TextStyles.subtitle),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () async {
                    Navigator.pop(ctx);
                    await _markAsRepaid(memberId);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text('Tak', style: TextStyles.whiteSubtitle),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Future<void> _markAsRepaid(int memberId) async {

    try {
      if (_debt.members.length == 1) {
        await DebtService.deleteDebt(
          tripId: widget.trip.id,
          debtId: _debt.id,
        );

        if (mounted) {
          Navigator.pop(context);
        }
      } else {
        await DebtService.removeMemberFromDebt(
          tripId: widget.trip.id,
          debtId: _debt.id,
          memberId: memberId,
        );

        final allDebts = await DebtService.fetchDebts(tripId: widget.trip.id);
        final updatedDebt = allDebts.firstWhere(
              (d) => d.id == _debt.id,
          orElse: () {
            return _debt;
          },
        );
        setState(() {
          _debt = updatedDebt;
        });
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Błąd podczas spłaty: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    try {
      return _buildSafe(context);
    } catch (e) {
      return Scaffold(
        body: Center(child: Text('Błąd widoku: $e')),
      );
    }
  }

  Widget _buildSafe(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
        title: Text(_debt.name, style: TextStyles.cardTitleHeading),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Pozostało do spłaty:', style: TextStyles.totalBudgetAmount),
            Text('${_debt.priceInPln.toStringAsFixed(2)} PLN', style: TextStyles.sectionHeading),
            const SizedBox(height: 16),
            Text('Dłużnicy:', style: TextStyles.cardTitleHeading),
            const SizedBox(height: 16),
            ..._buildMembersListSafely(),
          ],
        ),
      ),
    );
  }

  List<Widget> _buildMembersListSafely() {
    final widgets = <Widget>[];

    for (final member in _debt.members) {
      try {
        final name = '${member.firstName ?? ''} ${member.lastName ?? ''}'.trim();
        widgets.add(
          Card(
            elevation: 0,
            margin: const EdgeInsets.symmetric(vertical: 6),
            color: AppColors.cardsBackground,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: ListTile(
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              title: Text(name, style: TextStyles.cardTitleHeading),
              trailing: Text(
                '${_debt.pricePerMemberInPln.toStringAsFixed(2)} PLN',
                style: TextStyles.subtitle,
              ),
              onTap: () => _showRepaymentModal(context, member.id, name),
            ),
          ),
        );
      } catch (e) {
        widgets.add(Text(' Błąd przy wyświetlaniu dłużnika'));
      }
    }

    return widgets;
  }
}