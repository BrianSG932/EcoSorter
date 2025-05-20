//camera_screen.dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '/services/api_service.dart'; // si usas un archivo externo para la función classifyImage
import 'classify_result_screen.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key}); // ← importante para rutas
  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  final picker = ImagePicker();
  File? _image;
  bool _loading = false;             // ← nuevo

  Future<void> _getImage() async {
    final pickedFile = await picker.pickImage(source: ImageSource.camera);

<<<<<<< HEAD
      final classification = await classifyImage(_image!);
=======
    if (pickedFile == null) return;
>>>>>>> 5db0d862a18e5dc39fc1ac2bbb857d29f37c5be8

    setState(() {
      _image   = File(pickedFile.path);
      _loading = true;
    });

    try {
      final classification = await classifyImage(_image!);

      if (!mounted) return;
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ClassifyResultScreen(
            imageFile: _image!,
            result: classification,
          ),
        ),
      );
<<<<<<< HEAD
=======
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(e.toString())));
      }
    } finally {
      if (mounted) setState(() => _loading = false);
>>>>>>> 5db0d862a18e5dc39fc1ac2bbb857d29f37c5be8
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Clasificador de Residuos")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _image != null
                ? Image.file(_image!, width: 300, height: 300)
                : const Icon(Icons.camera_alt, size: 100),
            const SizedBox(height: 20),
<<<<<<< HEAD
            ElevatedButton(
              onPressed: _getImage,
              child: const Text("Capturar Imagen"),
            ),
            const SizedBox(height: 20),
            Text(result, textAlign: TextAlign.center),
=======
            _loading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _getImage,
                    child: const Text("Capturar Imagen"),
                  ),
>>>>>>> 5db0d862a18e5dc39fc1ac2bbb857d29f37c5be8
          ],
        ),
      ),
    );
  }
}