"""Module handling user sessions for the eCommerce application."""

from gotrue.types import Session as GoTrueSession  # type: ignore
from pydantic import BaseModel as PydanticBaseModel
from pydantic import NonNegativeInt


class Session(PydanticBaseModel):
    """Represents a user session with access and refresh tokens.

    Attributes:
        access_token (str): The access token for the session.
        refresh_token (str): The refresh token for the session.
        expires_in (NonNegativeInt): The duration in seconds until the session expires.
    """
    access_token: str
    refresh_token: str
    expires_in: NonNegativeInt

    @classmethod
    def validate_supabase_session(cls, session: GoTrueSession) -> "Session":
        """Validates and creates a Session instance from a GoTrueSession.

        Args:
            session (GoTrueSession): The session object obtained from Supabase.

        Returns:
            Session: The validated session instance.
        """
        return cls(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            expires_in=session.expires_in,
        )
