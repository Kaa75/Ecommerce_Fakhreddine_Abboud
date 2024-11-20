from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr

from src.utils.types import UuidStr


class ValidItems(PydanticBaseModel):
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
    class Customer:
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
        uuidStr: UuidStr = "00000000-0000-0000-0000-000000000000"
        name: str = "Inventory Item"
        location: str = "Location"
        
    class TestObject:
        id = ValidItems().uuidStr
        name = ""
