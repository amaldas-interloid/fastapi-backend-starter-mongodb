from collections.abc import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token
from app.enums.token import TokenType
from app.exceptions.exceptions import (
    ForbiddenException,
    InactiveUserException,
    InvalidCredentialsException,
)
from app.models.user import User
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from app.repositories.role_permission import RolePermissionRepository
from app.repositories.user_role import UserRoleRepository

security = HTTPBearer()
user_role_repository = UserRoleRepository()
role_repository = RoleRepository()
role_permission_repository = RolePermissionRepository()
permission_repository = PermissionRepository()


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


def require_role(role_name: str) -> Callable:
    async def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        user_roles = await user_role_repository.get_by_user_id(
            current_user.id,
        )

        for user_role in user_roles:
            role = await role_repository.get_by_id(
                user_role.role_id,
            )

            if role and role.name == role_name:
                return current_user

        raise ForbiddenException()

    return role_dependency


def require_permission(permission_name: str) -> Callable:
    async def permission_dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        user_roles = await user_role_repository.get_by_user_id(
            current_user.id,
        )

        for user_role in user_roles:
            role_permissions = await role_permission_repository.get_by_role_id(
                user_role.role_id,
            )

            for role_permission in role_permissions:
                permission = await permission_repository.get_by_id(
                    role_permission.permission_id,
                )

                if permission and permission.name == permission_name:
                    return current_user

        raise ForbiddenException()

    return permission_dependency
