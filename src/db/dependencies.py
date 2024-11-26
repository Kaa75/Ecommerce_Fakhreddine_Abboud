from fastapi import Depends
from supabase import Client

from src.db.base import get_authenticated_client, get_unauthenticated_client
from src.db.dao import CustomerDAO, HistoryDAO, InventoryDAO, ReviewDAO


def get_customer_dao(client: Client = Depends(get_authenticated_client)) -> CustomerDAO:
    return CustomerDAO(client)


def get_history_dao(client: Client = Depends(get_authenticated_client)) -> HistoryDAO:
    return HistoryDAO(client)


def get_inventory_dao(
    client: Client = Depends(get_authenticated_client),
) -> InventoryDAO:
    return InventoryDAO(client)


def get_review_dao(client: Client = Depends(get_authenticated_client)) -> ReviewDAO:
    return ReviewDAO(client)


def get_customer_dao_unauthenticated(
    client: Client = Depends(get_unauthenticated_client),
) -> CustomerDAO:
    return CustomerDAO(client)
