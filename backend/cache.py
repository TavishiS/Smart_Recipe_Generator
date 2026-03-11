import json
from models import RecipeCache

def save_recipe_cache(db, data, recipes):

    entry = RecipeCache(
        ingredients=",".join(sorted(data["ingredients"])),
        vegetarian=data["vegetarian"],
        spicy=data["spicy"],
        healthy=data["healthy"],
        difficulty=data["difficulty"],
        time=data["time"],
        recipes_json=json.dumps(recipes)
    )

    db.add(entry)
    db.commit()

def get_cached_recipe(db, data):

    key = ",".join(sorted(data["ingredients"]))

    entry = db.query(RecipeCache).filter(
        RecipeCache.ingredients == key,
        RecipeCache.vegetarian == data["vegetarian"],
        RecipeCache.spicy == data["spicy"],
        RecipeCache.healthy == data["healthy"],
        RecipeCache.difficulty == data["difficulty"],
        RecipeCache.time == data["time"]
    ).first()

    if entry:
        return json.loads(entry.recipes_json)

    return None
