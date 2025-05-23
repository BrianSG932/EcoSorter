import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:geolocator/geolocator.dart';
import '../screens/theme_provider.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool notificationsEnabled = true;
  String selectedLanguage = 'es';
  String selectedCountry = 'MX';
  String languageCode = 'es';

  final Map<String, String> languageNames = {
    'es': 'Español',
    'en': 'English',
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
      selectedCountry = prefs.getString('country') ?? 'MX';
      languageCode = selectedLanguage;
    });
  }

  Future<void> _saveNotifications(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setBool('notifications', value);
    setState(() => notificationsEnabled = value);
  }

  Future<void> _saveCountry(String country) async {
    final prefs = await SharedPreferences.getInstance();
    selectedCountry = country;

    switch (country) {
      case 'US':
        languageCode = 'en';
        break;
      default:
        languageCode = 'es';
    }

    await prefs.setString('country', selectedCountry);
    await prefs.setString('language', languageCode);

    setState(() {
      selectedLanguage = languageCode;
    });
  }

  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text("Configuración"),
        centerTitle: true,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          Card(
            child: ListTile(
              leading: const Icon(Icons.person),
              title: const Text("Perfil de usuario"),
              subtitle: const Text("Ver y editar información"),
              onTap: () => Navigator.pushNamed(context, '/profile'),
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
              title: const Text("Idioma actual"),
              subtitle: Text(languageNames[selectedLanguage] ?? 'Español'),
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: ListTile(
              leading: const Icon(Icons.flag),
              title: const Text("País / Región"),
              trailing: DropdownButton<String>(
                value: selectedCountry,
                onChanged: (value) {
                  if (value != null) {
                    _saveCountry(value);
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                          content: Text(
                              "Idioma aplicado: ${languageCode == 'es' ? 'Español' : 'Inglés'}")),
                    );
                  }
                },
                items: const [
                  DropdownMenuItem(value: 'MX', child: Text("México")),
                  DropdownMenuItem(value: 'US', child: Text("Estados Unidos")),
                  DropdownMenuItem(value: 'CO', child: Text("Colombia")),
                  DropdownMenuItem(value: 'AR', child: Text("Argentina")),
                  DropdownMenuItem(value: 'ES', child: Text("España")),
                ],
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
              leading: const Icon(Icons.location_on),
              title: const Text("Mostrar ubicación actual"),
              onTap: () async {
                bool serviceEnabled =
                    await Geolocator.isLocationServiceEnabled();
                LocationPermission permission =
                    await Geolocator.checkPermission();

                if (permission == LocationPermission.denied) {
                  permission = await Geolocator.requestPermission();
                }

                if (!serviceEnabled ||
                    permission == LocationPermission.deniedForever) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                        content: Text("Permiso de ubicación no disponible")),
                  );
                  return;
                }

                Position pos = await Geolocator.getCurrentPosition();
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text("Tu ubicación"),
                    content:
                        Text("Lat: ${pos.latitude}\nLng: ${pos.longitude}"),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text("Cerrar"),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: ListTile(
              leading: const Icon(Icons.verified_user),
              title: const Text("Permisos del dispositivo"),
              onTap: () async {
                Map<Permission, PermissionStatus> statuses = await [
                  Permission.camera,
                  Permission.location,
                  Permission.storage,
                  Permission.notification,
                ].request();

                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text("Estado de permisos"),
                    content: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: statuses.entries
                          .map((e) => Text(
                              "${e.key.toString().split('.').last}: ${e.value.name}"))
                          .toList(),
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text("Cerrar"),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: ListTile(
              leading: const Icon(Icons.help_outline),
              title: const Text("Centro de ayuda"),
              onTap: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text("Centro de ayuda"),
                    content: const Text(
                      "¿Tienes preguntas o necesitas soporte?\n\nEscríbenos a:\nsoporte@ecosorter.com",
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text("Cerrar"),
                      ),
                    ],
                  ),
                );
              },
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
