from db_singleton import DatabaseConnection
from model import Recipe, Ingredient

class RecipeRepository:
    def __init__(self):
        self.db_conn = DatabaseConnection()

    def get_all_view(self) -> list[Recipe]:
        db = self.db_conn.connect()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM view_recipe_details")
            rows = cursor.fetchall()
        finally:
            if cursor:
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
            ingredients = []
            if ingredients_str:
                for item in ingredients_str.split(", "):
                    try:
                        name, rest = item.split(":")
                        amount = ''.join([c for c in rest if c.isdigit() or c == '.'])
                        unit = rest.replace(amount, '')
                        ingredients.append(Ingredient(id=None, name=name, amount=float(amount), unit=unit))
                    except Exception:
                        continue
            recipes_map[rid].ingredients = ingredients

        return list(recipes_map.values())


    def add_recipe_with_ingredients(self, title: str, description: str, difficulty: str,
                                    is_vegetarian: bool, ingredients: list[Ingredient]):
        try:
            db = self.db_conn.connect()
            cursor = db.cursor()
            db.start_transaction()

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

            db.commit()
            cursor.close()

            return {"recipe_id": recipe_id, "title": title, "ingredients": [ing.to_dict() for ing in ingredients]}
        except Exception as e:
            db.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
