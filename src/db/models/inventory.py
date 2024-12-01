"""
This module defines the Inventory model for managing product stocks.
"""

from typing import Optional

from pydantic import NonNegativeInt, PositiveFloat

from src.db.models import BaseModel
from src.utils.types import CategoryStr, UuidStr


class Inventory(BaseModel):
    """
    Represents the inventory details of a product.

    Attributes:
        id: Unique identifier for the inventory item.
        product_name: Name of the product.
        category: Category of the product.
        price: Price of the product.
        quantity: Available quantity in stock.
        description: Description of the product.
    """

    id: Optional[UuidStr] = None
    product_name: str
    category: CategoryStr
    price: PositiveFloat
    quantity: NonNegativeInt
    description: str
