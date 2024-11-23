from typing import Optional

from gotrue.types import User as GoTrueUser  # type: ignore
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

    @classmethod
    def validate_supabase_user(cls, customer: GoTrueUser) -> "Customer":
        return cls(
            id=customer.id,
            email=customer.email,
            fullname=customer.user_metadata["full_name"],
            username=customer.user_metadata["username"],
            age=customer.user_metadata["age"],
            gender=customer.user_metadata["gender"],
            address=customer.user_metadata["address"],
            marital_status=customer.user_metadata["marital_status"],
        )
