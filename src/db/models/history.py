"""
This module defines the History model for tracking customer purchase history.
"""

from datetime import datetime
from typing import Optional

from pydantic import PositiveFloat, PositiveInt

from src.db.models import BaseModel
from src.utils.types import UuidStr


class History(BaseModel):
    """
    Represents a record of a customer's purchase.

    Attributes:
        id: Unique identifier for the history record.
        customer_id: Identifier of the customer.
        product_id: Identifier of the purchased product.
        quantity: Quantity purchased.
        total: Total amount of the purchase.
        purchase_date: Date and time of the purchase.
    """

    id: Optional[UuidStr] = None
    customer_id: UuidStr
    product_id: UuidStr
    quantity: PositiveInt
    total: PositiveFloat
