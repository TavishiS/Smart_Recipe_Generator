from pydantic import BaseModel

class IngredientCreate(BaseModel):
    name : str
    score : float

class IngredientDelete(BaseModel):
    name : str

class IngredientResponse(BaseModel):
    id : int
    name : str
    score : float

    class Config:
        from_attributes = True

class ConflictCheck(BaseModel):
    ingredients : list[str]

class RecipeRequest(BaseModel):
    ingredients : list[str]
    vegetarian : bool
    spicy : bool
    healthy : bool
    difficulty : str
    time : str