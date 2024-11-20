from fastapi import HTTPException, status

from src.auth.schemas import ForgetPasswordRequest
from src.common.responses import AuthResponse
from src.db.dao import UserDAO


def forget_password(request: ForgetPasswordRequest, user_dao: UserDAO) -> AuthResponse:
    user = user_dao.get_by_query(email=request.email)[0]
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user_dao.client.auth.reset_password_email(request.email)
    return AuthResponse()
