from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


def get_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    return credentials.credentials