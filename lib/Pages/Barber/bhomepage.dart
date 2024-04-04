import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:salonbuddy/Pages/Barber/Barbershopdetail.dart';
import 'package:salonbuddy/Pages/Barber/CreateBarbershopPage.dart';
import 'package:salonbuddy/Pages/Barber/UpdateBarbershopPage.dart';
import 'package:salonbuddy/Pages/auth/loginPage.dart';

class BHomePage extends StatefulWidget {
  final String accessToken;

  BHomePage({required this.accessToken});

  @override
  _BHomePageState createState() => _BHomePageState();
}

class _BHomePageState extends State<BHomePage> {
  List<dynamic> barbershops = [];

  @override
  void initState() {
    super.initState();
    fetchBarbershops();
  }

  Future<void> fetchBarbershops() async {
    try {
      final userId = extractUserIdFromToken(widget.accessToken);
      final apiUrl = 'http://192.168.10.69:8000/api/barbershops/user/$userId/';

      final response = await http.get(
        Uri.parse(apiUrl),
        headers: {'Authorization': 'Bearer ${widget.accessToken}'},
      );

      print('Status Code: ${response.statusCode}');
      print('Response Body: ${response.body}');

      if (response.statusCode == 200) {
        setState(() {
          barbershops = json.decode(response.body);
        });
      } else {
        throw Exception(
            'Failed to load barbershops. Status Code: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching barbershops: $e');
      throw Exception('Error fetching barbershops');
    }
  }

  String extractUserIdFromToken(String accessToken) {
    final parts = accessToken.split('.');
    if (parts.length != 3) {
      throw Exception('Invalid access token');
    }
    final payload = parts[1];
    final decodedPayload = base64Url.decode(payload);
    final Map<String, dynamic> payloadMap =
        json.decode(utf8.decode(decodedPayload));
    return payloadMap['id'].toString();
  }

  Future<void> deleteBarbershop(String id) async {
    final response = await http.delete(
      Uri.parse('http://192.168.10.69:8000/api/barbershops/$id/delete/'),
      headers: {'Authorization': 'Bearer ${widget.accessToken}'},
    );

    if (response.statusCode == 204) {
      // Barbershop deleted successfully, fetch the updated list
      fetchBarbershops();
    } else {
      throw Exception('Failed to delete barbershop');
    }
  }

  Future<void> navigateToCreateBarbershopPage(BuildContext context) async {
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => CreateBarbershopPage(
          accessToken: widget.accessToken,
        ),
      ),
    );
  }

  Future<void> navigateToUpdateBarbershopPage(
      BuildContext context, dynamic barbershop) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => UpdateBarbershopPage(
          barbershop: barbershop,
          accessToken: widget.accessToken,
        ),
      ),
    );

    // Fetch barbershops again after updating
    fetchBarbershops();
  }

  Future<void> navigateToBarbershopDetailsPage(
      BuildContext context, dynamic barbershop) async {
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => BarbershopDetailsPage(
          barbershopId: barbershop['id'], // Pass barbershopId here
          accessToken: widget.accessToken,
        ),
      ),
    );
  }

  Future<void> logout(BuildContext context) async {
    // Perform logout operation here, such as clearing session data
    // After logout, navigate back to the login page
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => LoginPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home Page'),
        actions: [
          IconButton(
            onPressed: () {
              logout(context);
            },
            icon: Icon(Icons.logout),
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome to the Barber Page!',
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                navigateToCreateBarbershopPage(context);
              },
              child: Text('Create Barbershop'),
            ),
            SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: barbershops.length,
                itemBuilder: (context, index) {
                  final barbershop = barbershops[index];
                  return ListTile(
                    title: Text(barbershop['name']),
                    subtitle: Text(barbershop['address']),
                    onTap: () {
                      navigateToBarbershopDetailsPage(context, barbershop);
                    },
                    onLongPress: () {
                      showDialog(
                        context: context,
                        builder: (BuildContext context) {
                          return AlertDialog(
                            title: Text('Delete Barbershop'),
                            content: Text(
                                'Are you sure you want to delete this barbershop?'),
                            actions: <Widget>[
                              TextButton(
                                onPressed: () => Navigator.of(context).pop(),
                                child: Text('Cancel'),
                              ),
                              TextButton(
                                onPressed: () {
                                  Navigator.of(context).pop();
                                  deleteBarbershop(barbershop['id'].toString());
                                },
                                child: Text('Delete'),
                              ),
                            ],
                          );
                        },
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
