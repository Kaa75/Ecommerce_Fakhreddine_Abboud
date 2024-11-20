from src.common.responses import AuthResponse
from src.common.session import Session
from src.db.dao.user_dao import UserDAO
from src.db.models import User


def refresh_token(user_dao: UserDAO) -> AuthResponse:
    response = user_dao.client.auth.refresh_session()
    user = User.validate_supabase_user(response.user)
    session = Session.validate_supabase_session(response.session)
    return AuthResponse(user=user, session=session)
