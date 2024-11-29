"""
This module defines the BaseModel class as the base for all ORM models.
"""

from typing import Any

from pydantic import BaseModel as PydanticBaseModel

from src.utils.data import ValidData


class BaseModel(PydanticBaseModel):
    """
    Base model that provides common functionality for all models.

    Methods:
        model_validate_partial: Validates and partially updates the model with provided data.
    """
    @classmethod
    def model_validate_partial(cls, data: dict[str, Any]) -> "BaseModel":
        _data = {}
        for field in cls.model_fields:
            if field not in data:
                _data[field] = ValidData.__dict__[cls.__name__].__dict__[field]
            else:
                _data[field] = data[field]
        return cls.model_validate(_data)
