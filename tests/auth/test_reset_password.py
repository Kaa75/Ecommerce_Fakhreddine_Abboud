import random
import uuid
from typing import Any
from unittest.mock import Mock

import pytest
from gotrue import AuthResponse as GoTrueAuthResponse  # type: ignore
from gotrue.types import User as GoTrueUser  # type: ignore

from src.auth.reset_password import reset_password
from src.auth.schemas import LoginRequest, RegisterRequest, ResetPasswordRequest
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


class TestResetPassword:
    def test_reset_password_successful(
        self,
        reset_password_request: ResetPasswordRequest,
        user1: Customer,
        gotrue_user: GoTrueUser,
    ) -> None:
        user_dao = Mock()
        user_dao.client.auth.update_user.return_value = GoTrueAuthResponse(
            user=gotrue_user,
            session=None,
        )

        response = reset_password(reset_password_request, user_dao)

        assert user_dao.client.auth.update_user.called

        assert response.customer == user1

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
    def test_reset_password_invalid_password(
        self, password: PasswordStr, reset_password_request: ResetPasswordRequest
    ) -> None:
        user_dao = Mock()
        user_dao.client.auth.update_user.side_effect = Exception()

        with pytest.raises(Exception):
            reset_password(ResetPasswordRequest(password="password"), user_dao)

    def test_reset_password_user_not_auth(self) -> None:
        user_dao = Mock()
        user_dao.get_by_query.return_value = None

        with pytest.raises(Exception):
            reset_password(ResetPasswordRequest(password="password"), user_dao)
