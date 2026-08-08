from uuid import uuid4

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.enums.token import TokenType
from app.exceptions.exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
    InvalidRefreshTokenException,
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
from app.schemas.token import RefreshTokenRequest


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
        refresh_token, jti = create_refresh_token(user.id)
        family_id = str(uuid4())

        refresh_token_document = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            jti=jti,
            family_id=family_id,
        )

        await self.refresh_token_repository.create(
            refresh_token_document
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    
    async def refresh_token(
        self,
        request: RefreshTokenRequest,
    ) -> TokenResponse:

        payload = decode_token(request.refresh_token)

        if payload.type != TokenType.REFRESH:
            raise InvalidRefreshTokenException()

        stored_token = await self.refresh_token_repository.get_by_token(
            request.refresh_token
        )

        if stored_token is None:
            raise InvalidRefreshTokenException()
        
        if stored_token.is_revoked:
            await self.refresh_token_repository.revoke_family(
                stored_token.family_id,
            )

            raise InvalidRefreshTokenException()


        if not await self.refresh_token_repository.is_valid(
            stored_token,
        ):
            raise InvalidRefreshTokenException()

        user = await self.user_repository.get_by_id(
            payload.sub,
        )

        if user is None or not user.is_active:
            raise InvalidRefreshTokenException()
        
        # Revoke the old refresh token
        await self.refresh_token_repository.revoke(
        stored_token,
        )

        # Create new access token
        access_token = create_access_token(user.id)

        # Create new refresh token
        new_refresh_token, new_jti = create_refresh_token(user.id)

        # Keep the same token family
        new_refresh_token_document = RefreshToken(
            user_id=user.id,
            token=new_refresh_token,
            jti=new_jti,
            family_id=stored_token.family_id,
        )

        await self.refresh_token_repository.create(
            new_refresh_token_document,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )
    async def logout(
        self,
        request: RefreshTokenRequest,
    ) -> None:
        stored_token = await self.refresh_token_repository.get_by_token(
            request.refresh_token,
        )

        if stored_token is None:
            raise InvalidRefreshTokenException()

        if stored_token.is_revoked:
            raise InvalidRefreshTokenException()

        await self.refresh_token_repository.revoke(
            stored_token,
        )

    
    

    
