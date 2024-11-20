from src.auth.schemas import VerifyOTPRequest
from src.utils.responses.auth_response import AuthResponse
from src.session import Session
from src.db.dao import CustomerDAO
from src.db.models import customer


def verify_otp(request: VerifyOTPRequest, user_dao: CustomerDAO) -> AuthResponse:
    response = user_dao.client.auth.verify_otp(
        {"email": request.email, "token": request.otp, "type": "recovery"}
    )
    customer = customer.validate_supabase_user(response.customer)
    session = Session.validate_supabase_session(response.session)
    return AuthResponse(customer=customer, session=session)
