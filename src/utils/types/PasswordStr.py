from typing import Annotated, Optional

from pydantic.functional_validators import BeforeValidator


def validate_password_str(v: Optional[str] = None) -> Optional[str]:
    if not v:
        return None
    try:
        if (
            len(v) < 8
            or not any(char.isupper() for char in v)
            or not any(char.islower() for char in v)
            or not any(char.isdigit() for char in v)
        ):
            raise ValueError
        return v
    except ValueError:
        raise ValueError(
            f"{v} is an invalid password, must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number"
        )


PasswordStr = Annotated[str, BeforeValidator(validate_password_str)]
