from fastapi import FastAPI, Depends
from database import engine, get_db
from sqlalchemy.orm import Session
import random
from fastapi.middleware.cors import CORSMiddleware

import models
import schemas
from recipe_generator import generate_recipes
from ingredient_rules import detect_conflicts
from recipe_ranker import rank_recipes
from cache import get_cached_recipe, save_recipe_cache

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"msg" : "Recipe app backend is running!"}

@app.get("/test_recipe")
def test_recipe():
    recipe = {
        "name" : "maggi",
        "ingredients" : [
            {"item" : "noodles", "quantity" : 1},
            {"item" : "tomato", "quantity" : 2},
            {"item" : "masala", "quantity" : 1}
        ],
        "steps" : [
            "Boil water for 2 min",
            "Add masala",
            "Add noodles",
            "Add chopped tomatoes and onion",
            "Serve hot"
        ]        
    }

    return recipe

@app.get("/ingredients", response_model=list[schemas.IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):

    ingredients = db.query(models.Ingredient).all()

    return ingredients

@app.post("/ingredients")
def add_ingredient(
    ingredient: schemas.IngredientCreate,
    db: Session = Depends(get_db)
):

    new_ingredient = models.Ingredient(
        name=ingredient.name,
        score=ingredient.score
    )

    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)

    return new_ingredient

@app.delete("/ingredients")
def remove_ingredient(
    ingredient: schemas.IngredientDelete,
    db: Session = Depends(get_db)
):

    ingredient_db = db.query(models.Ingredient).filter(
        models.Ingredient.name == ingredient.name
    ).first()

    if ingredient_db is None:
        return {"message": "Ingredient not found"}

    db.delete(ingredient_db)
    db.commit()

    return {"message": "Ingredient deleted"}

@app.post("/check_conflicts")
def check_conflicts(
    request: schemas.ConflictCheck,
    db: Session = Depends(get_db)
):

    conflicts = db.query(models.IngredientConflict).all()

    conflict_pairs = []

    ingredients = request.ingredients

    for c in conflicts:

        if c.ingredient1 in ingredients and c.ingredient2 in ingredients:
            conflict_pairs.append((c.ingredient1, c.ingredient2))

        elif c.ingredient2 in ingredients and c.ingredient1 in ingredients:
            conflict_pairs.append((c.ingredient2, c.ingredient1))

    return {
        "conflicts": conflict_pairs
    }

@app.get("/quote")
def get_quote(db: Session = Depends(get_db)):

    quotes = db.query(models.Quote).all()

    if not quotes:
        return {"quote": "No quotes available"}

    random_quote = random.choice(quotes)

    return {"quote": random_quote.quote}

@app.post("/generate_recipes")
def generate_recipe(request: schemas.RecipeRequest, db: Session = Depends(get_db)):

    data = {
        "ingredients": request.ingredients,
        "vegetarian": request.vegetarian,
        "spicy": request.spicy,
        "healthy": request.healthy,
        "difficulty": request.difficulty,
        "time": request.time
    }

    conflicts_user = detect_conflicts(data["ingredients"], db)

    if conflicts_user:
        return {
            "error" : "Conflicting ingredients detected...you cannot consume these together",
            "conflicts" : conflicts_user
        }

    cached = get_cached_recipe(db, data)

    if cached:
        return {"recipes": cached}
    else:
        recipes = generate_recipes(data)

        valid_recipes = []

        for recipe in recipes:
            ai_items = []
            for ingredient in recipe["ingredients"]:
                item = ingredient["item"]
                ai_items.append(item)
            conflicts_ai = detect_conflicts(ai_items, db)

            if not conflicts_ai:
                valid_recipes.append(recipe)  

        if valid_recipes:
            ranked_recipes = rank_recipes(valid_recipes, data)
            save_recipe_cache(db, data, ranked_recipes)
            return {"recipes": ranked_recipes}
        else:
            return {"msg" : "The recipes we can think of have ingredient conflicts. Please modify your ingredients."}