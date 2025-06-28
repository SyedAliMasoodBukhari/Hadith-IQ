import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_chat_core/flutter_chat_core.dart';
import 'package:uuid/uuid.dart';

class ModularChatWidget extends StatefulWidget {
  const ModularChatWidget({super.key});

  @override
  State<ModularChatWidget> createState() => _ModularChatWidgetState();
}

class _ModularChatWidgetState extends State<ModularChatWidget> {
  final User _currentUser = const User(id: 'user-id');
  late final InMemoryChatController _chatController;

  @override
  void initState() {
    super.initState();
    _chatController = InMemoryChatController();
  }

  @override
  void dispose() {
    _chatController.dispose();
    super.dispose();
  }

  void _handleSend(String text) {
    if (text.isEmpty) return;

    final sentMessage = Message.text(
      id: const Uuid().v4(),
      authorId: _currentUser.id,
      createdAt: DateTime.now(),
      text: text,
    );

    // Insert current user's message (sent)
    _chatController.insertMessage(sentMessage);

    // Simulate a reply (received)
    final receivedMessage = Message.text(
      id: const Uuid().v4(),
      authorId: 'other-user-id', // Different from currentUser.id
      createdAt: DateTime.now().add(const Duration(seconds: 1)),
      text: 'Auto-reply : Feature coming soon',
    );

    Future.delayed(const Duration(milliseconds: 500), () {
      _chatController.insertMessage(receivedMessage);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: Chat(
            chatController: _chatController,
            currentUserId: _currentUser.id,
            resolveUser: (userId) async {
              if (userId == _currentUser.id) return _currentUser;
              return const User(id: 'other-user-id', name: 'Responder');
            },
            onMessageSend: (text) => _handleSend(text),
            backgroundColor: Theme.of(context).colorScheme.surface,

            onMessageTap: (message, {TapUpDetails? details, int? index}) {
              if (message is TextMessage && message.text.isNotEmpty) {
                Clipboard.setData(ClipboardData(text: message.text));
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Message copied! ${message.text}'),
                    duration: const Duration(seconds: 1),
                  ),
                );
              }
            },

            // Custom theme
            theme: ChatTheme(
              colors: ChatColors(
                primary: Theme.of(context).colorScheme.primary,
                onPrimary: Theme.of(context).colorScheme.onPrimary,
                surface: Theme.of(context).colorScheme.surface,
                onSurface: Theme.of(context).colorScheme.onSurface,
                surfaceContainer:
                    Theme.of(context).colorScheme.secondaryFixedDim,
                surfaceContainerLow: Theme.of(context).colorScheme.surface,
                surfaceContainerHigh:
                    Theme.of(context).colorScheme.surfaceContainerHigh,
              ),
              typography: const ChatTypography(
                bodyLarge: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
                bodyMedium: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
                bodySmall: TextStyle(
                  fontSize: 12,
                ),
                labelLarge: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                ),
                labelMedium: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.w500,
                ),
                labelSmall: TextStyle(
                  fontSize: 10,
                ),
              ),
              shape: BorderRadius.circular(16),
            ),
          ),
        ),
      ],
    );
  }
}
