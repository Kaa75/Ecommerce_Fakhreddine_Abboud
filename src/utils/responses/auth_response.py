from typing import Optional

from pydantic import BaseModel as PydanticBaseModel

from src.common.session import Session
from src.db.models import User


class AuthResponse(PydanticBaseModel):
    user: Optional[User] = None
    session: Optional[Session] = None
