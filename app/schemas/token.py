from pydantic import BaseModel

from app.enums.token import TokenType


class TokenPayload(BaseModel):
    sub: str
    type: TokenType
    exp: int
    jti: str | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str
