"""
Handles the process when a user forgets their password, including validating the user
and sending reset instructions via email.
"""

from fastapi import HTTPException, status

from src.auth.schemas import ForgetPasswordRequest
from src.db.dao import CustomerDAO
from src.utils.responses import AuthResponse


def forget_password(
    request: ForgetPasswordRequest, customer_dao: CustomerDAO
) -> AuthResponse:
    customer = customer_dao.get_by_query(email=request.email)[0]
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    customer_dao.client.auth.reset_password_email(request.email)
    return AuthResponse()
