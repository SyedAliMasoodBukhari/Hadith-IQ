import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

ColorScheme lightColorScheme = const ColorScheme(
  brightness: Brightness.light,
  primary: Color(0xFF1B4B29),
  onPrimary: Color(0xFFF8F8F8),
  secondary: Color(0xFFD6C091),
  onSecondary: Color(0xFFF8F8F8),
  tertiary: Color(0xFF710E1A),
  onTertiary: Color(0xFFF8F8F8),
  error: Color(0xFF710E1A),
  onError: Color(0xFFF8F8F8),
  surface: Color(0xFFF8F8F8),
  onSurface: Color(0xFF131919),
  // surfaceContainerLowest: Colors.grey[50]!, // Lowest background color
  // surfaceContainerLow: Colors.grey[100]!, // Slightly elevated
  // surfaceContainer: Colors.grey[200]!, // Default surface
  // surfaceContainerHigh: Colors.grey[300]!, // Elevated surface
  // surfaceContainerHighest: Colors.grey[400]!, // Highest elevation
  inverseSurface: Color(0xFF131919), // Used in dark mode elevated content
  // onInverseSurface: const Color(0xFFF9F9F9),
);

ColorScheme darkColorScheme = const ColorScheme(
  brightness: Brightness.dark,
  primary: Color(0xFFD6C091),
  onPrimary: Color(0xFF131919), // Darker text color on primary
  secondary: Color(0xFF1B4B29), // Same secondary color
  onSecondary: Color(0xFF131919), // White text/icons on secondary
  error: Color(0xFFCF6679), // Material dark theme error color
  onError: Color(0xFF131919), // Text color on error (dark background)
  surface: Color(0xFF131919), // Dark surface color
  onSurface: Color(0xFFD6C091), // Light text/icons on dark surfaces
  // surfaceContainerLowest: Color(0xFF131919), // Darkest background
  // surfaceContainerLow: Color(0xFF131919), // Slightly lighter
  // surfaceContainer: Color(0xFF131919), // Default surface
  // surfaceContainerHigh: Color(0xFF131919), // Elevated surface
  // surfaceContainerHighest: Color(0xFF131919), // Highest elevated surface
  // inverseSurface: Color(0xFF131919), // Light inverse surface
  // onInverseSurface: Color(0xFF1E1E1E), // Text color on light inverse surface
);

ThemeData lightMode = ThemeData(
  colorScheme: lightColorScheme,
  useMaterial3: true,
  textTheme: GoogleFonts.robotoTextTheme(),
);
ThemeData darkMode = ThemeData(
  useMaterial3: true,
  colorScheme: darkColorScheme,
  textTheme: GoogleFonts.robotoTextTheme(),
);
