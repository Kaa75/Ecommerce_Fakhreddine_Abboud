from src.controllers.routers._base_router import BaseRouter
from src.db.dependencies import get_customer_dao
from src.db.models import Customer

customers_router = BaseRouter[Customer](
    prefix="/customers",
    tags=["Customers"],
    name="Customer",
    model=Customer,
    get_dao=get_customer_dao,
).build_router()
