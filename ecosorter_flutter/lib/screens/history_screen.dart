import 'package:flutter/material.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, String>> history = [
      {'fecha': '2025-05-22', 'detalle': 'Clasificaste 3 objetos reciclables'},
      {'fecha': '2025-05-21', 'detalle': 'Iniciaste sesión'},
      {
        'fecha': '2025-05-20',
        'detalle': 'Registraste un nuevo punto de recolección'
      },
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Historial de Actividad'),
        centerTitle: true,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: history.length,
        itemBuilder: (context, index) {
          final item = history[index];
          return Card(
            child: ListTile(
              leading: const Icon(Icons.history),
              title: Text(item['detalle']!),
              subtitle: Text('Fecha: ${item['fecha']}'),
            ),
          );
        },
      ),
    );
  }
}
