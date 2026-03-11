from database import SessionLocal
from models import Quote

db = SessionLocal()

quotes = [
    "Cooking is love made visible",
    "Good food is the foundation of happiness",
    "The secret ingredient is always love",
    "People who love to eat are always the best people",
]

for q in quotes:
    db.add(Quote(quote=q))

db.commit()
db.close()

print("Quotes inserted")