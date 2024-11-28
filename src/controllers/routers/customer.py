"""
This module defines the router for handling customer-related operations, including wallet management.
"""

from fastapi import Depends, status
from pydantic import PositiveFloat

from src.controllers.routers import BaseRouter
from src.db.dao import CustomerDAO
from src.db.dependencies import get_customer_dao
from src.db.models import Customer
from src.utils.responses.API_response import APIResponse
from src.utils.types import UuidStr

customers_router = BaseRouter[Customer](
    prefix="/customers",
    tags=["Customers"],
    name="Customer",
    model=Customer,
    get_dao=get_customer_dao,
).build_router()


@customers_router.put("/add_money/{id}")
async def add_money_to_wallet(
    id: UuidStr, money: PositiveFloat, dao: CustomerDAO = Depends(get_customer_dao)
) -> APIResponse:
    """
    Adds a specified amount of money to the customer's wallet.

    Args:
        id (UuidStr): The UUID of the customer.
        money (PositiveFloat): The amount of money to add.
        dao (CustomerDAO): The data access object for customers.

    Returns:
        APIResponse: The response indicating success or failure.
    """
    # Get the customer by ID using the DAO
    customer = dao.get_by_id(id)
    if not customer:
        return APIResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Customer not found",
        )
    prev_money = customer.wallet
    # Add money to the wallet
    new_wallet_amount = prev_money + money
    updated_customer = dao.update(id, {"wallet": new_wallet_amount})
    if updated_customer:
        return APIResponse(
            status_code=status.HTTP_200_OK,
            message="Money added to wallet",
            data={"wallet": updated_customer.wallet},
        )
    return APIResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Failed to update wallet",
    )
