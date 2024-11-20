from src.auth.schemas import OTPRequest
from src.db.dao import CustomerDAO
from src.utils.responses.auth_response import AuthResponse


def request_otp(request: OTPRequest, customer_dao: CustomerDAO) -> AuthResponse:
    customer_dao.client.auth.sign_in_with_otp({"email": request.email})
    return AuthResponse()
