"""
This module defines the router for handling review-related operations.
"""

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
"""Router instance for managing review endpoints."""

# API Calls:

# GET /reviews/
# Description: Retrieve all reviews.
# Method: GET
# URL: http://localhost:8000/reviews/

# POST /reviews/
# Description: Create a new review.
# Method: POST
# URL: http://localhost:8000/reviews/
# Body:
# {
#     "product_id": "uuid-string",
#     "customer_id": "uuid-string",
#     "rating": 5,
#     "comment": "Great product!"
# }

# POST /reviews/many
# Description: Create multiple new reviews.
# Method: POST
# URL: http://localhost:8000/reviews/many
# Body:
# [
#     {
#         "product_id": "uuid-string",
#         "customer_id": "uuid-string",
#         "rating": 4,
#         "comment": "Good quality."
#     },
#     {
#         "product_id": "uuid-string",
#         "customer_id": "uuid-string",
#         "rating": 3,
#         "comment": "Average experience."
#     }
# ]

# GET /reviews/{id}
# Description: Retrieve a review by ID.
# Method: GET
# URL: http://localhost:8000/reviews/{id}

# PUT /reviews/{id}
# Description: Update a review by ID.
# Method: PUT
# URL: http://localhost:8000/reviews/{id}
# Body:
# {
#     "rating": 4,
#     "comment": "Updated comment."
# }

# DELETE /reviews/{id}
# Description: Delete a review by ID.
# Method: DELETE
# URL: http://localhost:8000/reviews/{id}
