import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> classifyImage(File image) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('http://192.168.51.229:8000/clasificador/predecir'), // cambia a tu API real
  );
  request.files.add(await http.MultipartFile.fromPath('file', image.path));
  var response = await request.send();

  if (response.statusCode == 200) {
    var responseBody = await response.stream.bytesToString();
    return jsonDecode(responseBody);
  } else {
    throw Exception("Error en clasificación");
  }
}