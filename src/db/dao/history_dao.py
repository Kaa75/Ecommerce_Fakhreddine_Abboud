from supabase import Client

from src.db.dao import BaseDAO
from src.db.models import History
from src.db.tables import SupabaseTables


class HistoryDAO(BaseDAO[History]):
    def __init__(self, client: Client) -> None:
        super().__init__(client, SupabaseTables.HISTORY, History)
