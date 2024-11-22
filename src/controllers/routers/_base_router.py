from enum import Enum
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    get_type_hints,
)

from fastapi import Depends, Query, status
from fastapi.routing import APIRouter
from pydantic import BaseModel as PydanticBaseModel
from pydantic import create_model

from src.controllers.schemas._base_schemas import BaseResponse
from src.db.dao import BaseDAO
from src.db.models import BaseModel
from src.utils.responses import APIResponse
from src.utils.types import UuidStr

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


class BaseRouter(Generic[BaseModelType]):
    def __init__(
        self,
        prefix: str,
        tags: Optional[list[Union[str, Enum]]],
        name: str,
        model: Type[BaseModelType],
        get_dao: Callable[[], BaseDAO[BaseModelType]],
    ):
        self.name = name
        self.request = {
            field: field for field in model.model_fields.keys() if field != "id"
        }
        self.request_many = [self.request]
        fields: dict[str, type] = dict(get_type_hints(model))
        queries: dict[str, Any] = {
            key: (Optional[fields[key]], Query(None)) for key in fields if key != "id"
        }
        self.query = create_model("DynamicModel", **queries, __base__=BaseModel)
        self.get_dao = get_dao
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
        )

    async def get_by_query(
        self, query: PydanticBaseModel, dao: BaseDAO[BaseModelType]
    ) -> APIResponse:
        try:
            items = dao.get_by_query(**query.model_dump())
            if items:
                return APIResponse(
                    status_code=status.HTTP_200_OK,
                    message=f"{self.name}s found",
                    data=BaseResponse[BaseModelType](items=items).model_dump(),
                )
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f"{self.name}s not found",
            )
        except Exception as e:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e),
            )

    async def create(
        self,
        request: dict[str, Any],
        dao: BaseDAO[BaseModelType],
    ) -> APIResponse:
        try:
            item = dao.create(request)
            if item:
                return APIResponse(
                    status_code=status.HTTP_201_CREATED,
                    message=f"{self.name} created",
                    data=BaseResponse[BaseModelType](items=[item]).model_dump(),
                )
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f"{self.name} not created",
            )
        except Exception as e:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e),
            )

    async def create_many(
        self,
        request: list[dict[str, Any]],
        dao: BaseDAO[BaseModelType],
    ) -> APIResponse:
        try:
            items = dao.create_many(request)
            if items:
                return APIResponse(
                    status_code=status.HTTP_201_CREATED,
                    message=f"{self.name}s created",
                    data=BaseResponse[BaseModelType](items=items).model_dump(),
                )
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f"{self.name}s not created",
            )
        except Exception as e:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e),
            )

    async def get_by_id(self, id: UuidStr, dao: BaseDAO[BaseModelType]) -> APIResponse:
        try:
            item = dao.get_by_id(id)
            if item:
                return APIResponse(
                    status_code=status.HTTP_200_OK,
                    message=f"{self.name} found",
                    data=BaseResponse[BaseModelType](items=[item]).model_dump(),
                )
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f"{self.name} not found",
            )
        except Exception as e:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e),
            )

    async def update(
        self,
        id: UuidStr,
        request: dict[str, Any],
        dao: BaseDAO[BaseModelType],
    ) -> APIResponse:
        try:
            item = dao.update(id, request)
            if item:
                return APIResponse(
                    status_code=status.HTTP_200_OK,
                    message=f"{self.name} updated",
                    data=BaseResponse[BaseModelType](items=[item]).model_dump(),
                )
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f"{self.name} not updated",
            )
        except Exception as e:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e),
            )

    async def delete(self, id: UuidStr, dao: BaseDAO[BaseModelType]) -> APIResponse:
        try:
            item = dao.delete(id)
            if item:
                return APIResponse(
                    status_code=status.HTTP_200_OK,
                    message=f"{self.name} deleted",
                    data=BaseResponse[BaseModelType](items=[item]).model_dump(),
                )
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f"{self.name} not deleted",
            )
        except Exception as e:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e),
            )

    def build_router(self) -> APIRouter:
        @self.router.get("/")
        async def get_by_query(
            query: PydanticBaseModel = Depends(self.query),
            dao: BaseDAO[BaseModelType] = Depends(self.get_dao),
        ) -> APIResponse:
            return await self.get_by_query(query, dao)

        @self.router.post("/")
        async def create(
            request: dict[str, Any] = self.request,
            dao: BaseDAO[BaseModelType] = Depends(self.get_dao),
        ) -> APIResponse:
            return await self.create(request, dao)

        @self.router.post("/many")
        async def create_many(
            request: list[dict[str, Any]] = self.request_many,
            dao: BaseDAO[BaseModelType] = Depends(self.get_dao),
        ) -> APIResponse:
            return await self.create_many(request, dao)

        @self.router.get("/{id}")
        async def get_by_id(
            id: UuidStr,
            dao: BaseDAO[BaseModelType] = Depends(self.get_dao),
        ) -> APIResponse:
            return await self.get_by_id(id, dao)

        @self.router.put("/{id}")
        async def update(
            id: UuidStr,
            request: dict[str, Any] = self.request,
            dao: BaseDAO[BaseModelType] = Depends(self.get_dao),
        ) -> APIResponse:
            return await self.update(id, request, dao)

        @self.router.delete("/{id}")
        async def delete(
            id: UuidStr,
            dao: BaseDAO[BaseModelType] = Depends(self.get_dao),
        ) -> APIResponse:
            return await self.delete(id, dao)

        return self.router
