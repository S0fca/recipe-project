from db_connection import (get_connection)
from repository.recipe_repository import RecipeRepository
from model import Ingredient

class RecipeService:
    def __init__(self):
        self.repo = RecipeRepository()

    def get_all_recipes(self):
        db = get_connection()
        try:
            return self.repo.get_all_view(db)
        finally:
            db.close()

    def add_recipe(
        self,
        title: str,
        description: str,
        difficulty: str,
        is_vegetarian: bool,
        ingredients: list[Ingredient]
    ):
        for ing in ingredients:
            if ing.amount < 0:
                raise ValueError(
                    f"Ingredient '{ing.name}' has negative amount: {ing.amount}"
                )

        db = get_connection()
        try:
            db.start_transaction()
            recipe_id = self.repo.add_recipe_with_ingredients(
                db, title, description, difficulty, is_vegetarian, ingredients
            )
            db.commit()

            return {
                "recipe_id": recipe_id,
                "title": title,
                "ingredients": [ing.to_dict() for ing in ingredients]
            }
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
                            raise ValueError(
                                f"Ingredient '{i['name']}' has negative amount: {i['amount']}"
                            )
                        ingredients.append(
                            Ingredient(
                                id=None,
                                name=i["name"],
                                amount=i["amount"],
                                unit=i["unit"]
                            )
                        )

                    self.repo.add_recipe_with_ingredients(
                        db,
                        recipe_data["title"],
                        recipe_data.get("description", ""),
                        recipe_data.get("difficulty", "easy"),
                        recipe_data.get("is_vegetarian", False),
                        ingredients
                    )
                    imported += 1

                except Exception as e:
                    errors.append({
                        "index": idx,
                        "title": recipe_data.get("title"),
                        "error": str(e)
                    })

            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

        return {
            "imported": imported,
            "failed": len(errors),
            "errors": errors
        }

    def delete_recipe(self, recipe_id: int) -> dict:
        db = get_connection()
        try:
            db.start_transaction()
            deleted = self.repo.delete_recipe(db, recipe_id)

            if not deleted:
                db.rollback()
                return {"success": False, "error": "Recipe not found"}

            db.commit()
            return {"success": True, "message": "Recipe deleted"}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def edit_recipe(
        self,
        recipe_id: int,
        title: str,
        description: str,
        difficulty: str,
        is_vegetarian: bool,
        ingredients: list[Ingredient]
    ) -> dict:
        for ing in ingredients:
            if ing.amount < 0:
                return {
                    "success": False,
                    "error": f"Ingredient '{ing.name}' has negative amount"
                }

        db = get_connection()
        try:
            db.start_transaction()
            updated = self.repo.update_recipe(
                db, recipe_id, title, description, difficulty, is_vegetarian, ingredients
            )

            if not updated:
                db.rollback()
                return {"success": False, "error": "Recipe not found"}

            db.commit()
            return {"success": True, "message": "Recipe updated"}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()
