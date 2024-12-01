import random
import uuid
from typing import Any
from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from gotrue import AuthResponse as GoTrueAuthResponse  # type: ignore
from gotrue.types import Session as GoTrueSession  # type: ignore
from gotrue.types import User as GoTrueUser
from pydantic import EmailStr, PositiveInt

from src.auth.auth import login, register
from src.auth.schemas import LoginRequest, RegisterRequest
from src.db.models import Customer
from src.session import Session
from src.utils.types import PasswordStr


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
def login_request() -> Any:
    return LoginRequest(email="rayan@mail.com", password="pasSword123")


@pytest.fixture
def session() -> Session:
    return Session(
        access_token="access_token",
        refresh_token="refresh_token",
        expires_in=3600,
    )


@pytest.mark.asyncio
class TestRegister:
    async def test_register_successful(
        self,
        register_request: RegisterRequest,
        user1: Customer,
        gotrue_user: GoTrueUser,
    ) -> None:
        user_dao = Mock()
        user_dao.get_by_query.return_value = None
        user_dao.client.auth.sign_up.return_value = GoTrueAuthResponse(
            user=gotrue_user,
            session=None,
        )

        response = register(register_request, user_dao)

        assert user_dao.client.auth.sign_up.called

        assert response.customer == user1
        assert response.session is None

    @pytest.mark.parametrize(
        "fullname, username, age, gender, address, marital_status, email",
        [
            (None, "username", 25, "Male", "123 Street", "Single", "user@example.com"),
            (
                "First Last",
                None,
                30,
                "Female",
                "456 Avenue",
                "Married",
                "user@example.com",
            ),
            (
                "First Last",
                "username",
                None,
                "Other",
                "789 Boulevard",
                "Divorced",
                "user@example.com",
            ),
            (
                "First Last",
                "username",
                25,
                None,
                "123 Street",
                "Single",
                "user@example.com",
            ),
            ("First Last", "username", 25, "Male", None, "Single", "user@example.com"),
            (
                "First Last",
                "username",
                25,
                "Male",
                "123 Street",
                None,
                "user@example.com",
            ),
            ("First Last", "username", 25, "Male", "123 Street", "Single", None),
        ],
    )
    async def test_register_no_attribute(
        self,
        register_request: RegisterRequest,
        user1: Customer,
        fullname: str,
        username: str,
        age: PositiveInt,
        gender: str,
        address: str,
        marital_status: str,
        email: EmailStr,
    ) -> None:
        user_dao = Mock()
        user_dao.get_by_query.return_value = None
        user_dao.client.auth.sign_up.return_value = GoTrueAuthResponse(
            user=GoTrueUser(
                id=user1.id,
                email=email,
                user_metadata={
                    "fullname": fullname,
                    "username": username,
                    "age": age,
                    "gender": gender,
                    "address": address,
                    "marital_status": marital_status,
                },
                aud="authenticated",
                app_metadata={},
                created_at="2021-10-10T10:10:10.000Z",
            ),
            session=None,
        )

        with pytest.raises(Exception):
            register(register_request, user_dao)

    async def test_register_email_in_use(
        self, register_request: RegisterRequest, user1: Customer
    ) -> None:
        user_dao = Mock()
        user_dao.get_by_query.return_value = user1

        with pytest.raises(Exception) as exc:
            register(register_request, user_dao)
            assert "Email already in use" in str(exc.value)

    async def test_register_failed(
        self, register_request: RegisterRequest, user1: Customer
    ) -> None:
        user_dao = Mock()
        user_dao.get_by_query.return_value = None
        user_dao.client.auth.sign_up.side_effect = Exception()

        with pytest.raises(Exception) as exc:
            register(register_request, user_dao)
            assert "Registration failed, please check your credentials" in str(
                exc.value
            )

    @pytest.mark.parametrize(
        "password",
        [
            "pas",
            "password",
            "PASSWORD",
            "Password",
            "password1",
            "PASSWORD1",
            "Password1",
            "password!",
            "PASSWORD!",
            "Password!",
            "password1!",
            "PASSWORD1!",
            "Password1!",
        ],
    )
    async def test_register_password_too_short(
        self, register_request: RegisterRequest, password: PasswordStr
    ) -> None:
        user_dao = Mock()
        user_dao.client.auth.sign_up.side_effect = Exception()
        register_request.password = password
        with pytest.raises(Exception) as exc:
            register(register_request, user_dao)
            assert exc.type == HTTPException

    async def test_register_email_rate_limit_exceeded(
        self, register_request: RegisterRequest
    ) -> None:
        user_dao = Mock()
        user_dao.client.auth.sign_up.side_effect = Exception(
            "Email rate limit exceeded"
        )

        with pytest.raises(Exception) as exc:
            register(register_request, user_dao)
            assert "Email rate limit exceeded, please try again later" in str(exc.value)


@pytest.mark.asyncio
class TestLogin:
    async def test_login_successful(
        self,
        login_request: LoginRequest,
        user1: Customer,
        session: Session,
        gotrue_user: GoTrueUser,
        gotrue_session: GoTrueSession,
    ) -> None:
        user_dao = Mock()
        user_dao.get_by_query.return_value = user1
        user_dao.client.auth.sign_in_with_password.return_value = GoTrueAuthResponse(
            user=gotrue_user, session=gotrue_session
        )

        response = login(login_request, user_dao)

        assert user_dao.get_by_query.called
        assert user_dao.client.auth.sign_in_with_password.called

        assert response.customer == user1
        assert response.session == session

    async def test_login_user_not_found(self, login_request: LoginRequest) -> None:
        user_dao = Mock()
        user_dao.get_by_query.return_value = None

        with pytest.raises(Exception) as exc:
            login(login_request, user_dao)
            assert "User not found" in str(exc.value)

    async def test_login_failed(self, login_request: LoginRequest) -> None:
        user_dao = Mock()
        user_dao.get_by_query.return_value = None
        user_dao.client.auth.sign_in_with_password.side_effect = Exception()

        with pytest.raises(Exception) as exc:
            login(login_request, user_dao)
            assert "Login failed, please check your credentials" in str(exc.value)
