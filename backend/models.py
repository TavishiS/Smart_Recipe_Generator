from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from database import Base

class Ingredient(Base):

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    score = Column(Float)

class IngredientConflict(Base):

    __tablename__ = "ingredient_conflicts"

    id = Column(Integer, primary_key=True, index=True)
    ingredient1 = Column(String)
    ingredient2 = Column(String)

class Quote(Base):

    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    quote = Column(String)    


class RecipeCache(Base):

    __tablename__ = "recipe_cache"

    id = Column(Integer, primary_key=True, index=True)

    ingredients = Column(Text)

    vegetarian = Column(Boolean)

    spicy = Column(Boolean)

    healthy = Column(Boolean)

    difficulty = Column(String)

    time = Column(String)

    recipes_json = Column(Text)