from datetime import datetime
from typing import Optional

from pydantic import PositiveFloat, PositiveInt

from src.db.models import BaseModel
from src.utils.types import UuidStr


class History(BaseModel):
    id: Optional[UuidStr] = None
    customer_id: UuidStr
    product_id: UuidStr
    quantity: PositiveInt
    total: PositiveFloat
    purchase_date: datetime
