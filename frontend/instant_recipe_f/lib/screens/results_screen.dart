import 'package:flutter/material.dart';
import '../models/recipe.dart';

class ResultsScreen extends StatelessWidget {

  final List<Recipe> recipes;

  const ResultsScreen({super.key, required this.recipes});

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(title: const Text("Generated Recipes")),

      body: ListView.builder(
        itemCount: recipes.length,

        itemBuilder: (context, index) {

          final recipe = recipes[index];

          return Card(
            margin: const EdgeInsets.all(10),

            child: Padding(
              padding: const EdgeInsets.all(12),

              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [

                  Text(
                    recipe.name,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 5),

                  Text("⭐ Score: ${recipe.score.toStringAsFixed(1)}"),

                  const SizedBox(height: 10),

                  const Text(
                    "Ingredients:",
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),

                  ...recipe.ingredients.map((item) =>
                      Text("- ${item["item"]} (${item["quantity"]})")
                  ),

                  const SizedBox(height: 10),

                  const Text(
                    "Steps:",
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),

                  ...recipe.steps.map((step) =>
                      Text(step)
                  ),

                  const SizedBox(height: 10),

                  Text("Time: ${recipe.time}"),
                  Text("Difficulty: ${recipe.difficulty}"),

                ],
              ),
            ),
          );
        },
      ),
    );
  }
}