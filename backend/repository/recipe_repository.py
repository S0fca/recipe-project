from model import (Recipe, Ingredient)
from typing import List

class RecipeRepository:
    def get_all_view(self, db) -> List[Recipe]:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM view_recipe_details")
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
                    created_at=row.get("created_at"),
                    ingredients=[]
                )

            ingredients_str = row.get("ingredients")
            if ingredients_str:
                ingredients = []
                for item in ingredients_str.split(", "):
                    try:
                        name, rest = item.split(":")
                        amount = ''.join(c for c in rest if c.isdigit() or c == '.')
                        unit = rest.replace(amount, '')
                        ingredients.append(
                            Ingredient(id=None, name=name, amount=float(amount), unit=unit)
                        )
                    except Exception:
                        continue
                recipes_map[rid].ingredients = ingredients

        return list(recipes_map.values())

    def add_recipe_with_ingredients(
        self,
        db,
        title: str,
        description: str,
        difficulty: str,
        is_vegetarian: bool,
        ingredients: List[Ingredient]
    ) -> int:
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO recipe (title, description, difficulty, is_vegetarian)
                VALUES (%s, %s, %s, %s)
            """, (title, description, difficulty, is_vegetarian))

            recipe_id = cursor.lastrowid

            for ing in ingredients:
                cursor.execute("SELECT id FROM ingredient WHERE name=%s", (ing.name,))
                row = cursor.fetchone()

                if row:
                    ing_id = row[0]
                else:
                    cursor.execute("INSERT INTO ingredient (name) VALUES (%s)", (ing.name,))
                    ing_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO recipe_ingredient (recipe_id, ingredient_id, amount, unit)
                    VALUES (%s, %s, %s, %s)
                """, (recipe_id, ing_id, ing.amount, ing.unit))

            return recipe_id
        finally:
            cursor.close()

    def delete_recipe(self, db, recipe_id: int) -> bool:
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM recipe WHERE id=%s", (recipe_id,))
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def update_recipe(
        self,
        db,
        recipe_id: int,
        title: str,
        description: str,
        difficulty: str,
        is_vegetarian: bool,
        ingredients: List[Ingredient]
    ) -> bool:
        cursor = db.cursor()
        try:
            cursor.execute("""
                UPDATE recipe
                SET title=%s, description=%s, difficulty=%s, is_vegetarian=%s
                WHERE id=%s
            """, (title, description, difficulty, is_vegetarian, recipe_id))

            if cursor.rowcount == 0:
                return False

            cursor.execute("DELETE FROM recipe_ingredient WHERE recipe_id=%s", (recipe_id,))

            for ing in ingredients:
                cursor.execute("SELECT id FROM ingredient WHERE name=%s", (ing.name,))
                row = cursor.fetchone()

                if row:
                    ing_id = row[0]
                else:
                    cursor.execute("INSERT INTO ingredient (name) VALUES (%s)", (ing.name,))
                    ing_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO recipe_ingredient (recipe_id, ingredient_id, amount, unit)
                    VALUES (%s, %s, %s, %s)
                """, (recipe_id, ing_id, ing.amount, ing.unit))

            return True
        finally:
            cursor.close()
