"""Module defining the APIResponse class for standardized API responses."""

from typing import Any, TypeVar

from fastapi import status
from fastapi.responses import JSONResponse as FastAPIJSONResponse

from src.db.models import BaseModel

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


class APIResponse(FastAPIJSONResponse):
    """A custom JSON response class for API endpoints."""

    media_type = "application/json"

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_200_OK,
        data: dict[str, Any] = {},
    ) -> None:
        """Initialize the APIResponse with a message, status code, and optional data."""
        if not message:
            raise ValueError("message must be provided")
        if not status_code:
            raise ValueError("status_code must be provided")
        content = {
            "message": message,
            "data": data,
        }
        super().__init__(
            content=content,
            status_code=status_code,
            media_type=self.media_type,
        )
