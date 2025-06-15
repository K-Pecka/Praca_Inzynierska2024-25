import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '/core/theme/icons.dart';
import '/core/theme/themes.dart';
import '/core/models/trip_model.dart';

class CustomBottomNavBar extends StatelessWidget {
  final int currentIndex;
  final Function(int) onTap;
  final TripModel trip;

  const CustomBottomNavBar({
    super.key,
    required this.currentIndex,
    required this.onTap,
    required this.trip,
  });

  static const _selectedColor = AppColors.primary;
  static const _unselectedColor = AppColors.cardsBackground;

  Color _getColorForIcon(int index) {
    if (index == 4 && trip.creator.type != 2) {
      return Colors.grey.shade700;
    }
    return currentIndex == index ? _selectedColor : _unselectedColor;
  }

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      currentIndex: currentIndex,
      onTap: onTap,
      backgroundColor: AppColors.navigationBackground,
      type: BottomNavigationBarType.fixed,
      selectedItemColor: _selectedColor,
      unselectedItemColor: _unselectedColor,
      showSelectedLabels: false,
      showUnselectedLabels: false,
      items: [
        BottomNavigationBarItem(
          icon: _navIcon(NavbarIcons.home, 0),
          label: 'Home',
        ),
        BottomNavigationBarItem(
          icon: _navIcon(NavbarIcons.calendar, 1),
          label: 'Plan',
        ),
        BottomNavigationBarItem(
          icon: _navIcon(NavbarIcons.money, 2),
          label: 'Budżet',
        ),
        BottomNavigationBarItem(
          icon: _navIcon(NavbarIcons.ticket, 3),
          label: 'Bilety',
        ),
        BottomNavigationBarItem(
          icon: _navIcon(NavbarIcons.chat, 4),
          label: 'Czat',
        ),
      ],
    );
  }

  Widget _navIcon(SvgPicture icon, int index) {
    return ColorFiltered(
      colorFilter: ColorFilter.mode(
        _getColorForIcon(index),
        BlendMode.srcIn,
      ),
      child: SizedBox(width: 32, height: 32, child: icon),
    );
  }
}