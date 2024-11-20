from src.auth.schemas import ResetPasswordRequest
from src.common.responses import AuthResponse
from src.db.dao import UserDAO
from src.db.models import User


def reset_password(request: ResetPasswordRequest, user_dao: UserDAO) -> AuthResponse:
    response = user_dao.client.auth.update_user({"password": request.password})
    user = User.validate_supabase_user(response.user)
    return AuthResponse(user=user)
