from typing import Any, TypeVar

from fastapi import status
from fastapi.responses import JSONResponse as FastAPIJSONResponse

from src.db.models import BaseModel

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


class APIResponse(FastAPIJSONResponse):
    media_type = "application/json"

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_200_OK,
        data: dict[str, Any] = {},
    ) -> None:
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
