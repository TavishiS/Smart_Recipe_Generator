def ingredient_match_score(recipe, user_ingredients):

    recipe_items = [i["item"].lower() for i in recipe["ingredients"]]

    match = 0

    for ingredient in user_ingredients:
        if ingredient.lower() in recipe_items:
            match += 1

    return (match / len(user_ingredients)) * 30


def health_score(recipe, healthy_pref):

    if healthy_pref:
        return 40

    return 10


def difficulty_score(recipe, user_pref):

    if recipe["difficulty"] == user_pref:
        return 15

    return 5


# NEW helper function (prevents crash)
def extract_time(recipe):

    t = recipe["time"]

    if isinstance(t, int):
        return t

    if isinstance(t, str):
        try:
            return int(t.split()[0])
        except:
            return 30

    return 30


def time_score(recipe, user_pref):

    time_val = extract_time(recipe)

    if user_pref == "fast" and time_val <= 20:
        return 15

    if user_pref == "medium" and time_val <= 40:
        return 10

    return 5


def score_recipe(recipe, user_data):

    score = 0

    score += ingredient_match_score(
        recipe,
        user_data["ingredients"]
    )

    score += difficulty_score(
        recipe,
        user_data["difficulty"]
    )

    score += time_score(
        recipe,
        user_data["time"]
    )

    score += health_score(
        recipe,
        user_data["healthy"]
    )

    return score


# function to rank recipes
def rank_recipes(recipes, user_data):

    scored = []

    for recipe in recipes:

        s = score_recipe(recipe, user_data)

        recipe["score"] = s

        scored.append(recipe)

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored