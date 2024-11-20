from src.auth.schemas import VerifyOTPRequest
from src.db.dao import CustomerDAO
from src.session import Session
from src.db.models import Customer
from src.utils.responses.auth_response import AuthResponse


def verify_otp(request: VerifyOTPRequest, customer_dao: CustomerDAO) -> AuthResponse:
    response = customer_dao.client.auth.verify_otp(
        {"email": request.email, "token": request.otp, "type": "recovery"}
    )
    customer = Customer.validate_supabase_user(response.user)
    session = Session.validate_supabase_session(response.session)
    return AuthResponse(customer=customer, session=session)
