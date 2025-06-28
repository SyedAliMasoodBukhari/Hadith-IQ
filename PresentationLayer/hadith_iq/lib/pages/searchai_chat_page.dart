import 'package:flutter/material.dart';
import 'package:hadith_iq/components/basic_app_bar.dart';
import 'package:hadith_iq/components/chat_widget.dart';

class SearchAIChatPage extends StatefulWidget {
  final VoidCallback onToggleTheme;
  final String projectName; // Project name passed
  final VoidCallback projectButtonOnPressed;
  final bool isGlobal;

  const SearchAIChatPage(
      {super.key,
      required this.projectName,
      required this.onToggleTheme,
      required this.projectButtonOnPressed,
      required this.isGlobal});

  @override
  State<SearchAIChatPage> createState() => SearchAIChatPageState();
}

class SearchAIChatPageState extends State<SearchAIChatPage> {
  // ---------------- Local Variables ----------------
  late String currentProjectName;

  // ---------------------------------------------

  // ---------------- Constructor ----------------
  @override
  void initState() {
    super.initState();
    currentProjectName = widget.projectName;
  }
  // ---------------------------------------------

  // ---------------- Helper Methods ----------------

  // ---------------------------------------------

  @override
  Widget build(BuildContext context) {
    return SizedBox.expand(
      child: Column(
        children: [
          widget.isGlobal
              ? const SizedBox.shrink()
              : Padding(
                  padding: const EdgeInsets.only(left: 10),
                  child: MyBasicAppBar(
                    onToggleTheme: widget.onToggleTheme,
                    projectName: currentProjectName,
                    projectButtonOnPressed: widget.projectButtonOnPressed,
                  ),
                ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(
                  top: 5, left: 30, right: 30, bottom: 20),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: Theme.of(context).colorScheme.secondary,
                    width: 1,
                  ),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  spacing: 10,
                  children: [
                    Padding(
                      padding: const EdgeInsets.only(top: 15),
                      child: Text(
                        'Ask AI',
                        style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: Theme.of(context).colorScheme.onSurface),
                      ),
                    ),
                    Divider(
                      color:
                          Theme.of(context).colorScheme.surfaceContainerHighest,
                      thickness: 0.5,
                      indent: 200,
                      endIndent: 200,
                    ),
                    const Expanded(
                      child: Padding(
                        padding:
                            EdgeInsets.only(bottom: 10, left: 10, right: 10),
                        child: ModularChatWidget(),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
