import 'package:flutter/material.dart';
import 'package:hadith_iq/api/hadith_api.dart';
import 'package:hadith_iq/components/floating_button.dart';
import 'package:hadith_iq/components/paginated_list.dart';
import 'package:hadith_iq/components/search_bar.dart';

class SemanticSearchPage extends StatefulWidget {
  final String projectName; // Project name passed from the grid

  const SemanticSearchPage({super.key, required this.projectName});

  @override
  State<SemanticSearchPage> createState() => _SemanticSearchPageState();
}

class _SemanticSearchPageState extends State<SemanticSearchPage> {
  
  final HadithService hadithService= HadithService();
  late String currentProjectName;
// controller for TextField
  TextEditingController searchController = TextEditingController();

  List<String> searchResults = [];
  bool showHideLogo = true;
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    currentProjectName = widget.projectName; // Initialize with passed project name
  }

// Method to perform a search
  void performSearch(String query) async {
  if (query.isNotEmpty) {
    try {
      final List<String> results =
          await hadithService.fetchSemanticSearchResults(query, currentProjectName);

      setState(() {
        searchResults = results;
      });
      print(searchResults);
      print(searchResults.length);
    } catch (e) {
      print('Error fetching search results: $e');
    }
  }
  logoVisiblity();
}

void expandSearch(List<String> query) async {
  //clearResults();
  if (query.isNotEmpty) {
    try {
      print("in expand search");
      final List<String> results =
          await hadithService.fetchExpandSearchResults(query, currentProjectName);

      setState(() {
        searchResults = results;
      });
      print(searchResults);
      print(searchResults.length);
    } catch (e) {
      print('Error fetching search results: $e');
    }
  }
  logoVisiblity();
}

  // Method to clear the search results
  void clearResults() {
    setState(() {
      searchController.clear();
      searchResults = [];
      logoVisiblity();
    });
  }

  void logoVisiblity() {
    setState(() {
      if (searchResults.isNotEmpty) {
        showHideLogo = false;
      } else {
        showHideLogo = true;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Material(
        elevation: 10,
        borderRadius: BorderRadius.circular(16),
        shadowColor: const Color(0xFFD6C091).withOpacity(0.2),
        color: Theme.of(context).colorScheme.surface,
        child: Container(
          height: MediaQuery.of(context).size.height * 0.85,
          width: MediaQuery.of(context).size.width * 0.85,
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surface,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(
                color: const Color(0xFFD6C091).withOpacity(0.2),
                blurRadius: 10,
                spreadRadius: 3,
                offset:
                    const Offset(0, 0), // Shadow appears equally on all sides
              ),
            ],
          ),
          child: Stack(
            children: [
              // logo in background
              showHideLogo
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

              // Main content
              Center(
                child: Column(
                  children: [
                    const SizedBox(height: 27),
                    // Search Bar
                    MySearchBar(
                        hintText: 'Search Hadith or Narrator',
                        searchController: searchController,
                        onTap: logoVisiblity,
                        onSubmitted: performSearch),

                    const SizedBox(height: 15),

                    // Conditionally show the Clear and export Button
                    if (searchResults.isNotEmpty)
                      Padding(
                        padding: const EdgeInsets.only(left: 100, right: 100),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.start,
                          children: [
                            Padding(
                              padding: const EdgeInsets.only(right: 2),
                              child: MyFloatingButton(
                                icon: null,
                                text: 'Clear',
                                backgroundColor: Theme.of(context).colorScheme.onPrimary,
                                foregroundColor: Theme.of(context).colorScheme.primary,
                                onPressed: clearResults,
                                btnWidth: 90,
                                btnHeight: 43,
                              ),
                            ),
                            MyFloatingButton(
                              icon: null,
                              text: 'Expand',
                              backgroundColor: Theme.of(context).colorScheme.primary,
                              foregroundColor: Theme.of(context).colorScheme.onPrimary,
                              onPressed: () =>{
                                expandSearch(searchResults)
                              },
                              btnWidth: 90,
                              btnHeight: 46,
                            ),
                          ],
                        ),
                      ),
                    if (searchResults.isNotEmpty)
                      PaginatedExpansionTileList(
                        searchResults: searchResults,
                      ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
