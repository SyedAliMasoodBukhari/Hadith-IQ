import 'package:flutter/material.dart';
import 'package:hadith_iq/responsive/desktop_scaffold.dart';
import 'package:hadith_iq/responsive/mobile_scaffold.dart';
import 'package:hadith_iq/responsive/responsive_layout.dart';
import 'package:hadith_iq/responsive/tablet_scaffold.dart';
import 'package:hadith_iq/theme/theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  ThemeMode _themeMode = ThemeMode.light; // Default theme mode

  void _toggleTheme() {
    setState(() {
      _themeMode = _themeMode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: lightMode,
      darkTheme: darkMode,
      themeMode: _themeMode,
      home: ResponsiveLayout(
          mobileScaffold: const MobileScaffold(),
          tabletScaffold: TabletScaffold(onToggleTheme: _toggleTheme,),
          dekstopScaffold: DesktopScaffold(onToggleTheme: _toggleTheme,)),
    );
  }
}