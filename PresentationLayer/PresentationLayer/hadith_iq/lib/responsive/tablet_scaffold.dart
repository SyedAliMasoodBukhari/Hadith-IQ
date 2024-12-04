import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:hadith_iq/components/drawer.dart';
import 'package:hadith_iq/components/floating_button.dart';
import 'package:hadith_iq/components/list_tile_vertical.dart';

class TabletScaffold extends StatefulWidget {
  final VoidCallback onToggleTheme;
  const TabletScaffold({super.key, required this.onToggleTheme});

  @override
  State<TabletScaffold> createState() => _TabletScaffoldState();
}

class _TabletScaffoldState extends State<TabletScaffold> {
  // Function to handle the AppBar project button press
  void _handleProjectButtonPress() {}

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    return Scaffold(
      backgroundColor: Colors.grey[200],
      appBar: AppBar(
          backgroundColor: Theme.of(context).colorScheme.secondary,
          title: Row(
            mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  "IQ",
                  style: GoogleFonts.elMessiri(
                      color: Theme.of(context).colorScheme.primary,
                      fontSize: 30,
                      fontWeight: FontWeight.w700),
                ),
                const SizedBox(width: 7,),
                Text(
                  "حديث",
                  style: GoogleFonts.elMessiri(
                      color: Theme.of(context).colorScheme.error,
                      fontSize: 30,
                      fontWeight: FontWeight.w700),
                ),

              ],
            ),
          leading: IconButton(
              onPressed: _handleProjectButtonPress,
              icon: Icon(
                Icons.layers_outlined,
                color: Theme.of(context).colorScheme.primary,
              )),
          actions: [
            Padding(
              padding: const EdgeInsets.only(right: 10),
              child: IconButton(
                icon: Icon(
                  isDarkMode ? Icons.dark_mode : Icons.light_mode,
                  color: isDarkMode ? Colors.amber : Colors.white,
                ),
                onPressed: widget.onToggleTheme,
              ),
            ),
          ],
        ),
      drawer: MyDrawer(
        drawerHeaderButton: MyFloatingButton(
          icon: Icons.add,
          text: 'New',
          backgroundColor: Theme.of(context).colorScheme.primary,
          foregroundColor: Theme.of(context).colorScheme.onPrimary,
          onPressed: () {},
        ),
        vertButtons: [
          MyListTileVert(
              text: "P R O J E C T S",
              onTap: () {},
              icon: const Icon(
                Icons.layers_outlined,
                size: 30,
                color: Color(0xFF710E1A),
              )),
          MyListTileVert(
              text: "A H A D I T H",
              onTap: () {},
              icon: const Icon(
                Icons.manage_search_rounded,
                size: 30,
                color: Color(0xFF710E1A),
              )),
          MyListTileVert(
              text: "N A R R A T O R S",
              onTap: () {},
              icon: const Icon(
                Icons.manage_search_rounded,
                size: 30,
                color: Color(0xFF710E1A),
              )),
        ],
      ),
    );
  }
}
