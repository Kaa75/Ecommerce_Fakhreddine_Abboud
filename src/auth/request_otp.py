from src.auth.schemas import OTPRequest
from src.common.responses import AuthResponse
from src.db.dao import UserDAO


def request_otp(request: OTPRequest, user_dao: UserDAO) -> AuthResponse:
    user_dao.client.auth.sign_in_with_otp({"email": request.email})
    return AuthResponse()
