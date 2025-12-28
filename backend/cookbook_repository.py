from db_singleton import DatabaseConnection
from model import Cookbook

class CookbookRepository:
    def __init__(self):
        self.db_conn = DatabaseConnection()

    def get_all_view(self):
        db = self.db_conn.connect()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM view_cookbook_summary")
        rows = cursor.fetchall()
        cursor.close()
        return [Cookbook(
            id=row["cookbook_id"],
            name=row["cookbook_name"],
            description=row["cookbook_description"],
            recipe_count=row["recipe_count"]
        ) for row in rows]

    def create_cookbook(self, name: str, description: str = "") -> Cookbook:
        db = self.db_conn.connect()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO cookbook (name, description) VALUES (%s, %s)",
            (name, description)
        )
        db.commit()
        return Cookbook(cursor.lastrowid, name, description)
