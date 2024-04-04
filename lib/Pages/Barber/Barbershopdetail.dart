import 'package:flutter/material.dart';
import 'package:salonbuddy/Pages/Barber/Styleofcut.dart';
import 'package:salonbuddy/Pages/Barber/createstyleofcut.dart';

class BarbershopDetailsPage extends StatelessWidget {
  final int barbershopId;
  final String accessToken;

  BarbershopDetailsPage({
    required this.barbershopId,
    required this.accessToken,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Barbershop Details'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Barbershop Details'),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => StyleOfCutPage(
                      barbershopId: barbershopId,
                      accessToken: accessToken,
                    ),
                  ),
                );
              },
              child: Text('Navigate to Style of Cut Page'),
            ),
          ],
        ),
      ),
    );
  }
}
