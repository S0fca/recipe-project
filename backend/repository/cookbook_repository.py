from backend.model import Cookbook, Recipe, Ingredient
from typing import List

class CookbookRepository:
    def get_all_view(self, db) -> List[Cookbook]:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM view_cookbook_summary")
            rows = cursor.fetchall()
        finally:
            cursor.close()

        return [
            Cookbook(
                id=row["cookbook_id"],
                name=row["cookbook_name"],
                description=row["cookbook_description"],
                recipe_count=row["recipe_count"]
            ) for row in rows
        ]

    def create_cookbook(self, db, name: str, description: str = "") -> Cookbook:
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO cookbook (name, description) VALUES (%s, %s)",
                (name, description)
            )
            return Cookbook(cursor.lastrowid, name, description)
        finally:
            cursor.close()

    def add_recipe_to_cookbook(self, db, cookbook_id: int, recipe_id: int) -> bool:
        cursor = db.cursor()
        try:
            cursor.execute(
                "SELECT 1 FROM recipe_cookbook WHERE cookbook_id=%s AND recipe_id=%s",
                (cookbook_id, recipe_id)
            )
            if cursor.fetchone():
                return False

            cursor.execute(
                "INSERT INTO recipe_cookbook (cookbook_id, recipe_id) VALUES (%s, %s)",
                (cookbook_id, recipe_id)
            )
            return True
        finally:
            cursor.close()

    def get_recipes_in_cookbook(self, db, cookbook_id: int) -> list[Recipe]:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    r.id AS recipe_id,
                    r.title AS recipe_title,
                    r.description AS recipe_description,
                    r.difficulty,
                    r.is_vegetarian,
                    i.name AS ingredient_name,
                    ri.amount AS ingredient_amount,
                    ri.unit AS ingredient_unit
                FROM recipe r
                JOIN recipe_cookbook rc ON r.id = rc.recipe_id
                LEFT JOIN recipe_ingredient ri ON r.id = ri.recipe_id
                LEFT JOIN ingredient i ON ri.ingredient_id = i.id
                WHERE rc.cookbook_id = %s
            """, (cookbook_id,))
            rows = cursor.fetchall()
        finally:
            cursor.close()

        recipes_map: dict[int, Recipe] = {}
        for row in rows:
            rid = row["recipe_id"]
            if rid not in recipes_map:
                recipes_map[rid] = Recipe(
                    id=rid,
                    title=row.get("recipe_title", ""),
                    description=row.get("recipe_description", ""),
                    difficulty=row.get("difficulty", "easy"),
                    is_vegetarian=row.get("is_vegetarian", False),
                    ingredients=[]
                )
            if row["ingredient_name"]:
                recipes_map[rid].ingredients.append(
                    Ingredient(
                        id=None,
                        name=row["ingredient_name"],
                        amount=row["ingredient_amount"],
                        unit=row["ingredient_unit"]
                    )
                )

        return list(recipes_map.values())

    def import_cookbooks(self, db, cookbooks_data: list[dict]) -> dict:
        imported = 0
        errors = []
        cursor = db.cursor()
        try:
            db.start_transaction()
            for idx, cb in enumerate(cookbooks_data):
                name = cb.get("name")
                description = cb.get("description", "")
                if not name:
                    errors.append({"index": idx, "error": "Missing name"})
                    continue
                try:
                    cursor.execute(
                        "INSERT INTO cookbook (name, description) VALUES (%s, %s)",
                        (name, description)
                    )
                    imported += 1
                except Exception as e:
                    errors.append({"index": idx, "name": name, "error": str(e)})
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            cursor.close()
        return {"imported": imported, "failed": len(errors), "errors": errors}