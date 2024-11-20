from typing import Optional
from src.utils.types.UuidStr import UuidStr
from pydantic import BaseModel, EmailStr, PositiveInt, PositiveFloat
class Customer(BaseModel):
    id: Optional[UuidStr] = None
    fullname: str = None
    # email: EmailStr = None
    # username: str = None
    # age: PositiveInt = None
    # gender: str = None
    # address: str = None
    # marital_status: str = None
    # wallet: PositiveFloat = None
