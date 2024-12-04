import 'package:flutter/material.dart';
import 'package:hadith_iq/components/floating_button.dart';
import 'package:hadith_iq/components/list_tile_vertical.dart';

class MyDrawer extends StatelessWidget {
  final MyFloatingButton drawerHeaderButton;
  final List<MyListTileVert>? vertButtons;
  final List<ListTile>? buttons;

  const MyDrawer({
    super.key,
    this.vertButtons,
    this.buttons,
    required this.drawerHeaderButton,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Theme.of(context).colorScheme.surface,
      child: Container(
        width: 137,
        decoration: BoxDecoration(
          boxShadow: [
            BoxShadow(
              color: const Color(0xFFD6C091).withOpacity(0.2),
              blurRadius: 7,
              spreadRadius: 1,
              offset: const Offset(4, 4),
            ),
          ],
          borderRadius: const BorderRadius.only(
            topRight: Radius.circular(25),
            bottomRight: Radius.circular(25),
          ),
        ),
        child: Drawer(
          backgroundColor: Theme.of(context).colorScheme.surface,
          child: Column(
            children: [
              DrawerHeader(
                  child: Padding(
                padding: const EdgeInsets.only(
                    top: 44, bottom: 44),
                child: drawerHeaderButton,
              )),
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: // Check if vertButtons is null. If it is, use buttons; otherwise, use vertButtons.
                    (vertButtons ?? buttons ?? [])
                        .map((button) => button)
                        .toList(),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
