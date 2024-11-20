from typing import Optional

from pydantic import EmailStr, PositiveFloat, PositiveInt

from src.db.models import BaseModel
from src.utils.types.UuidStr import UuidStr


class Customer(BaseModel):
    id: Optional[UuidStr] = None
    fullname: str
    email: EmailStr
    username: str
    age: PositiveInt
    gender: str
    address: str
    marital_status: str
    wallet: PositiveFloat = 0.0
