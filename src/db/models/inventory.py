from typing import Optional

from src.db.models import BaseModel
from src.utils.types import UuidStr


class Inventory(BaseModel):
    id: Optional[UuidStr] = None
    name: str = ""
    location: str = ""
