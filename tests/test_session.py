import random
from unittest.mock import Mock
import uuid
import pytest
from gotrue.types import Session as GoTrueSession  # type: ignore
from gotrue.types import User as GoTrueUser
from src.db.models import Customer
from src.session import Session

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

class TestSession:
    def test_session_successful(self) -> None:
        session = Session(
            access_token="access token", refresh_token="refresh token", expires_in=3600
        )
        assert session.access_token == "access token"
        assert session.refresh_token == "refresh token"
        assert session.expires_in == 3600
        assert session.model_dump() == {
            "access_token": "access token",
            "refresh_token": "refresh token",
            "expires_in": 3600,
        }

    def test_session_invalid(self) -> None:
        with pytest.raises(ValueError):
            Session(
                access_token="access token",
                refresh_token="refresh token",
                expires_in=-1,
            )

    @pytest.mark.parametrize(
        "access_token, refresh_token, expires_in",
        [
            (None, "refresh token", 3600),
            ("access token", None, 3600),
            ("access token", "refresh token", None),
        ],
    )
    def test_session_invalid_none(
        self,
        access_token: str,
        refresh_token: str,
        expires_in: int,
    ) -> None:
        with pytest.raises(ValueError):
            Session(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
            )

    def test_validate_supabase_session_successful(
        self, gotrue_session: GoTrueSession
    ) -> None:
        session = Session.validate_supabase_session(gotrue_session)
        assert session.access_token == gotrue_session.access_token
        assert session.refresh_token == gotrue_session.refresh_token
        assert session.expires_in == gotrue_session.expires_in
        assert session.model_dump() == {
            "access_token": gotrue_session.access_token,
            "refresh_token": gotrue_session.refresh_token,
            "expires_in": gotrue_session.expires_in,
        }

    def test_validate_supabase_session_invalid(
        self, gotrue_session: GoTrueSession
    ) -> None:
        gotrue_session.expires_in = -1
        with pytest.raises(ValueError):
            Session.validate_supabase_session(gotrue_session)
