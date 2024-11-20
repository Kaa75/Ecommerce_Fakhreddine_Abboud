from typing import Optional

from pydantic import BaseModel as PydanticBaseModel

from src.session import Session
from src.db.models import Customer


class AuthResponse(PydanticBaseModel):
    customer: Optional[Customer] = None
    session: Optional[Session] = None
