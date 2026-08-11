from app.core.security import hash_password
from app.exceptions.exceptions import (
    UserAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreateRequest, UserUpdateRequest


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    async def create_user(
        self,
        request: UserCreateRequest,
    ) -> User:
        # Check duplicate email
        existing_email = await self.user_repository.get_by_email(
            request.email,
        )

        if existing_email is not None:
            raise UserAlreadyExistsException()

        # Check duplicate username
        existing_username = await self.user_repository.get_by_username(
            request.username,
        )

        if existing_username is not None:
            raise UsernameAlreadyExistsException()

        # Create user with hashed password
        user = User(
            email=request.email,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            hashed_password=hash_password(request.password),
        )

        return await self.user_repository.create(user)

    async def get_users(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[User], int]:
        skip = (page - 1) * page_size

        users = await self.user_repository.get_all_users(
            skip=skip,
            limit=page_size,
        )

        total = await self.user_repository.count_users()

        return users, total

    async def get_user(
        self,
        user_id: str,
    ) -> User | None:
        return await self.user_repository.get_by_id(
            user_id,
        )

    async def update_user(
        self,
        user: User,
        request: UserUpdateRequest,
    ) -> User:
        data = request.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        # Check duplicate email
        if "email" in data:
            existing_email = await self.user_repository.get_by_email(
                data["email"],
            )

            if (
                existing_email is not None
                and existing_email.id != user.id
            ):
                raise UserAlreadyExistsException()

        # Check duplicate username
        if "username" in data:
            existing_username = (
                await self.user_repository.get_by_username(
                    data["username"],
                )
            )

            if (
                existing_username is not None
                and existing_username.id != user.id
            ):
                raise UsernameAlreadyExistsException()

        # Hash password before storing
        if "password" in data:
            data["hashed_password"] = hash_password(
                data.pop("password"),
            )

        return await self.user_repository.update_user(
            user,
            data,
        )

    async def delete_user(
        self,
        user: User,
    ) -> User:
        return await self.user_repository.soft_delete(user)

