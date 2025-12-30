from backend.db_connection import get_connection
from backend.repository.report_repository import ReportRepository

class ReportService:
    def __init__(self):
        self.repo = ReportRepository()

    def get_summary(self):
        db = get_connection()
        try:
            return self.repo.get_summary_report(db)
        finally:
            db.close()
