from typing import Any, Dict, Generic, List, TypeVar

from fastapi import APIRouter, Depends, status

from src.db.dao import BaseDAO
from src.db.dependencies import get_customer_dao, get_history_dao, get_inventory_dao
from src.db.models import Customer, History, Inventory, BaseModel
from src.utils.responses import APIResponse
from src.utils.types import UuidStr

ModelType = TypeVar("ModelType", bound=BaseModel)

sales_router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


@sales_router.get("/goods")
async def get_goods(
    dao: BaseDAO[Inventory] = Depends(get_inventory_dao),
) -> APIResponse:
    try:
        all_goods = dao.get_by_query()
        if not all_goods:
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="No goods found",
            )
        goods_name_price = {}
        for good in all_goods:
            goods_name_price[good.product_name] = good.price

        return APIResponse(
            status_code=status.HTTP_200_OK,
            message="Goods found",
            data=goods_name_price,
        )
    except Exception as e:
        return APIResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e),
        )


@sales_router.get("/good")
async def get_good(
    name: str, dao: BaseDAO[Inventory] = Depends(get_inventory_dao)
) -> APIResponse:
    try:
        good = dao.get_by_query(product_name=name)
        if not good:
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="No good found",
            )
        return APIResponse(
            status_code=status.HTTP_200_OK,
            message="Good found",
            data=merge_dicts(good),
        )
    except Exception as e:
        return APIResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e),
        )


@sales_router.post("/purchase")
async def purchase_good(
    name: str,
    quantity: int,
    customer_id: UuidStr,
    inventory_dao: BaseDAO[Inventory] = Depends(get_inventory_dao),
    history_dao: BaseDAO[History] = Depends(get_history_dao),
    customer_dao: BaseDAO[Customer] = Depends(get_customer_dao),
) -> APIResponse:
    try:
        good = inventory_dao.get_by_query(product_name=name)[0]
        if not good:
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="No good found",
            )
        if good.quantity < quantity:
            return APIResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Not enough stock available",
            )

        total_price = good.price * quantity
        customer = customer_dao.get_by_id(customer_id)
        if not customer:
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Customer not found",
            )
        if customer.wallet < total_price:
            return APIResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Not enough money in wallet",
            )

        updated_customer = customer_dao.update(
            customer_id, {"wallet": customer.wallet - total_price}
        )

        assert good.id is not None
        updated_inventory = inventory_dao.update(
            good.id, {"quantity": good.quantity - quantity}
        )

        history = history_dao.create(
            {
                "customer_id": customer_id,
                "product_id": good.id,
                "quantity": quantity,
                "total_price": total_price,
            }
        )

        return APIResponse(
            status_code=status.HTTP_200_OK,
            message="Purchase successful",
            data={
                "customer": updated_customer,
                "inventory": updated_inventory,
                "history": history,
            },
        )
    except Exception as e:
        return APIResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e),
        )


@sales_router.get("/customer={id}/history")
async def get_customer_history(
    id: UuidStr, dao: BaseDAO[History] = Depends(get_history_dao)
) -> APIResponse:
    try:
        history = dao.get_by_query(customer_id=id)
        if not history:
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="No history found",
            )
        return APIResponse(
            status_code=status.HTTP_200_OK,
            message="History found",
            data=merge_dicts(history),
        )
    except Exception as e:
        return APIResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e),
        )


@sales_router.get("/product={id}/history")
async def get_product_history(
    id: UuidStr, dao: BaseDAO[History] = Depends(get_history_dao)
) -> APIResponse:
    try:
        history = dao.get_by_query(product_id=id)
        if not history:
            return APIResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="No history found",
            )
        return APIResponse(
            status_code=status.HTTP_200_OK,
            message="History found",
            data=merge_dicts(history),
        )
    except Exception as e:
        return APIResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e),
        )


def merge_dicts(dict_list: List[ModelType]) -> Dict[str, Any]:  # type: ignore
    result: Dict[str, Any] = {}
    for dictionary in dict_list:
        result.update(dictionary)
    return result
