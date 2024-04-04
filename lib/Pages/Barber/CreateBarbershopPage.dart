import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class CreateBarbershopPage extends StatelessWidget {
  final String accessToken;

  CreateBarbershopPage({required this.accessToken});

  final TextEditingController nameController = TextEditingController();
  final TextEditingController addressController = TextEditingController();

  Future<void> createBarbershop(BuildContext context) async {
    final int userId = extractUserIdFromToken(accessToken);
    final String apiUrl =
        'http://192.168.10.69:8000/api/barbershops/create/$userId/';

    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {
        'Authorization': 'Bearer $accessToken',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'name': nameController.text,
        'address': addressController.text,
        'user_id': userId, // Pass user ID as a separate field
      }),
    );

    if (response.statusCode == 201) {
      // Barbershop created successfully
      Navigator.pop(context, true); // Pass true back to indicate success
    } else {
      // Show error message if failed
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Failed to create barbershop'),
      ));
    }
  }

  int extractUserIdFromToken(String accessToken) {
    final parts = accessToken.split('.');
    if (parts.length != 3) {
      throw Exception('Invalid access token');
    }
    final payload = parts[1];
    final decodedPayload = base64Url.decode(payload);
    final Map<String, dynamic> payloadMap =
        json.decode(utf8.decode(decodedPayload));
    return payloadMap['id'];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Create New Barbershop'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: nameController,
              decoration: InputDecoration(labelText: 'Name'),
            ),
            SizedBox(height: 20),
            TextField(
              controller: addressController,
              decoration: InputDecoration(labelText: 'Address'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                createBarbershop(context);
              },
              child: Text('Create Barbershop'),
            ),
          ],
        ),
      ),
    );
  }
}
