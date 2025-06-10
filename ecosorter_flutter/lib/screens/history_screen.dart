import 'package:flutter/material.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> history = [
      {
        'fecha': '2025-05-22 14:30',
        'detalle': 'Clasificaste una botella de plástico',
        'imagen': 'assets/images/plastico.png',
        'ubicacion': 'CDMX, México'
      },
      {
        'fecha': '2025-05-21 10:15',
        'detalle': 'Clasificaste una lata de aluminio',
        'imagen': 'assets/images/aluminio.png',
        'ubicacion': 'Guadalajara, Jalisco'
      },
      {
        'fecha': '2025-05-20 17:45',
        'detalle': 'Clasificaste una caja de cartón',
        'imagen': 'assets/images/carton.png',
        'ubicacion': 'Monterrey, Nuevo León'
      },
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Historial de Clasificaciones'),
        centerTitle: true,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: history.length,
        itemBuilder: (context, index) {
          final item = history[index];
          return Card(
            elevation: 3,
            margin: const EdgeInsets.symmetric(vertical: 8),
            child: ListTile(
              leading: Image.asset(
                item['imagen'],
                width: 50,
                height: 50,
                fit: BoxFit.cover,
              ),
              title: Text(item['detalle']),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Fecha y hora: ${item['fecha']}'),
                  Text('Ubicación: ${item['ubicacion']}'),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
