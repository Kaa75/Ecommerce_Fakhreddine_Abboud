import uuid
from typing import Annotated, Optional

from pydantic.functional_validators import BeforeValidator


def validate_uuid_str(v: Optional[str] = None) -> Optional[str]:
    if not v:
        return None
    try:
        uuid.UUID(v)
    except ValueError:
        raise ValueError(f"{v} is an invalid UUID")
    return v


UuidStr = Annotated[str, BeforeValidator(validate_uuid_str)]
