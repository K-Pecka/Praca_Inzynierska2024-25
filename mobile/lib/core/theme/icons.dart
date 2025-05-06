import 'package:flutter_svg/flutter_svg.dart';

class NavbarIcons {
  static const String _path = 'assets/icons/navbar/';

  static final home = SvgPicture.asset('${_path}home.svg');
  static final calendar = SvgPicture.asset('${_path}calendar.svg');
  static final ticket = SvgPicture.asset('${_path}ticket.svg');
  static final chat = SvgPicture.asset('${_path}chat.svg');
  static final money = SvgPicture.asset('${_path}money_icon.svg');
}

class AppIcons{
  static const String _path = 'assets/icons/app/';

  static final location = SvgPicture.asset('${_path}location.svg');
  static final map = SvgPicture.asset('${_path}map.svg');
  static final money = SvgPicture.asset('${_path}money_icon.svg');
  static final itinerary = SvgPicture.asset('${_path}itinerary.svg');
}

class ActivityIcons {
  static final culture = SvgPicture.asset('assets/icons/app/activities/culture.svg');
  static final explore = SvgPicture.asset('assets/icons/app/activities/explore.svg');
  static final relax = SvgPicture.asset('assets/icons/app/activities/relax.svg');
  static final other = SvgPicture.asset('assets/icons/app/activities/other.svg');
}

class ExpenseIcons {
  static final attraction = SvgPicture.asset('assets/icons/app/expenses/attraction.svg');
  static final food = SvgPicture.asset('assets/icons/app/expenses/food.svg');
  static final transport = SvgPicture.asset('assets/icons/app/expenses/transport.svg');
  static final other = SvgPicture.asset('assets/icons/app/expenses/other.svg');
}