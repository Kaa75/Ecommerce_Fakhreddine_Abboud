"""
Provides functionality to refresh authentication tokens, ensuring continuous user sessions
by issuing new tokens upon request.
"""

from src.db.dao.customer_dao import CustomerDAO
from src.db.models import Customer
from src.session import Session
from src.utils.responses import AuthResponse


def refresh_token(customer_dao: CustomerDAO) -> AuthResponse:
    response = customer_dao.client.auth.refresh_session()
    customer = Customer.validate_supabase_user(response.user)
    session = Session.validate_supabase_session(response.session)
    return AuthResponse(customer=customer, session=session)
