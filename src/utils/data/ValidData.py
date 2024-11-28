"""
Module for validating data models using Pydantic.
"""

from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr

from src.utils.types import UuidStr


class ValidItems(PydanticBaseModel):
    """
    ValidItems model representing validated item data.
    """
    uuidStr: UuidStr = "00000000-0000-0000-0000-000000000000"
    emailStr: EmailStr = "email@mail.com"
    fullname: str = "First Last"
    username: str = "username"
    age: int = 20
    address: str = "1234 Main St"
    gender: str = "M"
    marital_status: str = "Single"
    wallet: float = 0.0


class ValidData:
    """
    Container for various valid data classes.
    """

    class Customer:
        """
        Customer data model with default valid values.
        """
        uuidStr: UuidStr = "00000000-0000-0000-0000-000000000000"
        emailStr: EmailStr = "email@mail.com"
        fullname: str = "First Last"
        username: str = "username"
        age: int = 20
        address: str = "1234 Main St"
        gender: str = "M"
        marital_status: str = "Single"
        wallet: float = 0.0

    class Inventory:
        """
        Inventory data model with default valid values.
        """
        uuidStr: UuidStr = "00000000-0000-0000-0000-000000000000"
        name: str = "Inventory Item"
        location: str = "Location"

    class TestObject:
        """
        TestObject model for testing purposes.
        """
        id = ValidItems().uuidStr
        name = ""
