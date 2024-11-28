"""
This module defines the Reviews model for the Ecommerce application.
"""

from datetime import datetime
from typing import Optional

from src.db.models import BaseModel
from src.utils.types import RatingInt, UuidStr


class Reviews(BaseModel):
    """
    Represents a customer review for a product.

    Attributes:
        id: Unique identifier for the review.
        product_id: Identifier of the reviewed product.
        customer_id: Identifier of the customer who made the review.
        rating: Rating given by the customer.
        review: Textual review.
        created_at: Timestamp when the review was created.
        updated_at: Timestamp when the review was last updated.
    """
    id: Optional[UuidStr] = None
    product_id: UuidStr
    customer_id: UuidStr
    rating: RatingInt
    review: str
    created_at: datetime
    updated_at: datetime
