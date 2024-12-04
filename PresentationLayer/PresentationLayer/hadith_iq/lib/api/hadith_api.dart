import 'dart:convert';
import 'package:http/http.dart' as http;

class HadithService {
// Function to fetch semantic search results
  Future<List<String>> fetchSemanticSearchResults(
      String hadith, String projectName) async {
    final response = await http.post(
      Uri.parse(
          'http://127.0.0.1:8000/api/hadith/semanticSearch'), // Replace with your FastAPI URL
      headers: {'Content-Type': 'application/json; charset=UTF-8'},
      body: json.encode({
        'hadith': hadith,
        'project_name': projectName,
      }),
    );

    if (response.statusCode == 200) {
      // Decode the UTF-8 response body
      final String responseBody = utf8.decode(response.bodyBytes);

      // Parse JSON and extract results
      final List<dynamic> jsonResponse = json.decode(responseBody)['results'];

      // Extract the 'matn' field from each result into a List<String>
      final List<String> matns = jsonResponse.map((result) {
        return result['matn'].toString(); // Ensure it's a string
      }).toList();

      return matns; // Return the list of strings
    } else {
      throw Exception(
          'Failed to fetch search results. Status code: ${response.statusCode}');
    }
  }

  // API function to fetch expanded search results
  Future<List<String>> fetchExpandSearchResults(
      List<String> hadithList, String projectName) async {
    final response = await http.post(
      Uri.parse(
          'http://127.0.0.1:8000/api/hadith/expandSearch'), // Replace with your FastAPI URL
      headers: {'Content-Type': 'application/json; charset=UTF-8'},
      body: json.encode({
        'hadithTO': hadithList,
        'project_name': projectName,
      }),
    );

    if (response.statusCode == 200) {
      final String responseBody = utf8.decode(response.bodyBytes);
      final Map<String, dynamic> jsonResponse = json.decode(responseBody);

      // Extract 'matn' field from the results
      if (jsonResponse.containsKey('results') &&
          jsonResponse['results'] is List) {
        final List results = jsonResponse['results'];
        return results.map((result) => result.toString()).toList();
      } else {
        throw Exception(
            'Invalid response format: results key not found or invalid');
      }
    } else {
      throw Exception(
          'Failed to fetch search results. Status code: ${response.statusCode}');
    }
  }
}
