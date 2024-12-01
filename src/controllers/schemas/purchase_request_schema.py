from pydantic import BaseModel, PositiveInt
from src.utils.types import UuidStr

class PurchaseRequest(BaseModel):
    product_id: UuidStr
    customer_id: UuidStr
    quantity: PositiveInt
