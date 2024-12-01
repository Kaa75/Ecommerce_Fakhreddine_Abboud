import pytest
from pydantic import PositiveInt

from src.auth.schemas import LoginRequest, RegisterRequest, ResetPasswordRequest


class TestRegisterRequest:
    def test_register_request_successful(self) -> None:
        register_request = RegisterRequest(
            full_name="First Last",
            username="username",
            age=22,
            gender="Male",
            address="Riyadh",
            marital_status="Single",
            email="email@mail.com",
            password="Password123",
        )
        assert register_request.full_name == "First Last"
        assert register_request.username == "username"
        assert register_request.age == 22
        assert register_request.gender == "Male"
        assert register_request.address == "Riyadh"
        assert register_request.marital_status == "Single"
        assert register_request.email == "email@mail.com"
        assert register_request.password == "Password123"
        assert register_request.auth_model_dump() == {
            "email": "email@mail.com",
            "password": "Password123",
            "options": {
                "data": {
                    "full_name": "First Last",
                    "username": "username",
                    "age": 22,
                    "gender": "Male",
                    "address": "Riyadh",
                    "marital_status": "Single",
                }
            },
        }

    @pytest.mark.parametrize(
        "full_name, username, age, gender, address, marital_status, email, password",
        [
            (
                "",
                "username",
                25,
                "Male",
                "123 Street",
                "Single",
                "user@example.com",
                "Passw0rd!",
            ),
            (
                "First Last",
                1,
                30,
                "Female",
                "456 Avenue",
                "Married",
                "user@example.com",
                "Passw0rd!",
            ),
            (
                "First Last",
                "username",
                -5,
                "Other",
                "789 Boulevard",
                "Divorced",
                "user@example.com",
                "Passw0rd!",
            ),
            (
                "First Last",
                "username",
                25,
                1,
                "123 Street",
                "Single",
                "user@example.com",
                "Passw0rd!",
            ),
            (
                "First Last",
                "username",
                25,
                "Male",
                1,
                "Single",
                "user@example.com",
                "Passw0rd!",
            ),
            (
                "First Last",
                "username",
                25,
                "Male",
                "123 Street",
                1,
                "user@example.com",
                "Passw0rd!",
            ),
            (
                "First Last",
                "username",
                25,
                "Male",
                "123 Street",
                "Single",
                "invalid-email",
                "Passw0rd!",
            ),
            (
                "First Last",
                "username",
                25,
                "Male",
                "123 Street",
                "Single",
                "user@example.com",
                "",
            ),
        ],
    )
    def test_register_request_invalid(
        self,
        full_name: str,
        username: str,
        age: PositiveInt,
        gender: str,
        address: str,
        marital_status: str,
        email: str,
        password: str,
    ) -> None:
        with pytest.raises(ValueError):
            RegisterRequest(
                full_name=full_name,
                username=username,
                age=age,
                gender=gender,
                address=address,
                marital_status=marital_status,
                email=email,
                password=password,
            )


class TestLoginRequest:
    def test_login_request_successful(self) -> None:
        login_request = LoginRequest(email="email@mail.com", password="Password123")
        assert login_request.email == "email@mail.com"
        assert login_request.password == "Password123"
        assert login_request.auth_model_dump() == {
            "email": "email@mail.com",
            "password": "Password123",
        }

    @pytest.mark.parametrize(
        "email, password",
        [
            ("email@mail", "Password123"),
            ("email@mail.com", "password123"),
        ],
    )
    def test_login_request_invalid(self, email: str, password: str) -> None:
        with pytest.raises(ValueError):
            LoginRequest(email=email, password=password)


class TestForgetPasswordRequest:
    def test_forget_password_request_successful(self) -> None: ...

    def test_forget_password_request_invalid(self) -> None: ...


class TestResetPasswordRequest:
    def test_reset_password_request_successful(self) -> None:
        password_reset_request = ResetPasswordRequest(password="Password123")
        assert password_reset_request.password == "Password123"
        assert password_reset_request.model_dump() == {
            "password": "Password123",
        }

    @pytest.mark.parametrize("password", ["password123"])
    def test_reset_password_request_invalid(self, password: str) -> None:
        with pytest.raises(ValueError):
            ResetPasswordRequest(password=password)


class TestOTPRequest:
    def test_otp_request_successful(self) -> None: ...

    def test_otp_request_invalid(self) -> None: ...


class TestSignInWithOTPRequest:
    def test_sign_in_with_otp_request_successful(self) -> None: ...

    def test_sign_in_with_otp_request_invalid(self) -> None: ...
