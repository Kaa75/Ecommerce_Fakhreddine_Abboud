"""
This module provides utilities for validating and handling UUID strings.
"""

import uuid
from typing import Annotated, Optional

from pydantic.functional_validators import BeforeValidator


def validate_uuid_str(v: Optional[str] = None) -> Optional[str]:
    """
    Validate that the provided string is a valid UUID.

    Args:
        v (Optional[str]): The UUID string to validate.

    Returns:
        Optional[str]: The validated UUID string or None if not provided.

    Raises:
        ValueError: If the string is not a valid UUID.
    """
    if not v:
        return None
    try:
        uuid.UUID(v)
    except ValueError:
        raise ValueError(f"{v} is an invalid UUID")
    return v


UuidStr = Annotated[str, BeforeValidator(validate_uuid_str)]
