"""
Handles the logic for resetting a customer's password, including updating the password
in the database and validating the operation.
"""

from src.auth.schemas import ResetPasswordRequest
from src.db.dao import CustomerDAO
from src.db.models import Customer
from src.utils.responses import AuthResponse


def reset_password(
    request: ResetPasswordRequest, customer_dao: CustomerDAO
) -> AuthResponse:
    response = customer_dao.client.auth.update_user({"password": request.password})
    customer = Customer.validate_supabase_user(response.user)
    return AuthResponse(customer=customer)
