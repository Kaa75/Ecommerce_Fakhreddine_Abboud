"""
This module defines the router for handling inventory-related operations.
"""

from src.controllers.routers import BaseRouter
from src.db.dependencies import get_inventory_dao
from src.db.models import Inventory

inventory_router = BaseRouter[Inventory](
    prefix="/inventory",
    tags=["Inventory"],
    name="Inventory",
    model=Inventory,
    get_dao=get_inventory_dao,
).build_router()
