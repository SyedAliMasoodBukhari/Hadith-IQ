import 'package:flutter/material.dart';

class MySearchBar extends StatefulWidget {
  final String hintText;
  final TextEditingController searchController;
  final VoidCallback onTap;
  final void Function(String) onSubmitted;

  const MySearchBar({
    super.key,
    required this.hintText,
    required this.searchController,
    required this.onTap,
    required this.onSubmitted,
  });

  @override
  State<MySearchBar> createState() => _MySearchBarState();
}

class _MySearchBarState extends State<MySearchBar> {
  @override
  void initState() {
    super.initState();
    // Add a listener to update the UI when the text changes
    widget.searchController.addListener(() {
      setState(() {}); // Rebuild the widget
    });
  }

  @override
  void dispose() {
    widget.searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: MediaQuery.of(context).size.width * 0.43,
      height: 40,
      child: SearchBar(
        textStyle: WidgetStatePropertyAll(
          TextStyle(
            fontSize: 14,
            color: Theme.of(context).colorScheme.onSurface,
          )
        ),
        leading: Padding(
          padding: const EdgeInsets.all(7),
          child: widget.searchController.text.isEmpty
              ? Icon(
                  Icons.search,
                  color: Theme.of(context).colorScheme.primary,
                  size: 20,
                )
              : null,
        ),
        controller: widget.searchController,
        hintText: widget.hintText,
        onSubmitted: widget.onSubmitted,
        onTap: widget.onTap,
        trailing: widget.searchController.text.isNotEmpty
            ? [
                IconButton(
                  icon: Icon(
                    Icons.clear,
                    color: Theme.of(context).colorScheme.error,
                    size: 16,
                  ),
                  onPressed: () {
                    widget.searchController.clear();
                  },
                ),
              ]
            : null,
      ),
    );
  }
}
