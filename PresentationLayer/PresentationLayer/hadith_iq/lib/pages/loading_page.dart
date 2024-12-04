import 'package:flutter/material.dart';

class LoadingPage extends StatelessWidget {
  const LoadingPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Dimmed background
        ModalBarrier(
          color: Colors.black.withOpacity(0.5),
          dismissible: false,
        ),

        const Center(
          child: CircularProgressIndicator(
            color: Colors.white,
          ),
        ),
      ],
    );
  }
}
