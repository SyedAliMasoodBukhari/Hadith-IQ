import 'package:http/http.dart' as http;
import 'dart:convert';

class ProjectService {

  // Function to fetch projects
  Future<List> fetchProjects() async {
    // final response = await http.get(Uri.parse('http://your_backend_url/projects'));

    // if (response.statusCode == 200) {
    //   List<dynamic> data = json.decode(response.body);

    //   // Transform the fetched data into a List of Lists
    //   return data.map<List<String>>((project) {
    //     return [project['name'], project['date']];
    //   }).toList();
    // } else {
    //   throw Exception('Failed to load projects');
    // }
    // Simulating an API response
    await Future.delayed(const Duration(seconds: 1)); // Simulate a delay
    return [
      ['Ali', '3 months ago'],
      ['test', '2 months ago'],
      ['Bukhari', '1 month ago']
    ];
  }

  // Method to send the new project to the backend
  Future<bool> addProject(String name, String date) async {
    final response = await http.post(
      Uri.parse('http://your_backend_url/projects'),
      headers: <String, String>{
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'name': name,
        'date': date,
      }),
    );

    if (response.statusCode == 201) {
      return true;
    } else {
      return false;
    }
  }
}