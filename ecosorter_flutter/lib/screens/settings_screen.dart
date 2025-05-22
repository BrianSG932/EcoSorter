import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../screens/theme_provider.dart'; // Ajusta si lo moviste a /providers

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool notificationsEnabled = true;
  String selectedLanguage = 'es';

  final Map<String, String> languageNames = {
    'es': 'Español',
    'en': 'English',
    'fr': 'Français',
  };

  @override
  void initState() {
    super.initState();
    _loadPreferences();
  }

  Future<void> _loadPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      notificationsEnabled = prefs.getBool('notifications') ?? true;
      selectedLanguage = prefs.getString('language') ?? 'es';
    });
  }

  Future<void> _saveNotifications(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setBool('notifications', value);
    setState(() => notificationsEnabled = value);
  }

  Future<void> _saveLanguage(String value) async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('language', value);
    setState(() => selectedLanguage = value);
  }

  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);

    return Scaffold(
      appBar: AppBar(title: const Text("Configuración")),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: ListTile(
              leading: const Icon(Icons.person),
              title: const Text("Perfil de usuario"),
              subtitle: const Text("Ver y editar información"),
              onTap: () {
                showDialog(
                  context: context,
                  builder: (_) => AlertDialog(
                    title: const Text("Perfil"),
                    content: const Text("Funcionalidad por implementar"),
                    actions: [
                      TextButton(
                        child: const Text("Cerrar"),
                        onPressed: () => Navigator.pop(context),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: SwitchListTile(
              secondary: const Icon(Icons.brightness_6),
              title: const Text("Modo oscuro"),
              value: themeProvider.isDarkMode,
              onChanged: (_) => themeProvider.toggleTheme(),
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: ListTile(
              leading: const Icon(Icons.language),
              title: const Text("Idioma"),
              trailing: DropdownButton<String>(
                value: selectedLanguage,
                borderRadius: BorderRadius.circular(12),
                onChanged: (value) {
                  if (value != null) {
                    _saveLanguage(value);
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                          content: Text(
                              'Idioma cambiado a ${languageNames[value]}')),
                    );
                  }
                },
                items: languageNames.entries
                    .map((entry) => DropdownMenuItem(
                          value: entry.key,
                          child: Text(entry.value),
                        ))
                    .toList(),
              ),
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: SwitchListTile(
              secondary: const Icon(Icons.notifications_active),
              title: const Text("Notificaciones"),
              value: notificationsEnabled,
              onChanged: _saveNotifications,
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: ListTile(
              leading: const Icon(Icons.logout),
              title: const Text("Cerrar sesión"),
              onTap: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text("Confirmar"),
                    content: const Text("¿Deseas cerrar sesión?"),
                    actions: [
                      TextButton(
                        child: const Text("Cancelar"),
                        onPressed: () => Navigator.pop(context),
                      ),
                      ElevatedButton(
                        child: const Text("Cerrar sesión"),
                        onPressed: () {
                          Navigator.pushNamedAndRemoveUntil(
                            context,
                            '/login',
                            (_) => false,
                          );
                        },
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
