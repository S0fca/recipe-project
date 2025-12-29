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
