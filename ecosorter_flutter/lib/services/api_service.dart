// lib/services/api_service.dart
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> classifyImage(File image) async {
  final uri = Uri.parse(
    'https://fantastic-space-trout-5gxvv59ggr46c4r7x-8000.app.github.dev/clasificador/predecir',
  );

  final request = http.MultipartRequest('POST', uri);
  request.files.add(await http.MultipartFile.fromPath('file', image.path));
  request.headers['accept'] = 'application/json';
  // No necesitas especificar Content-Type: multipart/form-data, se asigna automáticamente por MultipartRequest

  final streamedResponse = await request.send();
  final response = await http.Response.fromStream(streamedResponse);

  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    throw Exception(
        'Error al clasificar imagen. Código: ${response.statusCode}, ${response.body}');
  }
}