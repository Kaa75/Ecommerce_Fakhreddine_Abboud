import random
from typing import Any, Optional, get_type_hints
from unittest.mock import Mock
import uuid
import pytest
from fastapi import Query, status
from pydantic import BaseModel as PydanticBaseModel, create_model
from supabase import Client
from src.db.dao import BaseDAO
from src.db.models import BaseModel
from src.utils.data.ValidData import ValidItems
from src.controllers.routers import BaseRouter
from src.utils.responses import APIResponse
from src.utils.types import UuidStr
# from tests.fixtures.db.dao._base_dao import TestDAO
# from tests.fixtures.db.models._base_model import TestObject
class TestObject(BaseModel):
    __test__ = False
    id: Optional[UuidStr] = None
    name: str


@pytest.fixture
def test_objects(uuid_generator: Mock) -> list[TestObject]:
    return [
        TestObject(id=uuid_generator(), name="test_name_1"),
        TestObject(id=uuid_generator(), name="test_name_2"),
    ]


@pytest.fixture
def test_object1(test_objects: list[TestObject]) -> TestObject:
    return test_objects[0]


@pytest.fixture
def test_object2(test_objects: list[TestObject]) -> TestObject:
    return test_objects[1]

class TestDAO(BaseDAO[TestObject]):
    __test__ = False

    def __init__(self, client: Client) -> None:
        super().__init__(client, "TESTS", TestObject)


@pytest.fixture
def test_dao_successful(test_object1: TestObject, client: Client = Mock()) -> TestDAO:
    client = Mock()
    response = APIResponse(data=[test_object1.model_dump()], message="None")
    client.table("").select("").execute.return_value = response
    client.table("").select("").eq("", "").execute.return_value = response
    client.table("").select("").eq("", "").eq("", "").execute.return_value = response
    client.table("").insert("").execute.return_value = response
    client.table("").update("").eq("", "").execute.return_value = response
    client.table("").delete().eq("", "").execute.return_value = response
    return TestDAO(client)


@pytest.fixture
def test_dao_empty(client: Client = Mock()) -> TestDAO:
    client = Mock()
    response: APIResponse[None] = APIResponse(data=[], count=None)
    client.table("").select("").execute.return_value = response
    client.table("").select("").eq("", "").execute.return_value = response
    client.table("").select("").eq("", "").eq("", "").execute.return_value = response
    client.table("").insert("").execute.return_value = response
    client.table("").update("").eq("", "").execute.return_value = response
    client.table("").delete().eq("", "").execute.return_value = response
    return TestDAO(client)


@pytest.fixture
def test_dao_error(test_object1: TestObject, client: Client = Mock()) -> TestDAO:
    client = Mock()
    client.table("").select("").execute.side_effect = Exception("error")
    client.table("").select("").eq("", "").execute.side_effect = Exception("error")
    client.table("").select("").eq("", "").eq("", "").execute.side_effect = Exception(
        "error"
    )
    client.table("").insert("").execute.side_effect = Exception("error")
    client.table("").update("").eq("", "").execute.side_effect = Exception("error")
    client.table("").delete().eq("", "").execute.side_effect = Exception("error")
    return TestDAO(client)


@pytest.fixture
def router_successful(test_dao_successful: TestDAO) -> BaseRouter[TestObject]:
    return BaseRouter[TestObject](
        prefix="/test",
        tags=["test"],
        name="test",
        model=TestObject,
        get_dao=lambda: test_dao_successful,
    )


@pytest.fixture
def router_empty(test_dao_empty: TestDAO) -> BaseRouter[TestObject]:
    return BaseRouter[TestObject](
        prefix="/test",
        tags=["test"],
        name="test",
        model=TestObject,
        get_dao=lambda: test_dao_empty,
    )


@pytest.fixture
def router_error(test_dao_error: TestDAO) -> BaseRouter[TestObject]:
    return BaseRouter[TestObject](
        prefix="/test",
        tags=["test"],
        name="test",
        model=TestObject,
        get_dao=lambda: test_dao_error,
    )

@pytest.fixture
def uuid_generator() -> Mock:
    return Mock(side_effect=lambda: str(uuid.UUID(int=random.getrandbits(128))))

@pytest.fixture
def test_query() -> PydanticBaseModel:
    fields = dict(get_type_hints(TestObject))
    queries: dict[str, Any] = {
        key: (Optional[fields[key]], Query(None)) for key in fields if key != "id"
    }
    DynamicModel: type[PydanticBaseModel] = create_model("DynamicModel", **queries)
    return DynamicModel()


@pytest.mark.asyncio
class TestGetByQuery:
    async def test_get_by_query_successful(
        self,
        router_successful: BaseRouter[TestObject],
        test_dao_successful: TestDAO,
        test_query: PydanticBaseModel,
        test_object1: TestObject,
    ) -> None:
        response = await router_successful.get_by_query(test_query, test_dao_successful)
        res = eval(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert res == {
            "message": "'APIResponse' object has no attribute 'data'",
            "data": {},
        }

    async def test_get_by_query_error(
        self,
        router_error: BaseRouter[TestObject],
        test_dao_error: TestDAO,
        test_query: PydanticBaseModel,
    ) -> None:
        response = await router_error.get_by_query(query=test_query, dao=test_dao_error)
        res = eval(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert res == {"message": "error", "data": {}}


@pytest.mark.asyncio
class TestCreate:
    async def test_create_error(
        self, router_error: BaseRouter[TestObject], test_dao_error: TestDAO
    ) -> None:
        response = await router_error.create(
            request={"name": "test_name"}, dao=test_dao_error
        )
        res = eval(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert res == {"message": "error", "data": {}}


@pytest.mark.asyncio
class TestGetById:
    async def test_get_by_id_error(
        self, router_error: BaseRouter[TestObject], test_dao_error: TestDAO
    ) -> None:
        response = await router_error.get_by_id(
            id=ValidItems().uuidStr, dao=test_dao_error
        )
        res = eval(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert res == {"message": "error", "data": {}}


@pytest.mark.asyncio
class TestUpdate:
    async def test_update_error(
        self, router_error: BaseRouter[TestObject], test_dao_error: TestDAO
    ) -> None:
        response = await router_error.update(
            id=ValidItems().uuidStr, request={"name": "test_name"}, dao=test_dao_error
        )
        res = eval(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert res == {"message": "error", "data": {}}


@pytest.mark.asyncio
class TestDelete:
    async def test_delete_error(
        self, router_error: BaseRouter[TestObject], test_dao_error: TestDAO
    ) -> None:
        response = await router_error.delete(
            id=ValidItems().uuidStr, dao=test_dao_error
        )
        res = eval(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert res == {"message": "error", "data": {}}
