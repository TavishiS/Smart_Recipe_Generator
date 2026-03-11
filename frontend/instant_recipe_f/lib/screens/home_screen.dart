import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/recipe.dart';
import 'results_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

  final TextEditingController ingredientController = TextEditingController();

  List<String> ingredients = [];

  bool vegetarian = true;
  bool spicy = false;
  bool healthy = true;

  String difficulty = "easy";
  String time = "fast";

  void addIngredient() {
    if (ingredientController.text.isNotEmpty) {
      setState(() {
        ingredients.add(ingredientController.text);
      });
      ingredientController.clear();
    }
  }

  Future<void> generateRecipes() async {

    if (ingredients.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please add at least one ingredient")),
      );
      return;
    }

    final data = {
      "ingredients": ingredients,
      "vegetarian": vegetarian,
      "spicy": spicy,
      "healthy": healthy,
      "difficulty": difficulty,
      "time": time
    };

    final response = await ApiService.generateRecipes(data);

    if (response != null) {

      List<Recipe> recipes =
          response.map((r) => Recipe.fromJson(r)).toList();

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultsScreen(recipes: recipes),
        ),
      );

    } else {

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Could not generate recipes"),
        ),
      );

    }
  }

  Future<void> showQuote() async {

    final quote = await ApiService.getQuote();

    if (quote != null) {

      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text("Surprise quote:)"),
          content: Text(quote),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("Close"),
            )
          ],
        ),
      );

    } else {

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Could not fetch quote"),
        ),
      );

    }
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("Smart Recipe Generator"),
        centerTitle: true,
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),

        child: SingleChildScrollView(

          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,

            children: [

              /// BEAUTIFUL FOOD HEADER

              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.orange.shade200,
                  borderRadius: BorderRadius.circular(20),
                ),

                child: Column(
                  children: const [

                    Icon(
                      Icons.restaurant_menu,
                      size: 60,
                      color: Colors.white,
                    ),

                    SizedBox(height: 10),

                    Text(
                      "Smart Recipe Generator",
                      style: TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),

                    Text(
                      "Turn ingredients into delicious meals",
                      style: TextStyle(color: Colors.white),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 25),

              /// INGREDIENT INPUT

              const Text(
                "Add Ingredients",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),

              const SizedBox(height: 10),

              TextField(
                controller: ingredientController,

                decoration: InputDecoration(

                  labelText: "Enter ingredient",

                  suffixIcon: IconButton(
                    icon: const Icon(Icons.add),
                    onPressed: addIngredient,
                  ),

                  border: const OutlineInputBorder(),
                ),
              ),

              const SizedBox(height: 15),

              /// INGREDIENT CHIPS

              Wrap(
                spacing: 8,
                children: ingredients.map((item) {

                  return Chip(
                    label: Text(item),
                    backgroundColor: Colors.orange.shade100,

                    deleteIcon: const Icon(Icons.close),

                    onDeleted: () {
                      setState(() {
                        ingredients.remove(item);
                      });
                    },
                  );

                }).toList(),
              ),

              const SizedBox(height: 25),

              /// PREFERENCES

              const Text(
                "Preferences",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),

              const SizedBox(height: 10),

              SwitchListTile(
                title: const Text("Vegetarian"),
                value: vegetarian,
                onChanged: (value) {
                  setState(() {
                    vegetarian = value;
                  });
                },
              ),

              SwitchListTile(
                title: const Text("Spicy"),
                value: spicy,
                onChanged: (value) {
                  setState(() {
                    spicy = value;
                  });
                },
              ),

              SwitchListTile(
                title: const Text("Healthy"),
                value: healthy,
                onChanged: (value) {
                  setState(() {
                    healthy = value;
                  });
                },
              ),

              const SizedBox(height: 20),

              /// DIFFICULTY

              const Text(
                "Difficulty",
                style: TextStyle(fontSize: 16),
              ),

              DropdownButton<String>(
                value: difficulty,

                items: ["easy", "difficult"]
                    .map(
                      (item) => DropdownMenuItem(
                        value: item,
                        child: Text(item),
                      ),
                    )
                    .toList(),

                onChanged: (value) {
                  setState(() {
                    difficulty = value!;
                  });
                },
              ),

              const SizedBox(height: 20),

              /// COOKING TIME

              const Text(
                "Cooking Time",
                style: TextStyle(fontSize: 16),
              ),

              DropdownButton<String>(
                value: time,

                items: ["fast", "time-taking"]
                    .map(
                      (item) => DropdownMenuItem(
                        value: item,
                        child: Text(item),
                      ),
                    )
                    .toList(),

                onChanged: (value) {
                  setState(() {
                    time = value!;
                  });
                },
              ),

              const SizedBox(height: 30),

              /// GENERATE BUTTON

              Center(
                child: ElevatedButton(
                  onPressed: generateRecipes,
                  child: const Text("Generate Recipes"),
                ),
              ),

              const SizedBox(height: 20),

              /// QUOTE BUTTON

              Center(
                child: ElevatedButton(
                  onPressed: showQuote,
                  child: const Text("Click to see a beautiful quote"),
                ),
              ),

              const SizedBox(height: 40),
            ],
          ),
        ),
      ),
    );
  }
}