import random
import uuid
from typing import Any
from unittest.mock import Mock

import pytest
from fastapi import status
from gotrue import AuthResponse as GoTrueAuthResponse  # type: ignore
from gotrue.types import Session as GoTrueSession  # type: ignore
from gotrue.types import User as GoTrueUser

from src.auth.router import (
    login_route,
    refresh_token_route,
    register_route,
    reset_password_route,
)
from src.auth.schemas import LoginRequest, RegisterRequest, ResetPasswordRequest
from src.db.models import Customer
from src.session import Session


@pytest.fixture
def register_request() -> Any:
    return RegisterRequest(
        full_name="Rayan Alves",
        username="rayan",
        age=19,
        gender="Male",
        address="Riyadh",
        marital_status="Single",
        email="rayan@mail.com",
        password="Password123!",
    )


@pytest.fixture
def login_request() -> Any:
    return LoginRequest(email="rayan@mail.com", password="pasSword123")


@pytest.fixture
def reset_password_request() -> Any:
    return ResetPasswordRequest(password="newPasSword123")


@pytest.fixture
def uuid_generator() -> Mock:
    return Mock(side_effect=lambda: str(uuid.UUID(int=random.getrandbits(128))))


@pytest.fixture
def user1(uuid_generator: Mock) -> list[Customer]:
    return Customer(
        id=uuid_generator(),
        fullname="Rayan Alves",
        username="rayan",
        age=19,
        gender="Male",
        address="Riyadh",
        marital_status="Single",
        email="rayan@mail.com",
        wallet=0.0,
    )


@pytest.fixture
def gotrue_user(user1: Customer) -> GoTrueUser:
    return GoTrueUser(
        id=user1.id,
        email=user1.email,
        user_metadata={
            "fullname": user1.fullname,
            "username": user1.username,
            "age": user1.age,
            "gender": user1.gender,
            "address": user1.address,
            "marital_status": user1.marital_status,
        },
        aud="authenticated",
        app_metadata={},
        created_at="2021-10-10T10:10:10.000Z",
    )


@pytest.fixture
def gotrue_session(session: Session, gotrue_user: GoTrueUser) -> GoTrueSession:
    return GoTrueSession(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        expires_in=session.expires_in,
        token_type="Bearer",
        user=gotrue_user,
    )


@pytest.fixture
def session() -> Session:
    return Session(
        access_token="access_token",
        refresh_token="refresh_token",
        expires_in=3600,
    )


@pytest.mark.asyncio
class TestRegisterRoute:
    async def test_register_route_successful(
        self,
        register_request: RegisterRequest,
        gotrue_user: GoTrueUser,
        user1: Customer,
    ) -> None:
        user_dao = Mock()
        user_dao.get_by_query.return_value = None
        user_dao.client.auth.sign_up.return_value = GoTrueAuthResponse(
            user=gotrue_user,
            session=None,
        )
        response = await register_route(register_request, user_dao)
        res = eval(response.body, {"null": None})

        assert response.status_code == status.HTTP_200_OK
        assert res == {
            "message": "Registration successful",
            "data": {"customer": user1.model_dump(), "session": None},
        }


@pytest.mark.asyncio
class TestLoginRoute:
    async def test_login_route_successful(
        self,
        login_request: LoginRequest,
        gotrue_user: GoTrueUser,
        gotrue_session: GoTrueSession,
        user1: Customer,
        session: Session,
    ) -> None:
        user_dao = Mock()
        user_dao.client.auth.sign_in_with_password.return_value = GoTrueAuthResponse(
            user=gotrue_user,
            session=gotrue_session,
        )
        response = await login_route(login_request, user_dao)
        res = eval(response.body)

        assert response.status_code == status.HTTP_200_OK
        assert res == {
            "message": "Login successful",
            "data": {
                "customer": user1.model_dump(),
                "session": session.model_dump(),
            },
        }


@pytest.mark.asyncio
class TestForgetPasswordRoute:
    async def test_forget_password_route_successful(self) -> None: ...


@pytest.mark.asyncio
class TestRefreshTokenRoute:
    async def test_refresh_token_route_successful(
        self,
        gotrue_user: GoTrueUser,
        gotrue_session: GoTrueSession,
        user1: Customer,
        session: Session,
    ) -> None:
        user_dao = Mock()
        user_dao.client.auth.refresh_session.return_value = GoTrueAuthResponse(
            user=gotrue_user,
            session=gotrue_session,
        )
        response = await refresh_token_route(user_dao)
        res = eval(response.body)

        assert response.status_code == status.HTTP_200_OK
        assert res == {
            "message": "Token refresh successful",
            "data": {
                "customer": user1.model_dump(),
                "session": session.model_dump(),
            },
        }


@pytest.mark.asyncio
class TestRequestOTPRoute:
    async def test_request_otp_route_successful(self) -> None: ...


@pytest.mark.asyncio
class TestVerifyOTPRoute:
    async def test_verify_otp_route_successful(self) -> None: ...


@pytest.mark.asyncio
class TestResetPasswordRoute:
    async def test_reset_password_route_successful(
        self,
        reset_password_request: ResetPasswordRequest,
        gotrue_user: GoTrueUser,
        user1: Customer,
    ) -> None:
        user_dao = Mock()
        user_dao.client.auth.update_user.return_value = GoTrueAuthResponse(
            user=gotrue_user,
            session=None,
        )
        response = await reset_password_route(reset_password_request, user_dao)
        res = eval(response.body, {"null": None})

        assert response.status_code == status.HTTP_200_OK
        assert res == {
            "message": "Password change successful",
            "data": {"customer": user1.model_dump(), "session": None},
        }
