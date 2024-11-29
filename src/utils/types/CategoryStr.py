"""Module for defining and validating category strings."""

from typing import Annotated

from pydantic import BeforeValidator


def validate_category(value: str) -> str:
    """Validate that the category is one of the allowed options.

    Args:
        value (str): The category to validate.

    Raises:
        ValueError: If the category is not valid.

    Returns:
        str: The validated category in lowercase.
    """
    if value.lower() not in ["electronics", "clothes", "accessories", "food"]:
        raise ValueError("Invalid category")
    return value.lower()


CategoryStr = Annotated[str, BeforeValidator(validate_category, "category")]
