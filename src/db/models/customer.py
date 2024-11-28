"""
This module defines the Customer model for managing customer information.
"""

from typing import Optional

from gotrue.types import User as GoTrueUser  # type: ignore
from pydantic import EmailStr, PositiveFloat, PositiveInt

from src.db.models import BaseModel
from src.utils.types.UuidStr import UuidStr


class Customer(BaseModel):
    """
    Represents a customer in the Ecommerce system.

    Attributes:
        id: Unique identifier for the customer.
        fullname: Full name of the customer.
        email: Email address of the customer.
        username: Username chosen by the customer.
        age: Age of the customer.
        gender: Gender of the customer.
        address: Physical address of the customer.
        marital_status: Marital status of the customer.
        wallet: Balance in the customer's wallet.
    """
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
        """
        Validate and create a Customer instance from a GoTrueUser.

        Args:
            customer: The GoTrueUser instance to validate.

        Returns:
            A Customer instance with validated data.
        """
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
