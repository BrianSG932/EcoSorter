//home_screen.dart
import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  final List<_NavItem> _navItems = [
    _NavItem(icon: Icons.home, label: 'Inicio', route: '/home'),
    _NavItem(icon: Icons.map, label: 'Mapa', route: '/map'),
    _NavItem(icon: Icons.bar_chart, label: 'Estadísticas', route: '/stats'),
    _NavItem(icon: Icons.settings, label: 'Ajustes', route: '/settings'),
    _NavItem(icon: Icons.logout, label: 'Salir', route: '/login'),
  ];

  void _navigateTo(String route) {
    Navigator.pushReplacementNamed(context, route);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("EcoSorter - Inicio"),
        actions: [
          IconButton(
            icon: const Icon(Icons.brightness_4),
            onPressed: () {
              // TODO: implementar modo oscuro
            },
          )
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text("Bienvenido al Clasificador de Basura",
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: () => _navigateTo('/camera'),
              icon: const Icon(Icons.camera_alt),
              label: const Text("Capturar imagen"),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        selectedItemColor: Colors.green,
        unselectedItemColor: Colors.grey,
        onTap: (index) {
          setState(() => _currentIndex = index);
          _navigateTo(_navItems[index].route);
        },
        items: _navItems
            .map((item) =>
                BottomNavigationBarItem(icon: Icon(item.icon), label: item.label))
            .toList(),
      ),
    );
  }
}

class _NavItem {
  final IconData icon;
  final String label;
  final String route;

  _NavItem({required this.icon, required this.label, required this.route});
}