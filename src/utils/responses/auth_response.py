from typing import Optional

from pydantic import BaseModel as PydanticBaseModel

from src.db.models import Customer
from src.session import Session


class AuthResponse(PydanticBaseModel):
    customer: Optional[Customer] = None
    session: Optional[Session] = None
