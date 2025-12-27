from db_singleton import DatabaseConnection
from model import Recipe, Ingredient

class RecipeRepository:
    def __init__(self):
        self.db = DatabaseConnection().connect()

    def get_all_view(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM view_recipe_details")
        rows = cursor.fetchall()
        recipes = []
        for row in rows:
            ingredients_list = []
            if row["ingredients"]:
                for ing_str in row["ingredients"].split(", "):
                    parts = ing_str.split(":")
                    name = parts[0]
                    amount_unit = parts[1]
                    amount = float(''.join(filter(lambda x: x.isdigit() or x=='.', amount_unit)))
                    unit = ''.join(filter(lambda x: x.isalpha(), amount_unit))
                    ingredients_list.append(Ingredient(id=None, name=name, amount=amount, unit=unit))
            recipe = Recipe(
                id=row["recipe_id"],
                title=row["recipe_title"],
                description=row["recipe_description"],
                difficulty=row["difficulty"],
                is_vegetarian=row["is_vegetarian"],
                created_at=row["created_at"],
                ingredients=ingredients_list
            )
            recipes.append(recipe)
        cursor.close()
        return recipes

    def add_recipe_with_ingredients(self, title: str, description: str, difficulty: str,
                                    is_vegetarian: bool, ingredients: list[Ingredient]):
        try:
            self.db.commit()

            cursor = self.db.cursor()
            self.db.start_transaction()

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

            self.db.commit()
            cursor.close()

            return {"recipe_id": recipe_id, "title": title, "ingredients": [ing.to_dict() for ing in ingredients]}
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()
