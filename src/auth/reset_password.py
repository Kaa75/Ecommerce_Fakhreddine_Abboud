from src.auth.schemas import ResetPasswordRequest
from src.utils.responses import AuthResponse
from src.db.dao import CustomerDAO
from src.db.models import Customer


def reset_password(request: ResetPasswordRequest, user_dao: CustomerDAO) -> AuthResponse:
    response = user_dao.client.auth.update_user({"password": request.password})
    customer = Customer.validate_supabase_user(response.customer)
    return AuthResponse(customer=customer)
