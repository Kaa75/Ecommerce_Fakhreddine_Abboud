from fastapi import APIRouter, Depends, status

from src.auth.auth import login, register
from src.auth.forget_password import forget_password
from src.auth.refresh_token import refresh_token
from src.auth.request_otp import request_otp
from src.auth.reset_password import reset_password
from src.auth.schemas import (
    ForgetPasswordRequest,
    LoginRequest,
    OTPRequest,
    RegisterRequest,
    ResetPasswordRequest,
    VerifyOTPRequest,
)
from src.auth.verify_otp import verify_otp
from src.common.responses import APIResponse
from src.common.responses.API_response import APIResponse
from src.db.dao import UserDAO
from src.db.dao.user_dao import UserDAO
from src.db.dependencies import get_user_dao, get_user_dao_unauthenticated

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
    "/register",
    response_class=APIResponse,
    summary="Register",
    description="Register a new user",
)
async def register_route(
    request: RegisterRequest,
    user_dao: UserDAO = Depends(get_user_dao_unauthenticated),
) -> APIResponse:
    if user_dao.get_by_query(email=request.email):
        return APIResponse(
            message="Email already in use",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return APIResponse(
        message="Registration successful",
        status_code=status.HTTP_200_OK,
        data=register(request, user_dao).model_dump(),
    )


@auth_router.post(
    "/login",
    response_class=APIResponse,
    summary="Login",
    description="Login to the system",
)
async def login_route(
    request: LoginRequest,
    user_dao: UserDAO = Depends(get_user_dao_unauthenticated),
) -> APIResponse:
    return APIResponse(
        message="Login successful",
        status_code=status.HTTP_200_OK,
        data=login(request, user_dao).model_dump(),
    )


@auth_router.post(
    "/reset-password",
    response_class=APIResponse,
    summary="Reset Password",
    description="Reset user password",
)
async def reset_password_route(
    request: ResetPasswordRequest,
    user_dao: UserDAO = Depends(get_user_dao),
) -> APIResponse:
    return APIResponse(
        message="Password change successful",
        status_code=status.HTTP_200_OK,
        data=reset_password(request, user_dao).model_dump(),
    )


@auth_router.post(
    "/forget-password",
    response_class=APIResponse,
    summary="Forget Password",
    description="Forget user password",
)
async def forgot_password_route(
    request: ForgetPasswordRequest,
    user_dao: UserDAO = Depends(get_user_dao_unauthenticated),
) -> APIResponse:
    return APIResponse(
        message="Forget password email sent successfully",
        status_code=status.HTTP_200_OK,
        data=forget_password(request, user_dao).model_dump(),
    )


@auth_router.post(
    "/refresh-token",
    response_class=APIResponse,
    summary="Refresh Token",
    description="Refresh user token",
)
async def refresh_token_route(
    user_dao: UserDAO = Depends(get_user_dao),
) -> APIResponse:
    return APIResponse(
        message="Token refresh successful",
        status_code=status.HTTP_200_OK,
        data=refresh_token(user_dao).model_dump(),
    )


@auth_router.post(
    "/request-otp",
    response_class=APIResponse,
    summary="Request OTP",
    description="Request OTP",
)
async def request_otp_route(
    request: OTPRequest,
    user_dao: UserDAO = Depends(get_user_dao_unauthenticated),
) -> APIResponse:
    return APIResponse(
        message="OTP request successful",
        status_code=status.HTTP_200_OK,
        data=request_otp(request, user_dao).model_dump(),
    )


@auth_router.post(
    "/verify-otp",
    response_class=APIResponse,
    summary="Verify OTP",
    description="Verify OTP",
)
async def verify_otp_route(
    request: VerifyOTPRequest,
    user_dao: UserDAO = Depends(get_user_dao_unauthenticated),
) -> APIResponse:
    return APIResponse(
        message="OTP verification successful",
        status_code=status.HTTP_200_OK,
        data=verify_otp(request, user_dao).model_dump(),
    )
