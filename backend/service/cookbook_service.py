from backend.db_connection import get_connection
from backend.repository.cookbook_repository import CookbookRepository

class CookbookService:
    def __init__(self):
        self.repo = CookbookRepository()

    def get_all_cookbooks(self):
        db = get_connection()
        try:
            return self.repo.get_all_view(db)
        finally:
            db.close()

    def create_cookbook(self, name: str, description: str = ""):
        db = get_connection()
        try:
            db.start_transaction()
            cookbook = self.repo.create_cookbook(db, name, description)
            db.commit()
            return cookbook
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def add_recipe_to_cookbook(self, cookbook_id: int, recipe_id: int) -> dict:
        db = get_connection()
        try:
            db.start_transaction()
            added = self.repo.add_recipe_to_cookbook(db, cookbook_id, recipe_id)
            db.commit()

            if not added:
                return {"success": False, "error": "Recipe already in cookbook"}
            return {"success": True, "message": "Recipe added to cookbook"}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def get_cookbook_recipes(self, cookbook_id: int):
        db = get_connection()
        try:
            recipes = self.repo.get_recipes_in_cookbook(db, cookbook_id)
            return recipes
        finally:
            db.close()

    def import_cookbooks(self, cookbooks_data: list[dict]):
        db = get_connection()
        try:
            result = self.repo.import_cookbooks(db, cookbooks_data)
            return result
        finally:
            db.close()