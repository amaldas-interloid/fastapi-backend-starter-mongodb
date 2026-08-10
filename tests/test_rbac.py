from unittest.mock import AsyncMock, MagicMock

import pytest

from app.api.deps import require_permission, require_role
from app.exceptions.exceptions import ForbiddenException


def create_mock_user(
    user_id: str = "test-user-id",
) -> MagicMock:
    user = MagicMock()
    user.id = user_id
    return user


@pytest.mark.anyio
async def test_require_role_success(monkeypatch):
    user = create_mock_user()

    role = MagicMock()
    role.id = "admin-role-id"
    role.name = "admin"

    user_role = MagicMock()
    user_role.user_id = user.id
    user_role.role_id = role.id

    get_by_user_id = AsyncMock(
        return_value=[user_role],
    )

    get_by_id = AsyncMock(
        return_value=role,
    )

    monkeypatch.setattr(
        "app.api.deps.user_role_repository.get_by_user_id",
        get_by_user_id,
    )

    monkeypatch.setattr(
        "app.api.deps.role_repository.get_by_id",
        get_by_id,
    )

    dependency = require_role("admin")

    result = await dependency(user)

    assert result is user

    get_by_user_id.assert_awaited_once_with(user.id)
    get_by_id.assert_awaited_once_with(role.id)


@pytest.mark.anyio
async def test_require_role_forbidden(monkeypatch):
    user = create_mock_user()

    role = MagicMock()
    role.id = "user-role-id"
    role.name = "user"

    user_role = MagicMock()
    user_role.user_id = user.id
    user_role.role_id = role.id

    monkeypatch.setattr(
        "app.api.deps.user_role_repository.get_by_user_id",
        AsyncMock(return_value=[user_role]),
    )

    monkeypatch.setattr(
        "app.api.deps.role_repository.get_by_id",
        AsyncMock(return_value=role),
    )

    dependency = require_role("admin")

    with pytest.raises(ForbiddenException):
        await dependency(user)


@pytest.mark.anyio
async def test_require_role_forbidden_when_user_has_no_roles(
    monkeypatch,
):
    user = create_mock_user()

    monkeypatch.setattr(
        "app.api.deps.user_role_repository.get_by_user_id",
        AsyncMock(return_value=[]),
    )

    dependency = require_role("admin")

    with pytest.raises(ForbiddenException):
        await dependency(user)


@pytest.mark.anyio
async def test_require_permission_success(monkeypatch):
    user = create_mock_user()

    role = MagicMock()
    role.id = "admin-role-id"

    user_role = MagicMock()
    user_role.user_id = user.id
    user_role.role_id = role.id

    role_permission = MagicMock()
    role_permission.role_id = role.id
    role_permission.permission_id = "user-read-id"

    permission = MagicMock()
    permission.id = "user-read-id"
    permission.name = "user:read"

    monkeypatch.setattr(
        "app.api.deps.user_role_repository.get_by_user_id",
        AsyncMock(return_value=[user_role]),
    )

    monkeypatch.setattr(
        "app.api.deps.role_permission_repository.get_by_role_id",
        AsyncMock(return_value=[role_permission]),
    )

    monkeypatch.setattr(
        "app.api.deps.permission_repository.get_by_id",
        AsyncMock(return_value=permission),
    )

    dependency = require_permission("user:read")

    result = await dependency(user)

    assert result is user


@pytest.mark.anyio
async def test_require_permission_forbidden(monkeypatch):
    user = create_mock_user()

    user_role = MagicMock()
    user_role.user_id = user.id
    user_role.role_id = "user-role-id"

    role_permission = MagicMock()
    role_permission.role_id = user_role.role_id
    role_permission.permission_id = "user-write-id"

    permission = MagicMock()
    permission.id = "user-write-id"
    permission.name = "user:write"

    monkeypatch.setattr(
        "app.api.deps.user_role_repository.get_by_user_id",
        AsyncMock(return_value=[user_role]),
    )

    monkeypatch.setattr(
        "app.api.deps.role_permission_repository.get_by_role_id",
        AsyncMock(return_value=[role_permission]),
    )

    monkeypatch.setattr(
        "app.api.deps.permission_repository.get_by_id",
        AsyncMock(return_value=permission),
    )

    dependency = require_permission("user:read")

    with pytest.raises(ForbiddenException):
        await dependency(user)


@pytest.mark.anyio
async def test_require_permission_forbidden_when_user_has_no_roles(
    monkeypatch,
):
    user = create_mock_user()

    monkeypatch.setattr(
        "app.api.deps.user_role_repository.get_by_user_id",
        AsyncMock(return_value=[]),
    )

    dependency = require_permission("user:read")

    with pytest.raises(ForbiddenException):
        await dependency(user)
