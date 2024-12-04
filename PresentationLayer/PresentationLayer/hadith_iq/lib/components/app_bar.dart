import 'package:flutter/material.dart';

class MyAppBar extends StatelessWidget implements PreferredSizeWidget {
  final Widget title;
  final Color backgroundColor;
  final double appBarHeight;
  final bool showLogo;
  final void Function()? projectIconOnPress;
  final void Function()? lightModeOnPress;

  const MyAppBar({
    required this.appBarHeight,
    required this.title,
    this.backgroundColor = Colors.deepPurple,
    super.key,
    this.showLogo = false,
    required this.projectIconOnPress,
    required this.lightModeOnPress,
  });

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: backgroundColor,
      title: title,
      flexibleSpace: showLogo
          ? Align(
              alignment: Alignment.centerLeft,
              child: Padding(
                padding:
                    const EdgeInsets.only(left: 30), // Add spacing if needed
                child: Image.asset(
                  'assets/images/FYP_Logo.png',
                  height: 56,
                  fit: BoxFit.contain,
                ),
              ),
            )
          : null,
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(appBarHeight);
}
