import 'package:flutter/material.dart';
import 'package:hadith_iq/api/project_api.dart';
import 'package:hadith_iq/components/search_bar.dart';

class ManageProjectsPage extends StatefulWidget {
  final Function(String) onGridItemClick;

  const ManageProjectsPage({
    super.key,
    required this.onGridItemClick,
  });

  @override
  State<ManageProjectsPage> createState() => ManageProjectsPageState();
}

class ManageProjectsPageState extends State<ManageProjectsPage> {
  ProjectService projectService = ProjectService();
// controller for TextField
  TextEditingController searchController = TextEditingController();

  List searchProjects = [];
  bool showLogo = false;
  bool isGridView = true;
  List _localProjects = [];
  List filteredProjects = [];

  @override
  void initState() {
    super.initState();
    isGridView = true;
    filteredProjects = _localProjects;
  }

  Future<void> fetchAndSetProjects() async {
    _localProjects = await projectService.fetchProjects();
  }

  // Function to get the current date
  String _getCurrentDate() {
    DateTime now = DateTime.now();
    return "${now.year}-${now.month}-${now.day}";
  }

  // Method to show the Add Project dialog
  Future<void> showAddProjectDialog() async {
    final TextEditingController projectController = TextEditingController();

    await showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text("Add New Project"),
          content: TextField(
            controller: projectController,
            decoration: const InputDecoration(
              hintText: "Enter project name",
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context); // Close the dialog
              },
              child: const Text("Cancel"),
            ),
            ElevatedButton(
              onPressed: () {
                final projectName = projectController.text.trim();
                if (projectName.isNotEmpty) {
                  setState(() {
                    String currentDate = _getCurrentDate();
                    _localProjects.add([projectName, currentDate]);
                    // sending to backend
                     projectService.addProject(projectName, currentDate);
                  });
                }
                Navigator.pop(context); // Close the dialog
              },
              child: const Text("Add"),
            ),
          ],
        );
      },
    );
  }

  void updateSearch(String query) {
    setState(() {
      filteredProjects = _localProjects
          .where((item) => item.toLowerCase().contains(query.toLowerCase()))
          .toList(); // Filter items based on the search query
    });
  }

  // Method to clear the search results
  void clearResults() {
    setState(() {
      searchController.clear();
      searchProjects = [];
    });
  }

  String? selectedFilePath;

  void logoVisiblity() {
    setState(() {
      if (_localProjects.isNotEmpty) {
        showLogo = false;
      } else {
        showLogo = true;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // logo in background
        showLogo
            ? Center(
                child: Opacity(
                  opacity: 0.1,
                  child: Image.asset(
                    'assets/images/FYP_Logo.png',
                    fit: BoxFit.cover,
                    width: 650,
                    height: 540,
                  ),
                ),
              )
            : const SizedBox.shrink(),

        Center(
          child: Column(
            children: [
              const SizedBox(height: 35),
              // Search Bar
              MySearchBar(
                  hintText: 'Search Project',
                  searchController: searchController,
                  onTap: () {},
                  onSubmitted: updateSearch),

              // Conditionally show the list/grid toggle Button
              Padding(
                padding: const EdgeInsets.only(right: 100),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    IconButton(
                        icon: Icon(
                          isGridView
                              ? Icons.grid_view_rounded
                              : Icons.view_list_rounded,
                        ),
                        onPressed: () {
                          if (_localProjects.isNotEmpty) {
                            setState(() {
                              isGridView =
                                  !isGridView;
                            });
                          }
                        },
                        color: Theme.of(context)
                            .colorScheme
                            .onPrimary, // Line color from theme
                        style: IconButton.styleFrom(
                          fixedSize: const Size(35, 35),
                          elevation: 10,
                          iconSize: 20,
                          backgroundColor: Theme.of(context)
                              .colorScheme
                              .primary, // Line color from theme
                        )),
                  ],
                ),
              ),

              Divider(
                color: Theme.of(context)
                    .colorScheme
                    .tertiary, // Line color from theme
                thickness: 0.5,
                indent: 200, // Space from the left edge
                endIndent: 200, // Space from the right edge
              ),

              const SizedBox(height: 10), // add space using this

              if (_localProjects.isNotEmpty && !isGridView)
                Padding(
                  padding: const EdgeInsets.only(left: 125, right: 220),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Name",
                        style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                            color: Theme.of(context).colorScheme.onSurface),
                      ),
                      Padding(
                        padding: const EdgeInsets.only(left: 325),
                        child: Text(
                          "Last Modified",
                          style: TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                              color: Theme.of(context).colorScheme.onSurface),
                        ),
                      ),
                      Text(
                        "Created",
                        style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                            color: Theme.of(context).colorScheme.onSurface),
                      ),
                    ],
                  ),
                ),

              const SizedBox(height: 5), // add space using this

              // Conditionally show GridView or ListView
              FutureBuilder(
                  future: projectService
                      .fetchProjects(), // Call the fetchProjects method here
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const Center(
                          child:
                              CircularProgressIndicator()); // Show loading spinner
                    } else if (snapshot.hasError) {
                      return Center(
                          child: Text(
                              'Error: ${snapshot.error}')); // Show error message
                    } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                      return const Center(
                          child: Text(
                              'No projects available')); // No data available
                    } else {
                      _localProjects = snapshot.data!;
                      return Expanded(
                        child: Padding(
                          padding: const EdgeInsets.only(
                              left: 100, right: 100, bottom: 20),
                          child: isGridView
                              ? GridView.builder(
                                  gridDelegate:
                                      const SliverGridDelegateWithFixedCrossAxisCount(
                                    crossAxisCount: 4, // Number of columns
                                    crossAxisSpacing:
                                        5.0, // Spacing between columns
                                    mainAxisSpacing:
                                        20.0, // Spacing between rows
                                  ),
                                  itemCount: _localProjects.length,
                                  itemBuilder: (context, index) {
                                    final projectName =
                                        _localProjects[index][0];
                                    return InkWell(
                                      onTap: () {
                                        widget.onGridItemClick(projectName);
                                      },
                                      borderRadius: BorderRadius.circular(12),
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Expanded(
                                            child: Card(
                                              color: Theme.of(context)
                                                  .colorScheme
                                                  .surface
                                                  .withOpacity(0.7),
                                              child: Center(
                                                  child: Text(
                                                projectName,
                                                style: TextStyle(
                                                    fontSize: 12,
                                                    fontWeight: FontWeight.w500,
                                                    color: Theme.of(context)
                                                        .colorScheme
                                                        .onSurface),
                                              )),
                                            ),
                                          ),
                                          Padding(
                                            padding:
                                                const EdgeInsets.only(left: 10),
                                            child: Text(
                                              projectName,
                                              style: TextStyle(
                                                  fontSize: 12,
                                                  fontWeight: FontWeight.w500,
                                                  color: Theme.of(context)
                                                      .colorScheme
                                                      .onSurface),
                                            ),
                                          ),
                                          Padding(
                                            padding: const EdgeInsets.only(
                                                left: 10, bottom: 3),
                                            child: Text(
                                              _localProjects[index][1],
                                              style: TextStyle(
                                                  fontSize: 12,
                                                  fontWeight: FontWeight.w500,
                                                  color: Theme.of(context)
                                                      .colorScheme
                                                      .onSurface),
                                            ),
                                          ),
                                        ],
                                      ),
                                    );
                                  },
                                )
                              : ListView.builder(
                                  itemCount: _localProjects.length,
                                  itemBuilder: (context, index) {
                                    final projectName =
                                        _localProjects[index][0];
                                    return MouseRegion(
                                      cursor: SystemMouseCursors.click,
                                      child: InkWell(
                                        onTap: () {
                                          widget.onGridItemClick(projectName);
                                        },
                                        borderRadius: BorderRadius.circular(12),
                                        child: Card(
                                          color: Theme.of(context)
                                              .colorScheme
                                              .surface
                                              .withOpacity(0.7),
                                          child: Row(
                                            mainAxisAlignment:
                                                MainAxisAlignment.spaceBetween,
                                            children: [
                                              Padding(
                                                padding: const EdgeInsets.only(
                                                    left: 20,
                                                    top: 10,
                                                    bottom: 10),
                                                child: Text(
                                                  projectName,
                                                  style: TextStyle(
                                                      fontSize: 13,
                                                      fontWeight:
                                                          FontWeight.w500,
                                                      color: Theme.of(context)
                                                          .colorScheme
                                                          .onSurface),
                                                ),
                                              ),
                                              Padding(
                                                padding: const EdgeInsets.only(
                                                    left: 300),
                                                child: Text(
                                                  '20 hours ago',
                                                  style: TextStyle(
                                                      fontSize: 13,
                                                      fontWeight:
                                                          FontWeight.w500,
                                                      color: Theme.of(context)
                                                          .colorScheme
                                                          .onSurface),
                                                ),
                                              ),
                                              Padding(
                                                padding: const EdgeInsets.only(
                                                    right: 100),
                                                child: Text(
                                                  _localProjects[index][1],
                                                  style: TextStyle(
                                                      fontSize: 13,
                                                      fontWeight:
                                                          FontWeight.w500,
                                                      color: Theme.of(context)
                                                          .colorScheme
                                                          .onSurface),
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                        ),
                      );
                    }
                  }),
            ],
          ),
        ),
      ],
    );
  }
}
