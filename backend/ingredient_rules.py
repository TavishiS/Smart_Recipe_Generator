from sqlalchemy.orm import Session
import models


def detect_conflicts(ingredients, db: Session):

    ingredients = [i.lower() for i in ingredients]

    conflicts = db.query(models.IngredientConflict).all()

    conflicts_found = []

    for rule in conflicts:

        if rule.ingredient1 in ingredients and rule.ingredient2 in ingredients:

            conflicts_found.append(
                (rule.ingredient1, rule.ingredient2)
            )

    return conflicts_found