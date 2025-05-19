//main.dart
import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';
import 'screens/map_screen.dart';
import 'screens/stats_screen.dart';
import 'screens/settings_screen.dart';
import 'screens/camera_screen.dart';

void main() {
  runApp(const EcoSorterApp());
}

class EcoSorterApp extends StatelessWidget {
  const EcoSorterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EcoSorter',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      debugShowCheckedModeBanner: false,
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginScreen(),
        '/home': (context) => const HomeScreen(),
        '/map': (context) => const MapScreen(),
        '/stats': (context) => const StatsScreen(),
        '/settings': (context) => const SettingsScreen(),
        '/camera': (context) => const CameraScreen(),
      },
    );
  }
}