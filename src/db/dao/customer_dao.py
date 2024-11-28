"""
Module for Customer Data Access Object.
"""

from supabase import Client

from src.db.dao import BaseDAO
from src.db.models import Customer
from src.db.tables import SupabaseTables


class CustomerDAO(BaseDAO[Customer]):
    """
    Data Access Object for managing Customers in the database.

    Inherits from BaseDAO to provide CRUD operations for Customers.
    """

    def __init__(self, client: Client) -> None:
        """
        Initialize the CustomerDAO with a Supabase client.

        Args:
            client: The Supabase client instance.
        """
        super().__init__(client, SupabaseTables.CUSTOMERS, Customer)
