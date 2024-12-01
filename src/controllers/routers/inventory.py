"""
This module defines the router for handling inventory-related operations.
"""

from fastapi import Depends, status
from pydantic import PositiveInt

from src.controllers.routers import BaseRouter
from src.db.dao._base_dao import BaseDAO
from src.db.dependencies import get_inventory_dao
from src.db.models import Inventory
from src.utils.responses.API_response import APIResponse
from src.utils.types import UuidStr

inventory_router = BaseRouter[Inventory](
    prefix="/inventory",
    tags=["Inventory"],
    name="Inventory",
    model=Inventory,
    get_dao=get_inventory_dao,
).build_router()


@inventory_router.put("/{id}")
async def deduct_goods(
    id: UuidStr,
    amount: PositiveInt,
    inventory_dao: BaseDAO[Inventory] = Depends(get_inventory_dao),
) -> APIResponse:
    """
    Deducts a specified amount of goods from the inventory.

    Args:
        id (UuidStr): The unique identifier of the inventory item.
        amount (PositiveInt): The amount of goods to deduct.
        inventory_dao (BaseDAO[Inventory], optional): The DAO for Inventory. Defaults to Depends(get_inventory_dao).

    Returns:
        APIResponse: The response containing the result of the deduction operation.
    """
    try:
        product = inventory_dao.get_by_id(id)
        if not product:
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Inventory not found",
            )
        curr_stock = product.quantity
        if curr_stock < amount:
            return APIResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Not enough stock in inventory",
                data={"stock": curr_stock},
            )
        new_stock = curr_stock - amount
        updated_inventory = inventory_dao.update(id, {"stock": new_stock})

        assert updated_inventory is not None

        return APIResponse(
            status_code=status.HTTP_200_OK,
            message="Goods deducted successfully",
            data=updated_inventory.model_dump(),
        )
    except Exception as e:
        return APIResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e),
        )
