import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class UpdateBarbershopPage extends StatefulWidget {
  final dynamic barbershop;
  final String accessToken;

  UpdateBarbershopPage({required this.barbershop, required this.accessToken});

  @override
  _UpdateBarbershopPageState createState() => _UpdateBarbershopPageState();
}

class _UpdateBarbershopPageState extends State<UpdateBarbershopPage> {
  late TextEditingController _nameController;
  late TextEditingController _addressController;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(text: widget.barbershop['name']);
    _addressController =
        TextEditingController(text: widget.barbershop['address']);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Update Barbershop'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _nameController,
              decoration: InputDecoration(labelText: 'Name'),
            ),
            SizedBox(height: 20),
            TextField(
              controller: _addressController,
              decoration: InputDecoration(labelText: 'Address'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                final String id = widget.barbershop['id'].toString();
                final String name = _nameController.text;
                final String address = _addressController.text;
                updateBarbershop(id, name, address);
              },
              child: Text('Update Barbershop'),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> updateBarbershop(String id, String name, String address) async {
    final response = await http.put(
      Uri.parse('http://192.168.10.69:8000/api/barbershops/$id/update/'),
      headers: {
        'Authorization': 'Bearer ${widget.accessToken}',
        'Content-Type': 'application/json',
      },
      body: json.encode({'name': name, 'address': address}),
    );

    if (response.statusCode == 200) {
      // Barbershop updated successfully, fetch the updated list
      Navigator.pop(context);
    } else {
      throw Exception('Failed to update barbershop');
    }
  }
}
