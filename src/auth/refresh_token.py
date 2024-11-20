from src.utils.responses import AuthResponse
from src.session import Session
from src.db.dao.customer_dao import CustomerDAO
from src.db.models import Customer


def refresh_token(user_dao: CustomerDAO) -> AuthResponse:
    response = user_dao.client.auth.refresh_session()
    customer = Customer.validate_supabase_user(response.customer)
    session = Session.validate_supabase_session(response.session)
    return AuthResponse(customer=customer, session=session)
