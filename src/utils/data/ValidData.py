"""
Module for validating data models using Pydantic.
"""

from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr, PositiveFloat, PositiveInt

from src.utils.types import UuidStr


class ValidItems(PydanticBaseModel):
    """
    ValidItems model representing validated item data.
    """

    uuidStr: UuidStr = "00000000-0000-0000-0000-000000000000"
    emailStr: EmailStr = "email@mail.com"
    fullname: str = "First Last"
    username: str = "username"
    age: PositiveInt = 20
    address: str = "1234 Main St"
    gender: str = "M"
    marital_status: str = "Single"
    wallet: PositiveFloat = 0.0
    product_name: str = "Product Name"
    price: PositiveFloat = 1.0
    quantity: PositiveInt = 0
    description: str = "Product Description"
    category: str = "electronics"
    rating: PositiveInt = 5

class ValidData:
    """
    Container for various valid data classes.
    """

    class Customer:
        """
        Customer data model with default valid values.
        """

        id = ValidItems().uuidStr
        email = ValidItems().emailStr
        fullname = ValidItems().fullname
        username = ValidItems().username
        age = ValidItems().age
        address = ValidItems().address
        gender = ValidItems().gender
        marital_status = ValidItems().marital_status
        wallet = ValidItems().wallet   

    class Inventory:
        """
        Inventory data model with default valid values.
        """

        id = ValidItems().uuidStr
        product_name = ValidItems().product_name
        category = ValidItems().category
        price = ValidItems().price
        quantity = ValidItems().quantity
        description = ValidItems().description

    class History:
        """
        History data model with default valid values.
        """
        id = ValidItems().uuidStr
        customer_id = ValidItems().uuidStr
        product_id = ValidItems().uuidStr
        quantity = ValidItems().quantity
        total = ValidItems().price
    
    class Reviews:
        """
        Reviews data model with default valid values.
        """
        id = ValidItems().uuidStr
        product_id = ValidItems().uuidStr
        customer_id = ValidItems().uuidStr
        rating = ValidItems().rating
        review = ValidItems().description

    class TestObject:
        """
        TestObject model for testing purposes.
        """

        id = ValidItems().uuidStr
        name = ""
