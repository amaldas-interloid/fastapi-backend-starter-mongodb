from fastapi import APIRouter, Depends, status

from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service() -> AuthService:
    return AuthService(UserRepository())


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register_user(
        username=request.username,
        email=request.email,
        password=request.password,
    )