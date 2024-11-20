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
from src.db.dao import CustomerDAO
from src.db.dao.customer_dao import CustomerDAO
from src.db.dependencies import get_customer_dao, get_customer_dao_unauthenticated
from src.utils.responses import APIResponse
from src.utils.responses.API_response import APIResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
    "/register",
    response_class=APIResponse,
    summary="Register",
    description="Register a new Customer",
)
async def register_route(
    request: RegisterRequest,
    Customer_dao: CustomerDAO = Depends(get_customer_dao_unauthenticated),
) -> APIResponse:
    if Customer_dao.get_by_query(email=request.email):
        return APIResponse(
            message="Email already in use",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return APIResponse(
        message="Registration successful",
        status_code=status.HTTP_200_OK,
        data=register(request, Customer_dao).model_dump(),
    )


@auth_router.post(
    "/login",
    response_class=APIResponse,
    summary="Login",
    description="Login to the system",
)
async def login_route(
    request: LoginRequest,
    Customer_dao: CustomerDAO = Depends(get_customer_dao_unauthenticated),
) -> APIResponse:
    return APIResponse(
        message="Login successful",
        status_code=status.HTTP_200_OK,
        data=login(request, Customer_dao).model_dump(),
    )


@auth_router.post(
    "/reset-password",
    response_class=APIResponse,
    summary="Reset Password",
    description="Reset Customer password",
)
async def reset_password_route(
    request: ResetPasswordRequest,
    Customer_dao: CustomerDAO = Depends(get_customer_dao),
) -> APIResponse:
    return APIResponse(
        message="Password change successful",
        status_code=status.HTTP_200_OK,
        data=reset_password(request, Customer_dao).model_dump(),
    )


@auth_router.post(
    "/forget-password",
    response_class=APIResponse,
    summary="Forget Password",
    description="Forget Customer password",
)
async def forgot_password_route(
    request: ForgetPasswordRequest,
    Customer_dao: CustomerDAO = Depends(get_customer_dao_unauthenticated),
) -> APIResponse:
    return APIResponse(
        message="Forget password email sent successfully",
        status_code=status.HTTP_200_OK,
        data=forget_password(request, Customer_dao).model_dump(),
    )


@auth_router.post(
    "/refresh-token",
    response_class=APIResponse,
    summary="Refresh Token",
    description="Refresh Customer token",
)
async def refresh_token_route(
    Customer_dao: CustomerDAO = Depends(get_customer_dao),
) -> APIResponse:
    return APIResponse(
        message="Token refresh successful",
        status_code=status.HTTP_200_OK,
        data=refresh_token(Customer_dao).model_dump(),
    )


@auth_router.post(
    "/request-otp",
    response_class=APIResponse,
    summary="Request OTP",
    description="Request OTP",
)
async def request_otp_route(
    request: OTPRequest,
    Customer_dao: CustomerDAO = Depends(get_customer_dao_unauthenticated),
) -> APIResponse:
    return APIResponse(
        message="OTP request successful",
        status_code=status.HTTP_200_OK,
        data=request_otp(request, Customer_dao).model_dump(),
    )


@auth_router.post(
    "/verify-otp",
    response_class=APIResponse,
    summary="Verify OTP",
    description="Verify OTP",
)
async def verify_otp_route(
    request: VerifyOTPRequest,
    Customer_dao: CustomerDAO = Depends(get_customer_dao_unauthenticated),
) -> APIResponse:
    return APIResponse(
        message="OTP verification successful",
        status_code=status.HTTP_200_OK,
        data=verify_otp(request, Customer_dao).model_dump(),
    )
