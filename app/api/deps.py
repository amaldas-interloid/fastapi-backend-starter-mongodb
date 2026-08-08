from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token
from app.enums.token import TokenType
from app.exceptions.exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
)
from app.models.user import User

security = HTTPBearer()


def get_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    return credentials.credentials


async def get_current_user(
    token: str = Depends(get_token),
) -> User:
    payload = decode_token(token)

    if payload.type != TokenType.ACCESS:
        raise InvalidCredentialsException()

    user = await User.get(payload.sub)

    if user is None:
        raise InvalidCredentialsException()

    if not user.is_active:
        raise InactiveUserException()

    return user