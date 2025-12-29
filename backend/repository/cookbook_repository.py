from backend.model import Cookbook
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
