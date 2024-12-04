import 'package:flutter/material.dart';

class MyFloatingButton extends StatelessWidget {
  final IconData? icon;
  final String text;
  final Color backgroundColor;
  final Color foregroundColor;
  final void Function()? onPressed;
  final double btnWidth;
  final double btnHeight;

  const MyFloatingButton({
    super.key,
    this.icon,
    required this.text,
    required this.backgroundColor,
    required this.foregroundColor,
    required this.onPressed,
    this.btnWidth = 110,
    this.btnHeight = 50,
  });

  @override
  Widget build(BuildContext context) {
    if (icon != null) {
      return ElevatedButton.icon(
              onPressed: onPressed,
              label: Text(
                text,
                style:
                    const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
              ),
              icon: Icon(
                icon,
                size: 20,
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: backgroundColor,
                foregroundColor: foregroundColor,
                elevation: 7,
                fixedSize: Size(btnWidth, btnHeight),
                shape: RoundedRectangleBorder(
                  side: BorderSide(
                    color: foregroundColor,
                    width: 0.3,
                  ),
                  borderRadius: BorderRadius.circular(15.0),
                ),
              ));
    } else {
      return ElevatedButton(
          onPressed: onPressed,
          style: ElevatedButton.styleFrom(
            backgroundColor: backgroundColor,
            foregroundColor: foregroundColor,
            elevation: 3,
            shape: RoundedRectangleBorder(
              side: BorderSide(
                color: foregroundColor,
                width: 0.3,
              ),
              borderRadius: BorderRadius.circular(15.0),
            ),
            fixedSize: Size(btnWidth, btnHeight),
          ),
          child: Text(
            text,
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
          ));
    }
  }
}
