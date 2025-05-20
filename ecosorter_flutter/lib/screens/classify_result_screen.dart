// lib/screens/classify_result_screen.dart

import 'dart:io';
import 'package:flutter/material.dart';

class ClassifyResultScreen extends StatelessWidget {
  final File imageFile;
  final Map<String, dynamic> result;

  const ClassifyResultScreen({
    super.key,
    required this.imageFile,
    required this.result,
  });

  @override
  Widget build(BuildContext context) {
    final clase = result['clase_predicha']['material'];
    final confianza = result['clase_predicha']['confianza'];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Resultado de Clasificación'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Image.file(imageFile, width: 300, height: 300),
            const SizedBox(height: 20),
            Text(
              'Material: $clase',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Text(
              'Confianza: $confianza%',
              style: const TextStyle(fontSize: 18),
            ),
            const Spacer(),
            ElevatedButton.icon(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(Icons.arrow_back),
              label: const Text("Volver"),
            )
          ],
        ),
      ),
    );
  }
}
