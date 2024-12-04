import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:hadith_iq/components/drawer.dart';
import 'package:hadith_iq/components/floating_button.dart';
import 'package:hadith_iq/components/list_tile_vertical.dart';
import 'package:hadith_iq/pages/manage_projects.dart';
import 'package:hadith_iq/pages/semantic_search.dart';
import '../util/import_file.dart';

class DesktopScaffold extends StatefulWidget {
  final VoidCallback onToggleTheme;

  const DesktopScaffold({super.key, required this.onToggleTheme});

  @override
  State<DesktopScaffold> createState() => DesktopScaffoldState();
}

class DesktopScaffoldState extends State<DesktopScaffold> {
  final GlobalKey<ManageProjectsPageState> _manageProjectsKey =
      GlobalKey(); // GlobalKey for ManageProjectsPage

  // Default page for the content area
  Widget _contentArea = const SizedBox(); // Initially empty

  bool isProjectScreen = true;

  bool pressButton = false;

  String? selectedFilePath;

  @override
  void initState() {
    super.initState();
    pressButton = true;
    _contentArea = ManageProjectsPage(
      key: _manageProjectsKey,
      onGridItemClick: (projectName) {
        _changePage(SemanticSearchPage(projectName: projectName));
      },
    );
  }

  // Method to show the Add Project dialog via GlobalKey
  void _showAddProjectDialog() {
    _manageProjectsKey.currentState?.showAddProjectDialog(); // Access the state and call the method
  }

  // Function to handle the Import button press
  Future<void> _handleImportButtonPress() async {
    selectedFilePath = await ImportFile.selectCsvFile();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(selectedFilePath.toString()),
        backgroundColor: Theme.of(context).colorScheme.error,
        duration: const Duration(seconds: 2),
      ),
    );
  }

  // Method to change the content dynamically
  void _changePage(Widget newPage) {
    setState(() {
      pressButton = true;
      _contentArea = newPage;
      if (_contentArea.runtimeType != ManageProjectsPage) {
        isProjectScreen = false;
      } else {
        isProjectScreen = true;
      }
    });
  }

  // Function to handle the AppBar project button press
  void _handleProjectButtonPress() {
    _changePage(ManageProjectsPage(
      key: _manageProjectsKey,
      onGridItemClick: (projectName) {
        _changePage(SemanticSearchPage(projectName: projectName));
      },
    ));
  }

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    return Scaffold(
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
              const SizedBox(
                width: 7,
              ),
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
        body: Row(children: [
          // darwer
          isProjectScreen
              ? // Project Screen drawer
              MyDrawer(
                  drawerHeaderButton: MyFloatingButton(
                    icon: Icons.add,
                    text: 'New',
                    backgroundColor: Theme.of(context).colorScheme.primary,
                    foregroundColor: Theme.of(context).colorScheme.onPrimary,
                    onPressed: _showAddProjectDialog,
                  ),
                  vertButtons: [
                    MyListTileVert(
                      text: "P R O J E C T S",
                      onTap: () {
                        setState(() {
                          if (_contentArea.runtimeType == ManageProjectsPage) {
                            pressButton = true;
                          }
                        });
                      },
                      icon: const Icon(
                        Icons.layers_outlined,
                        size: 27,
                        color: Color(0xFF710E1A),
                      ),
                      isSelected: pressButton,
                    ),
                    MyListTileVert(
                      text: "R E C E N T S",
                      onTap: () {},
                      icon: const Icon(
                        Icons.access_time_rounded,
                        size: 27,
                        color: Color(0xFF710E1A),
                      ),
                    ),
                    MyListTileVert(
                      text: "T R A S H",
                      onTap: () {},
                      icon: const Icon(
                        Icons.delete_outline_rounded,
                        size: 27,
                        color: Color(0xFF710E1A),
                      ),
                    ),
                  ],
                )
              : // Main Screen drawer
              MyDrawer(
                  drawerHeaderButton: MyFloatingButton(
                    icon: Icons.add,
                    text: 'Import',
                    backgroundColor: Theme.of(context).colorScheme.primary,
                    foregroundColor: Theme.of(context).colorScheme.onPrimary,
                    onPressed: _handleImportButtonPress,
                  ),
                  vertButtons: [
                    MyListTileVert(
                      text: "S E A R C H",
                      onTap: () {
                        setState(() {
                          if (_contentArea is SemanticSearchPage) {
                            pressButton = true;
                          }
                        });
                      },
                      icon: const Icon(
                        Icons.search_rounded,
                        size: 27,
                        color: Color(0xFF710E1A),
                      ),
                      isSelected: pressButton,
                    ),
                    MyListTileVert(
                      text: "A H A D I T H",
                      onTap: () {},
                      icon: const Icon(
                        Icons.menu_book_rounded,
                        size: 27,
                        color: Color(0xFF710E1A),
                      ),
                    ),
                    MyListTileVert(
                      text: "N A R R A T O R S",
                      onTap: () {},
                      icon: const Icon(
                        Icons.people_alt_outlined,
                        size: 28,
                        color: Color(0xFF710E1A),
                      ),
                    ),
                  ],
                ),

          // body code
          Expanded(
              child: Stack(
            children: [
              // Content
              _contentArea,
            ],
          ))
        ]));
  }
}
