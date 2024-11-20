from src.auth.schemas import OTPRequest
from src.utils.responses.auth_response import AuthResponse
from src.db.dao import CustomerDAO


def request_otp(request: OTPRequest, user_dao: CustomerDAO) -> AuthResponse:
    user_dao.client.auth.sign_in_with_otp({"email": request.email})
    return AuthResponse()
