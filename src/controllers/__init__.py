from .routers.customer import customers_router
from .routers.inventory import inventory_router
from .routers.reviews import review_router
from .routers.sales import sales_router
from .status import status_router

__all__ = [
    "status_router",
    "customers_router",
    "review_router",
    "inventory_router",
    "sales_router",
]
