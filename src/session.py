from gotrue.types import Session as GoTrueSession  # type: ignore
from pydantic import BaseModel as PydanticBaseModel
from pydantic import NonNegativeInt


class Session(PydanticBaseModel):
    access_token: str
    refresh_token: str
    expires_in: NonNegativeInt

    @classmethod
    def validate_supabase_session(cls, session: GoTrueSession) -> "Session":
        return cls(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            expires_in=session.expires_in,
        )
