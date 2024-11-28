"""
This module defines the Pydantic models for authentication requests, including registration,
login, password reset, and OTP verification.
"""

from typing import Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr, Field, PositiveInt, field_validator

from src.utils.types import PasswordStr
from src.utils.validators.name_validator import validate_name


class RegisterRequest(PydanticBaseModel):
    full_name: str = Field(description="Full Name")
    username: str = Field(description="Username")
    age: PositiveInt = Field(description="Age must be a positive integer")
    gender: str = Field(description="Sex")
    address: str = Field(description="Address")
    marital_status: str = Field(description="Marital Status")
    email: EmailStr = Field(description="Email must be valid email")
    password: PasswordStr = Field(
        description="Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number.",
    )

    @field_validator("full_name")
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
                    "full_name": self.full_name,
                    "username": self.username,
                    "age": str(self.age),
                    "gender": self.gender,
                    "address": self.address,
                    "marital_status": self.marital_status,
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
