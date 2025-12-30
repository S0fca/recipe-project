class ReportRepository:
    def get_summary_report(self, db):
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS total_recipes FROM recipe")
            total_recipes = cursor.fetchone()["total_recipes"] or 0

            cursor.execute("SELECT COUNT(*) AS total_cookbooks FROM cookbook")
            total_cookbooks = cursor.fetchone()["total_cookbooks"] or 0

            cursor.execute("SELECT COUNT(*) AS total_ingredients FROM ingredient")
            total_ingredients = cursor.fetchone()["total_ingredients"] or 0

            cursor.execute("""
                SELECT AVG(ing_count) AS avg_ingredients_per_recipe
                FROM (
                    SELECT COUNT(*) AS ing_count
                    FROM recipe_ingredient
                    GROUP BY recipe_id
                ) AS sub
            """)
            avg_ingredients_per_recipe = float(cursor.fetchone()["avg_ingredients_per_recipe"] or 0)

            cursor.execute("""
                SELECT MIN(ing_count) AS min_ing, MAX(ing_count) AS max_ing
                FROM (
                    SELECT COUNT(*) AS ing_count
                    FROM recipe_ingredient
                    GROUP BY recipe_id
                ) AS sub
            """)
            row = cursor.fetchone() or {}
            min_ingredients_in_recipe = row.get("min_ing") or 0
            max_ingredients_in_recipe = row.get("max_ing") or 0

            cursor.execute("""
                SELECT 
                    AVG(rc_count) AS avg_recipes_per_cookbook,
                    MIN(rc_count) AS min_recipes_in_cookbook,
                    MAX(rc_count) AS max_recipes_in_cookbook
                FROM (
                    SELECT c.id AS cookbook_id, COUNT(rc.recipe_id) AS rc_count
                    FROM cookbook c
                    LEFT JOIN recipe_cookbook rc ON c.id = rc.cookbook_id
                    GROUP BY c.id
                ) AS sub
            """)
            row = cursor.fetchone() or {}
            avg_recipes_per_cookbook = float(row.get("avg_recipes_per_cookbook") or 0)
            min_recipes_in_cookbook = row.get("min_recipes_in_cookbook") or 0
            max_recipes_in_cookbook = row.get("max_recipes_in_cookbook") or 0

            return {
                "total_recipes": total_recipes,
                "total_cookbooks": total_cookbooks,
                "total_ingredients": total_ingredients,
                "avg_ingredients_per_recipe": avg_ingredients_per_recipe,
                "min_ingredients_in_recipe": min_ingredients_in_recipe,
                "max_ingredients_in_recipe": max_ingredients_in_recipe,
                "avg_recipes_per_cookbook": avg_recipes_per_cookbook,
                "min_recipes_in_cookbook": min_recipes_in_cookbook,
                "max_recipes_in_cookbook": max_recipes_in_cookbook,
            }
        finally:
            cursor.close()
