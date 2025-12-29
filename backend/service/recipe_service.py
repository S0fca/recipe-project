from backend.db_connection import get_connection
from backend.repository.recipe_repository import RecipeRepository
from backend.model import Ingredient

class RecipeService:
    def __init__(self):
        self.repo = RecipeRepository()

    def get_all_recipes(self):
        db = get_connection()
        try:
            return self.repo.get_all_view(db)
        finally:
            db.close()

    def add_recipe(self, title: str, description: str, difficulty: str,
                   is_vegetarian: bool, ingredients: list[Ingredient]):
        for ing in ingredients:
            if ing.amount < 0:
                raise ValueError(f"Ingredient '{ing.name}' has negative amount: {ing.amount}")

        db = get_connection()
        try:
            db.start_transaction()
            result = self.repo.add_recipe_with_ingredients(db, title, description, difficulty, is_vegetarian, ingredients)
            db.commit()
            return result
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def import_recipes(self, recipes_data: list[dict]):
        db = get_connection()
        imported = 0
        errors = []
        try:
            db.start_transaction()
            for idx, recipe_data in enumerate(recipes_data):
                try:
                    ingredients = []
                    for i in recipe_data.get("ingredients", []):
                        if i["amount"] < 0:
                            raise ValueError(f"Ingredient '{i['name']}' has negative amount: {i['amount']}")
                        ingredients.append(
                            Ingredient(id=None, name=i["name"], amount=i["amount"], unit=i["unit"])
                        )

                    self.repo.add_recipe_with_ingredients(
                        db,
                        title=recipe_data["title"],
                        description=recipe_data.get("description", ""),
                        difficulty=recipe_data.get("difficulty", "easy"),
                        is_vegetarian=recipe_data.get("is_vegetarian", False),
                        ingredients=ingredients
                    )
                    imported += 1
                except Exception as e:
                    errors.append({"index": idx, "title": recipe_data.get("title"), "error": str(e)})
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

        return {"imported": imported, "failed": len(errors), "errors": errors}
