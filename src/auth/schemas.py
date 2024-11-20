from typing import Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr, Field, field_validator

from src.common.utils.types import PasswordStr
from src.common.utils.validators import validate_name


class RegisterRequest(PydanticBaseModel):
    first_name: str = Field(description="First Name")
    last_name: str = Field(description="Last Name")
    email: EmailStr = Field(description="Email must be valid email")
    password: PasswordStr = Field(
        description="Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number.",
    )

    @field_validator("first_name", "last_name")
    def name_validator(cls, v: str) -> str:
        return validate_name(v)

    def auth_model_dump(
        self,
    ) -> dict[str, Union[str, dict[str, dict[str, str]]]]:
        return {
            "email": self.email,
            "password": self.password,
            "options": {
                "data": {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                }
            },
        }


class LoginRequest(PydanticBaseModel):
    email: EmailStr = Field(description="Email must be a valid email")
    password: PasswordStr = Field(
        description="Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number."
    )

    def auth_model_dump(self) -> dict[str, str]:
        return {
            "email": self.email,
            "password": self.password,
        }


class ForgetPasswordRequest(PydanticBaseModel):
    email: EmailStr = Field(description="Email must be valid email")


class ResetPasswordRequest(PydanticBaseModel):
    password: PasswordStr = Field(
        description="Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number.",
    )


class OTPRequest(PydanticBaseModel):
    email: EmailStr = Field(description="Email must be valid email")


class VerifyOTPRequest(PydanticBaseModel):
    email: EmailStr = Field(description="Email must be valid email")
    otp: str = Field(description="OTP must be 6 characters long")
