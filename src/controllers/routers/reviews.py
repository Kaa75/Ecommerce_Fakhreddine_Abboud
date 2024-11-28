from src.controllers.routers import BaseRouter
from src.db.dependencies import get_review_dao
from src.db.models import Reviews

review_router = BaseRouter[Reviews](
    prefix="/reviews",
    tags=["Reviews"],
    name="Reviews",
    model=Reviews,
    get_dao=get_review_dao,
).build_router()
