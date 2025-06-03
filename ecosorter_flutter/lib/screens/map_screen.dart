//ecosorter_flutter/lib/screens/map_screen.dart
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late GoogleMapController _controller;

  final LatLng _initialPosition = const LatLng(23.644900232304753, -100.64795166362644); // CDMX
  final LatLng _recyclingPoint = const LatLng(23.63881579355342, -100.63919511899142); // Punto alterno
  final LatLng _recyclingPoint1 = const LatLng(23.654049247564654, -100.63729311366781); 
  final LatLng _recyclingPoint2 = const LatLng(23.669772220807662, -100.65171266866915);
  final LatLng _recyclingPoint3 = const LatLng(23.669772220807662, -100.65171266866915);

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
            infoWindow: const InfoWindow(title: "Centro de matehuala"),
          ),
          Marker(
            markerId: const MarkerId("reciclaje"),
            position: _recyclingPoint,
            infoWindow: const InfoWindow(title: "Punto de reciclaje"),
          ),
          Marker(
            markerId: const MarkerId("reciclaje"),
            position: _recyclingPoint1,
            infoWindow: const InfoWindow(title: "Punto de reciclaje"),
          ),
          Marker(
            markerId: const MarkerId("reciclaje"),
            position: _recyclingPoint2,
            infoWindow: const InfoWindow(title: "Punto de reciclaje"),
          ),
          Marker(
            markerId: const MarkerId("reciclaje"),
            position: _recyclingPoint3,
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