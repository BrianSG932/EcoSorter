// lib/services/api_service.dart
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

/// Dirección donde está corriendo **FastAPI**.
/// – Si usas un emulador Android: 10.0.2.2:8000  
/// – Si usas un dispositivo físico: la IP de tu PC en la misma red (ej.: 192.168.50.180:8000)
const _baseUrl = 'https://ideal-succotash-wrgvvx4rrj5g35jq-8000.app.github.dev/clasificador/predecir';

Future<Map<String, dynamic>> classifyImage(File image) async {
  final request = http.MultipartRequest('POST', Uri.parse(_baseUrl))
    ..files.add(await http.MultipartFile.fromPath('file', image.path));

  try {
    final streamed = await request.send();
    final response = await http.Response.fromStream(streamed);

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else {
      throw Exception('Error ${response.statusCode}: ${response.body}');
    }
  } on SocketException {
    throw Exception('No se pudo conectar al servidor. '
        'Asegúrate de que FastAPI esté corriendo y tu teléfono/PC estén en la misma red.');
  }
}