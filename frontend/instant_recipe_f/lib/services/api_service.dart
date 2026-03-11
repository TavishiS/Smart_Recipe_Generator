import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {

  // static const String baseUrl = "http://localhost:8000";
  // static const String baseUrl = "https://smart-recipe-generator-4vdq.onrender.com";
  static const String baseUrl = "https://king-unretired-prepiously.ngrok-free.dev";

  static Future<List<dynamic>?> generateRecipes(
      Map<String, dynamic> data) async {

    final url = Uri.parse("$baseUrl/generate_recipes");

    final response = await http.post(
      url,
      headers: {
        "Content-Type": "application/json"
      },
      body: jsonEncode(data),
    );

    if (response.statusCode == 200) {

      final decoded = jsonDecode(response.body);

      if (decoded["recipes"] != null) {
        return decoded["recipes"];
      }

      return null;
    }

    return null;
  }

  static Future<String?> getQuote() async {

  final url = Uri.parse("$baseUrl/quote");

  final response = await http.get(url);

  if (response.statusCode == 200) {
    final decoded = jsonDecode(response.body);
    return decoded["quote"];
  }

  return null;
}
}