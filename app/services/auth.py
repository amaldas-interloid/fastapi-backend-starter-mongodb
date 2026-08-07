from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.exceptions.exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
    ) -> None:
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    async def register_user(
        self,
       request: RegisterRequest,
    ) -> RegisterResponse:
        existing_user = await self.user_repository.get_by_email(request.email)

        if existing_user is not None:
            raise UserAlreadyExistsException()

        existing_user = await self.user_repository.get_by_username(
            request.username
        )

        if existing_user is not None:
            raise UsernameAlreadyExistsException()

        user = User(
            username=request.username,
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            hashed_password=hash_password(request.password),
        )

        await self.user_repository.create(user)

        return RegisterResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
        )
        
    async def login_user(
            self,
            request: LoginRequest,
    )->TokenResponse:
        user= await self.user_repository.get_by_email(
            request.email
        )

        if user is None:
            raise InvalidCredentialsException()

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InactiveUserException()
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        refresh_token_document = RefreshToken(
            user_id=user.id,
            token=refresh_token,
        )

        await self.refresh_token_repository.create(
            refresh_token_document
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    
