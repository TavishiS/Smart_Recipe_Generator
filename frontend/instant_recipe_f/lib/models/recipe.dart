class Recipe {
  final String name;
  final List ingredients;
  final List steps;
  final String time;
  final String difficulty;
  final double score;

  Recipe({
    required this.name,
    required this.ingredients,
    required this.steps,
    required this.time,
    required this.difficulty,
    required this.score,
  });

  factory Recipe.fromJson(Map<String, dynamic> json) {
    return Recipe(
      name: json["name"],
      ingredients: json["ingredients"],
      steps: json["steps"],
      time: json["time"],
      difficulty: json["difficulty"],
      score: (json["score"] ?? 0).toDouble(),
    );
  }
}