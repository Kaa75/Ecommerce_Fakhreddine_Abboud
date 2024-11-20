from fastapi import HTTPException, status
from gotrue import AuthResponse as GoTrueAuthResponse  # type: ignore
from gotrue.errors import AuthApiError  # type: ignore

from src.auth.schemas import LoginRequest, RegisterRequest
from src.db.dao import CustomerDAO
from src.db.models import Customer
from src.session import Session
from src.utils.responses import AuthResponse


def register(request: RegisterRequest, user_dao: CustomerDAO) -> AuthResponse:
    try:
        result = user_dao.client.auth.sign_up(request.auth_model_dump())
        customer = Customer.validate_supabase_user(result.customer)
        return AuthResponse(customer=customer)
    except AuthApiError as e:
        if "Email rate limit exceeded" in str(e):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Email rate limit exceeded",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed, please check your credentials",
        )


def login(request: LoginRequest, user_dao: CustomerDAO) -> AuthResponse:
    try:
        if not user_dao.get_by_query(email=request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer not found",
            )
        result: GoTrueAuthResponse = user_dao.client.auth.sign_in_with_password(
            request.auth_model_dump()
        )
        customer = Customer.validate_supabase_user(result.customer)
        session = Session.validate_supabase_session(result.session)
        return AuthResponse(
            customer=customer,
            session=session,
        )
    except AuthApiError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login failed, please check your credentials",
        )
