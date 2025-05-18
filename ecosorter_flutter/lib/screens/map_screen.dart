import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late GoogleMapController _controller;

  final LatLng _initialPosition = const LatLng(19.4326, -99.1332); // CDMX
  final LatLng _recyclingPoint = const LatLng(19.427, -99.145); // Punto alterno

  void _goToRecyclingPoint() {
    _controller.animateCamera(
      CameraUpdate.newLatLngZoom(_recyclingPoint, 15),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Mapa de reciclaje")),
      body: GoogleMap(
        initialCameraPosition: CameraPosition(
          target: _initialPosition,
          zoom: 12,
        ),
        onMapCreated: (controller) {
          _controller = controller;
        },
        markers: {
          Marker(
            markerId: const MarkerId("punto1"),
            position: _initialPosition,
            infoWindow: const InfoWindow(title: "Centro de CDMX"),
          ),
          Marker(
            markerId: const MarkerId("reciclaje"),
            position: _recyclingPoint,
            infoWindow: const InfoWindow(title: "Punto de reciclaje"),
          ),
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _goToRecyclingPoint,
        child: const Icon(Icons.location_searching),
        tooltip: "Ir al punto de reciclaje",
      ),
    );
  }
}
