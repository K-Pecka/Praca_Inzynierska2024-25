import 'package:flutter/material.dart';
import 'package:multi_select_flutter/chip_display/multi_select_chip_display.dart';
import 'package:multi_select_flutter/dialog/multi_select_dialog_field.dart';
import 'package:multi_select_flutter/util/multi_select_item.dart';
import 'package:multi_select_flutter/util/multi_select_list_type.dart';
import '../../../../core/theme/text_styles.dart';
import '../../../../core/theme/icons.dart';
import '../../../core/models/debt_model.dart';
import '../../../core/models/trip_model.dart';
import '../../../core/services/debt_service.dart';
import '../../../core/theme/themes.dart';
import '../../../core/widgets/custom_input_field.dart';

class DebtOverviewCard extends StatefulWidget {
  final double totalBudget;
  final double used;

  const DebtOverviewCard({
    super.key,
    required this.totalBudget,
    required this.used,
  });

  @override
  State<DebtOverviewCard> createState() => _DebtOverviewCardState();
}

class _DebtOverviewCardState extends State<DebtOverviewCard> {
  @override
  Widget build(BuildContext context) {

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            ColorFiltered(
              colorFilter: const ColorFilter.mode(
                AppColors.primary,
                BlendMode.srcIn,
              ),
              child: SizedBox(width: 36, height: 36, child: AppIcons.money),
            ),
            const SizedBox(width: 8),
            const Text(
              'Zaległości',
              style: TextStyles.cardTitleHeading,
            ),
          ],
        ),
        const SizedBox(height: 8),
        Container(
          width: double.infinity,
          decoration: BoxDecoration(
            color: AppColors.cardsBackground,
            borderRadius: BorderRadius.circular(20),
          ),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Łączny dług:',
                style: TextStyles.cardTitleHeading,
              ),
              const SizedBox(height: 8),
              Text(
                '${widget.totalBudget.toStringAsFixed(2)} PLN',
                style: TextStyles.sectionHeading,
              ),
            ],
          ),
        ),
      ],
    );
  }
}


class DebtActionsRow extends StatelessWidget {
  final bool showForm;
  final VoidCallback onToggleForm;
  final VoidCallback onFilter;

  const DebtActionsRow({
    super.key,
    required this.showForm,
    required this.onToggleForm,
    required this.onFilter,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: ElevatedButton(
            onPressed: onToggleForm,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              padding: const EdgeInsets.symmetric(vertical: 14),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            child: Text(
              showForm ? 'Anuluj' : 'Dodaj',
              style: TextStyles.whiteSubtitle,
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: ElevatedButton.icon(
            onPressed: onFilter,
            label: const Text('Filtruj', style: TextStyles.whiteSubtitle),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              padding: const EdgeInsets.symmetric(vertical: 14),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class DebtTile extends StatelessWidget {
  final DebtModel debt;
  final TripModel trip;
  final VoidCallback onTap;

  const DebtTile({super.key, required this.debt, required this.trip, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.cardsBackground,
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        onTap: onTap,
        title: Text(debt.name, style: TextStyles.cardTitleHeading),
        subtitle: Text('${debt.priceInPln.toStringAsFixed(2)} PLN', style: TextStyles.subtitle),
        trailing: const Icon(Icons.arrow_forward_ios_rounded, size: 16),
      ),
    );
  }
}

class DebtForm extends StatefulWidget {
  final TripModel trip;
  final VoidCallback onAdded;

  const DebtForm({super.key, required this.trip, required this.onAdded});

  @override
  State<DebtForm> createState() => _DebtFormState();
}

class _DebtFormState extends State<DebtForm> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _priceController = TextEditingController();
  String _selectedCurrency = 'PLN';

  final List<String> _currencies = ['PLN', 'EUR', 'USD'];

  late List<Member> _allMembers;
  List<Member> _selectedMembers = [];

  @override
  void initState() {
    super.initState();
    _allMembers = widget.trip.members;
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate() || _selectedMembers.isEmpty) return;

    await DebtService.addDebt(
      tripId: widget.trip.id,
      name: _nameController.text.trim(),
      price: _priceController.text.trim(),
      currency: _selectedCurrency,
      members: _selectedMembers.map((m) => m.id).toList(),
    );

    widget.onAdded();
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 32),
      child: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Center(child: Text('Dodaj zaległość', style: TextStyles.cardTitleHeading)),
            const SizedBox(height: 16),
            buildInputField(
              controller: _nameController,
              label: 'Nazwa',
              keyboardType: TextInputType.text,
              style: TextStyles.cardTitleHeading,
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16)),
              validator: (val) => val == null || val.isEmpty ? 'Podaj nazwę' : null,
            ),
            const SizedBox(height: 12),
            buildInputField(
              controller: _priceController,
              label: 'Kwota',
              keyboardType: TextInputType.number,
              style: TextStyles.cardTitleHeading,
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16)),
              validator: (val) => val == null || val.isEmpty ? 'Podaj kwotę' : null,
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _selectedCurrency,
              items: _currencies.map((c) => DropdownMenuItem(value: c, child: Text(c))).toList(),
              onChanged: (val) => setState(() => _selectedCurrency = val ?? 'PLN'),
              decoration: InputDecoration(
                labelText: 'Waluta',
                labelStyle: TextStyles.textHint,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(16)),
              ),
            ),
            const SizedBox(height: 16),
            MultiSelectDialogField<Member>(
              dialogWidth: 300,
              dialogHeight: 400,
              items: [
                MultiSelectItem<Member>(
                  Member(id: -1, firstName: 'Wszyscy', lastName: '', email: ''),
                  'Wszyscy',
                ),
                ..._allMembers.map((m) {
                  final name = '${m.firstName ?? ''} ${m.lastName ?? ''}'.trim();
                  return MultiSelectItem<Member>(m, name);
                })
              ],
              title: const Text("Uczestnicy"),
              buttonText: const Text("Wybierz uczestników"),
              buttonIcon: const Icon(Icons.person_add),
              cancelText: const Text("Anuluj", style: TextStyles.subtitle),
              confirmText: const Text("OK", style: TextStyles.subtitle),
              searchable: true,
              listType: MultiSelectListType.LIST,
              chipDisplay: MultiSelectChipDisplay.none(),
              onConfirm: (values) {
                final isSelectAll = values.any((m) => m.id == -1);
                setState(() {
                  if (isSelectAll) {
                    _selectedMembers = List.from(_allMembers);
                  } else {
                    _selectedMembers = values.where((m) => m.id != -1).toList();
                  }
                });
              },
              decoration: BoxDecoration(
                border: Border.all(color: Colors.black38, width: 1.2),
                borderRadius: BorderRadius.circular(16),
              ),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _submit,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('Zapisz', style: TextStyles.whiteSubtitle),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class TouristDebtTile extends StatelessWidget {
  final DebtModel debt;

  const TouristDebtTile({super.key, required this.debt});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.cardsBackground,
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        title: Text(debt.name, style: TextStyles.cardTitleHeading),
        subtitle: Text(
          '${debt.pricePerMemberInPln.toStringAsFixed(2)} PLN',
          style: TextStyles.subtitle,
        ),
      ),
    );
  }
}