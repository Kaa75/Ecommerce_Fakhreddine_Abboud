from supabase import Client

from src.db.dao import BaseDAO
from src.db.models import Reviews
from src.db.tables import SupabaseTables


class ReviewDAO(BaseDAO[Reviews]):
    def __init__(self, client: Client) -> None:
        super().__init__(client, SupabaseTables.REVIEWS, Reviews)
