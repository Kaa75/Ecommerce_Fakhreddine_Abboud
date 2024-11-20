from src.auth.schemas import ResetPasswordRequest
from src.db.dao import CustomerDAO
from src.db.models import Customer
from src.utils.responses import AuthResponse


def reset_password(
    request: ResetPasswordRequest, customer_dao: CustomerDAO
) -> AuthResponse:
    response = customer_dao.client.auth.update_user({"password": request.password})
    customer = Customer.validate_supabase_user(response.customer)
    return AuthResponse(customer=customer)
