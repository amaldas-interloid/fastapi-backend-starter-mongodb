from fastapi import APIRouter, Depends, status

from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.schemas.common import APIResponse
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_auth_service() -> AuthService:
    return AuthService(
        user_repository=UserRepository(),
        refresh_token_repository=RefreshTokenRepository(),
    )


@router.post(
    "/register",
    response_model=APIResponse[RegisterResponse],
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.register_user(request)

    return APIResponse(
        success=True,
        message="User registered successfully",
        data=user,
    )


@router.post(
    "/login",
    response_model=APIResponse[TokenResponse],
)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    token = await auth_service.login_user(request)

    return APIResponse(
        success=True,
        message="Login successful",
        data=token,
    )