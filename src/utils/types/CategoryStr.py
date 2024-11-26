from typing import Annotated

from pydantic import BeforeValidator


def validate_category(value: str) -> str:
    if value.lower() not in ["electronics", "clothes", "accessories", "food"]:
        raise ValueError("Invalid category")
    return value.lower()


CategoryStr = Annotated[str, BeforeValidator(validate_category, "category")]
