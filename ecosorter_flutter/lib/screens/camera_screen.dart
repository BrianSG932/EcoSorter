//camera_screen.dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '/services/api_service.dart'; // si usas un archivo externo para la función classifyImage
import 'classify_result_screen.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});  // ← importante para rutas
  @override
  _CameraScreenState createState() => _CameraScreenState();
}


class _CameraScreenState extends State<CameraScreen> {
  final picker = ImagePicker();
  File? _image;
  String result = '';

  Future<void> _getImage() async {
    final pickedFile = await picker.pickImage(source: ImageSource.camera);
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });

    final classification = await classifyImage(_image!);

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ClassifyResultScreen(
            imageFile: _image!,
            result: classification,
          ),
        ),
      );


    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Clasificador de Residuos")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _image != null
                ? Image.file(_image!, width: 300, height: 300)
                : Icon(Icons.camera_alt, size: 100),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _getImage,
              child: Text("Capturar Imagen"),
            ),
            SizedBox(height: 20),
            Text(result, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}
