from datetime import datetime
from typing import Optional

from src.db.models import BaseModel
from src.utils.types import RatingInt, UuidStr


class Reviews(BaseModel):
    id: Optional[UuidStr] = None
    product_id: UuidStr
    customer_id: UuidStr
    rating: RatingInt
    review: str
    created_at: datetime
    updated_at: datetime
    status: str
