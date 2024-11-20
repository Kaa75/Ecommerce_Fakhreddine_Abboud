from typing import Any, Generic, Optional, TypeVar

from supabase import Client

from src.db.models import BaseModel
from src.utils.types import UuidStr

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


class BaseDAO(Generic[BaseModelType]):
    def __init__(
        self, client: Client, table: str, base_model: type[BaseModelType]
    ) -> None:
        self.client = client
        self.table = table
        self.base_model = base_model

    def get_by_query(
        self,
        **kwargs: Any,
    ) -> list[BaseModelType]:
        query = self.client.table(self.table).select("*")
        for key, value in kwargs.items():
            if value is not None:
                query = query.eq(key, value)
        data = query.execute()
        if not data.data:
            return []
        return [self.base_model.model_validate(item) for item in data.data]

    def create(self, model_data: dict[str, Any]) -> Optional[BaseModelType]:
        self.base_model.model_validate(model_data)
        data = self.client.table(self.table).insert(model_data).execute()
        if not data.data:
            return None
        return self.base_model.model_validate(data.data[0])

    def create_many(self, model_data: list[dict[str, Any]]) -> list[BaseModelType]:
        for _data in model_data:
            self.base_model.model_validate(_data)
        data = self.client.table(self.table).insert(model_data).execute()
        if not data.data:
            return []
        return [self.base_model.model_validate(item) for item in data.data]

    def get_by_id(self, id: UuidStr) -> Optional[BaseModelType]:
        data = self.client.table(self.table).select("*").eq("id", id).execute()
        if not data.data:
            return None
        return self.base_model.model_validate(data.data[0])

    def update(
        self, id: UuidStr, model_data: dict[str, Any]
    ) -> Optional[BaseModelType]:
        self.base_model.model_validate_partial(model_data)
        data = self.client.table(self.table).update(model_data).eq("id", id).execute()
        if not data.data:
            return None
        return self.base_model.model_validate(data.data[0])

    def delete(self, id: UuidStr) -> Optional[BaseModelType]:
        data = self.client.table(self.table).delete().eq("id", id).execute()
        if not data.data:
            return None
        return self.base_model.model_validate(data.data[0])
