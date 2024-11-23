import 'dart:math';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Row(
          children: [
            // Sidebar
            Container(
              width: 200,
              color: Colors.white,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Sidebar logo
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Image.asset(
                      'assets/logo.png', // Replace with your logo path
                      height: 40,
                    ),
                  ),
                  const Divider(),
                  // Import Button with File Picker
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      onPressed: () async {
                        await pickAndUploadFile(context);
                      },
                      icon: const Icon(Icons.add),
                      label: const Text('Import'),
                    ),
                  ),
                  const Divider(),
                  // Sidebar Items
                  SidebarItem(
                    icon: Icons.dashboard,
                    label: 'Projects',
                    onPressed: () {},
                  ),
                  SidebarItem(
                    icon: Icons.menu_book,
                    label: 'View all Hadith',
                    onPressed: () {},
                  ),
                  SidebarItem(
                    icon: Icons.person,
                    label: 'View all Narrators',
                    onPressed: () {},
                  ),
                ],
              ),
            ),
            // Main Content
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Top App Bar
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    color: const Color(0xFFD4C29C), // Beige Color
                    height: 50,
                    child: Row(
                      children: [
                        const Spacer(),
                        // Search Bar
                        Container(
                          width: 400,
                          height: 40,
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: Colors.grey),
                          ),
                          child: Row(
                            children: [
                              const Padding(
                                padding: EdgeInsets.symmetric(horizontal: 8),
                                child: Icon(Icons.search, color: Colors.grey),
                              ),
                              Expanded(
                                child: TextField(
                                  decoration: const InputDecoration(
                                    hintText: 'Search Hadith or Narrator',
                                    border: InputBorder.none,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  // Main Content Area
                  Expanded(
                    child: Center(
                      child: Opacity(
                        opacity: 0.1,
                        child: Image.asset(
                          'assets/background_logo.png', // Replace with your background logo path
                          height: 300,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> pickAndUploadFile(BuildContext context) async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();

    if (result != null) {
      String? filePath = result.files.single.path;

      if (filePath != null) {
        File file = File(filePath);
        try {
          // Show a loading dialog while uploading
          // Create multipart request
          var request = http.MultipartRequest(
            "POST",
            Uri.parse("http://127.0.0.1:8000/importfile"),
          );

          // Add the file to the request
          request.files.add(await http.MultipartFile.fromPath('file', file.path));

          // Send the request
          var response = await request.send();

          // Close the loading dialog
          //Navigator.of(context).pop();

          // Handle response
          if (response.statusCode == 200) {
            /*ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text("File uploaded successfully!")),
            );*/
          } else {
            /*ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text("Failed to upload file. Status code: ${response.statusCode}")),
            )*/
          }
        } catch (e) {
          //Navigator.of(context).pop(); // Close the loading dialog
          /*ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("Error: $e")),
          )*/
        }
      }
    } else {
      /*ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("File picker canceled")),
      );*/
    }
  }
}

class SidebarItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onPressed;

  const SidebarItem({
    required this.icon,
    required this.label,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
      child: GestureDetector(
        onTap: onPressed,
        child: Row(
          children: [
            Icon(icon, color: Colors.black),
            const SizedBox(width: 8),
            Text(label, style: const TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}

/*import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
       debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Row(
          children: [
            // Sidebar
            Container(
              width: 200,
              color: Colors.white,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Sidebar logo
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Image.asset(
                      'assets/logo.png', // Replace with your logo path
                      height: 40,
                    ),
                  ),
                  const Divider(),
                  // Import Button
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      onPressed: () {},
                      icon: const Icon(Icons.add),
                      label: const Text('Import'),
                    ),
                  ),
                  const Divider(),
                  // Sidebar Items
                  SidebarItem(
                    icon: Icons.dashboard,
                    label: 'Projects',
                    onPressed: () {},
                  ),
                  SidebarItem(
                    icon: Icons.menu_book,
                    label: 'View all Hadith',
                    onPressed: () {},
                  ),
                  SidebarItem(
                    icon: Icons.person,
                    label: 'View all Narrators',
                    onPressed: () {},
                  ),
                ],
              ),
            ),
            // Main Content
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Top App Bar
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    color: const Color(0xFFD4C29C), // Beige Color
                    height: 50,
                    child: Row(
                      children: [
                        const Spacer(),
                        // Search Bar
                        Container(
                          width: 400,
                          height: 40,
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: Colors.grey),
                          ),
                          child: Row(
                            children: [
                              const Padding(
                                padding: EdgeInsets.symmetric(horizontal: 8),
                                child: Icon(Icons.search, color: Colors.grey),
                              ),
                              Expanded(
                                child: TextField(
                                  decoration: const InputDecoration(
                                    hintText: 'Search Hadith or Narrator',
                                    border: InputBorder.none,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  // Main Content Area
                  Expanded(
                    child: Center(
                      child: Opacity(
                        opacity: 0.1,
                        child: Image.asset(
                          'assets/background_logo.png', // Replace with your background logo path
                          height: 300,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),

      /*title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    */
    );
  }
}

class SidebarItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onPressed;

  const SidebarItem({
    required this.icon,
    required this.label,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
      child: GestureDetector(
        onTap: onPressed,
        child: Row(
          children: [
            Icon(icon, color: Colors.black),
            const SizedBox(width: 8),
            Text(label, style: const TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      // This call to setState tells the Flutter framework that something has
      // changed in this State, which causes it to rerun the build method below
      // so that the display can reflect the updated values. If we changed
      // _counter without calling setState(), then the build method would not be
      // called again, and so nothing would appear to happen.
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // TRY THIS: Try changing the color here to a specific color (to
        // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
        // change color while the other colors stay the same.
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          // Column is also a layout widget. It takes a list of children and
          // arranges them vertically. By default, it sizes itself to fit its
          // children horizontally, and tries to be as tall as its parent.
          //
          // Column has various properties to control how it sizes itself and
          // how it positions its children. Here we use mainAxisAlignment to
          // center the children vertically; the main axis here is the vertical
          // axis because Columns are vertical (the cross axis would be
          // horizontal).
          //
          // TRY THIS: Invoke "debug painting" (choose the "Toggle Debug Paint"
          // action in the IDE, or press "p" in the console), to see the
          // wireframe for each widget.
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
*/