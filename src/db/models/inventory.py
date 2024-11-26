from typing import Optional

from pydantic import PositiveFloat, PositiveInt

from src.db.models import BaseModel
from src.utils.types import CategoryStr, UuidStr


class Inventory(BaseModel):
    id: Optional[UuidStr] = None
    product_name: str
    category: CategoryStr
    price: PositiveFloat
    quantity: PositiveInt
    description: str
