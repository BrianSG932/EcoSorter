import 'package:flutter/material.dart';
import 'package:camera/camera.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;
  CameraController? _cameraController;
  bool _isCameraInitialized = false;

  final List<Map<String, dynamic>> _pages = [
    {'icon': Icons.camera_alt, 'label': 'Clasificar', 'route': '/camera'},
    {'icon': Icons.map, 'label': 'Mapa', 'route': '/map'},
    {'icon': Icons.history, 'label': 'Historial', 'route': '/history'},
    {'icon': Icons.settings, 'label': 'Configuración', 'route': '/settings'},
  ];

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    final cameras = await availableCameras();
    if (cameras.isNotEmpty) {
      _cameraController = CameraController(
        cameras.first,
        ResolutionPreset.medium,
        enableAudio: false,
      );
      await _cameraController!.initialize();
      setState(() {
        _isCameraInitialized = true;
      });
    }
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
    Navigator.pushNamed(context, _pages[index]['route']);
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          const SizedBox(height: 20),
          const Text(
            'Vista previa de la cámara',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          Expanded(
            child: _isCameraInitialized
                ? AspectRatio(
                    aspectRatio: _cameraController!.value.aspectRatio,
                    child: CameraPreview(_cameraController!),
                  )
                : const Center(child: CircularProgressIndicator()),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: ElevatedButton.icon(
              onPressed: _isCameraInitialized
                  ? () async {
                      final image = await _cameraController!.takePicture();
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                            content: Text('Foto capturada: ${image.path}')),
                      );
                    }
                  : null,
              icon: const Icon(Icons.camera_alt),
              label: const Text('Tomar Foto'),
            ),
          ),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        selectedItemColor: Theme.of(context).primaryColor,
        unselectedItemColor: Colors.grey,
        items: _pages
            .map(
              (page) => BottomNavigationBarItem(
                icon: Icon(page['icon']),
                label: page['label'],
              ),
            )
            .toList(),
        type: BottomNavigationBarType.fixed,
      ),
    );
  }
}
