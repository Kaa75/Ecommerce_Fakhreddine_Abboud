"""
Module for Review Data Access Object.
"""

from supabase import Client

from src.db.dao import BaseDAO
from src.db.models import Reviews
from src.db.tables import SupabaseTables


class ReviewDAO(BaseDAO[Reviews]):
    """
    Data Access Object for managing Reviews in the database.

    Inherits from BaseDAO to provide CRUD operations for Reviews.
    """

    def __init__(self, client: Client) -> None:
        """
        Initialize the ReviewDAO with a Supabase client.

        Args:
            client: The Supabase client instance.
        """
        super().__init__(client, SupabaseTables.REVIEWS, Reviews)
