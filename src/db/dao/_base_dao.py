from typing import Any, Generic, Optional, TypeVar

from supabase import Client

from src.db.models import BaseModel
from src.utils.types import UuidStr

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


class BaseDAO(Generic[BaseModelType]):
    """
    Generic Data Access Object providing basic CRUD operations.

    Args:
        client (Client): Supabase client instance.
        table (str): Name of the table.
        base_model (type[BaseModelType]): Pydantic model for the table.
    """

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
        """
        Retrieve records matching the query parameters.

        Args:
            **kwargs: Arbitrary keyword arguments representing query filters.

        Returns:
            List of validated model instances.
        """
        query = self.client.table(self.table).select("*")
        for key, value in kwargs.items():
            if value is not None:
                query = query.eq(key, value)
        data = query.execute()
        if not data.data:
            return []
        return [self.base_model.model_validate(item) for item in data.data]

    def create(self, model_data: dict[str, Any]) -> Optional[BaseModelType]:
        """
        Create a new record in the table.

        Args:
            model_data (dict): Data for the new record.

        Returns:
            The created model instance or None if creation failed.
        """
        self.base_model.model_validate(model_data)
        data = self.client.table(self.table).insert(model_data).execute()
        if not data.data:
            return None
        return self.base_model.model_validate(data.data[0])

    def create_many(self, model_data: list[dict[str, Any]]) -> list[BaseModelType]:
        """
        Create multiple records in the table.

        Args:
            model_data (list of dict): List of data for the new records.

        Returns:
            List of created model instances.
        """
        for _data in model_data:
            self.base_model.model_validate(_data)
        data = self.client.table(self.table).insert(model_data).execute()
        if not data.data:
            return []
        return [self.base_model.model_validate(item) for item in data.data]

    def get_by_id(self, id: UuidStr) -> Optional[BaseModelType]:
        """
        Retrieve a record by its unique identifier.

        Args:
            id (UuidStr): The unique identifier of the record.

        Returns:
            The model instance if found, else None.
        """
        data = self.client.table(self.table).select("*").eq("id", id).execute()
        if not data.data:
            return None
        return self.base_model.model_validate(data.data[0])

    def update(
        self, id: UuidStr, model_data: dict[str, Any]
    ) -> Optional[BaseModelType]:
        """
        Update a record by its unique identifier.

        Args:
            id (UuidStr): The unique identifier of the record.
            model_data (dict): Data to update the record with.

        Returns:
            The updated model instance if successful, else None.
        """
        self.base_model.model_validate_partial(model_data)
        data = self.client.table(self.table).update(model_data).eq("id", id).execute()
        if not data.data:
            return None
        return self.base_model.model_validate(data.data[0])

    def delete(self, id: UuidStr) -> Optional[BaseModelType]:
        """
        Delete a record by its unique identifier.

        Args:
            id (UuidStr): The unique identifier of the record.

        Returns:
            The deleted model instance if successful, else None.
        """
        data = self.client.table(self.table).delete().eq("id", id).execute()
        if not data.data:
            return None
        return self.base_model.model_validate(data.data[0])
