import 'package:flutter/material.dart';
import 'package:hadith_iq/components/floating_button.dart';

class PaginatedExpansionTileList extends StatefulWidget {
  final List<String> searchResults; // The full list of results

  const PaginatedExpansionTileList({super.key, required this.searchResults});

  @override
  State<PaginatedExpansionTileList> createState() =>
      _PaginatedExpansionTileListState();
}

class _PaginatedExpansionTileListState
    extends State<PaginatedExpansionTileList> {
  int currentPage = 0;
  final int itemsPerPage = 6;

  // Get the paginated items for the current page
  List<String> get paginatedResults {
    final startIndex = currentPage * itemsPerPage;
    final endIndex =
        (startIndex + itemsPerPage).clamp(0, widget.searchResults.length);
    return widget.searchResults.sublist(startIndex, endIndex);
  }

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 10),
        child: Column(
          children: [
            // List of ExpansionTiles
            Expanded(
              child: ListView.builder(
                itemCount: paginatedResults.length,
                itemBuilder: (context, index) {
                  return Padding(
                    padding: const EdgeInsets.only(
                      left: 50,
                      right: 50,
                    ),
                    child: Card(
                      child: ExpansionTile(
                        title: Text(
                          "Result ${currentPage * itemsPerPage + index + 1}",
                          style: const TextStyle(
                              fontSize: 14, fontWeight: FontWeight.w600),
                        ),
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: Text(
                              paginatedResults[index],
                              style: const TextStyle(
                                  fontSize: 13, fontWeight: FontWeight.w500),
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),

            // Pagination controls
            Padding(
              padding: const EdgeInsets.only(top: 10,bottom: 5),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  MyFloatingButton(
                    icon: Icons.arrow_back_rounded,
                    text: 'Previous',
                    backgroundColor: Theme.of(context).colorScheme.onPrimary,
                    foregroundColor: Theme.of(context).colorScheme.primary,
                    onPressed: currentPage > 0
                        ? () {
                            setState(() {
                              currentPage--;
                            });
                          }
                        : null,
                    btnWidth: 116,
                    btnHeight: 40,
                  ),
                  const SizedBox(width: 5),
                  ElevatedButton(
                    onPressed: (currentPage + 1) * itemsPerPage <
                            widget.searchResults.length
                        ? () {
                            setState(() {
                              currentPage++;
                            });
                          }
                        : null,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Theme.of(context).colorScheme.onPrimary,
                    foregroundColor: Theme.of(context).colorScheme.primary,
                      elevation: 7,
                      fixedSize: const Size(116, 40),
                      shape: RoundedRectangleBorder(
                        side: BorderSide(
                          color: Theme.of(context).colorScheme.primary,
                          width: 0.3,
                        ),
                        borderRadius: BorderRadius.circular(15.0),
                      ),
                    ),
                    child: const Row(
                      mainAxisSize: MainAxisSize
                          .min, // Ensures button width matches content
                      children: [
                        Text(
                          'Next',
                          style: TextStyle(
                              fontSize: 12, fontWeight: FontWeight.w600),
                        ),
                        SizedBox(width: 5), // Space between text and icon
                        Icon(
                          Icons.arrow_forward_rounded,
                          size: 20,
                        ),
                      ],
                    ),
                  )
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
