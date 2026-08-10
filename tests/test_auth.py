from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.exceptions.exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth import AuthService


def create_mock_user(
    *,
    username: str = "testuser",
    email: str = "test@example.com",
    is_active: bool = True,
    is_verified: bool = False,
):
    user = MagicMock()

    user.id = "test-user-id"
    user.username = username
    user.email = email
    user.first_name = "Test"
    user.last_name = "User"
    user.hashed_password = "hashed-password"
    user.is_active = is_active
    user.is_verified = is_verified

    return user


@pytest.fixture
def user_repository():
    return AsyncMock()


@pytest.fixture
def refresh_token_repository():
    return AsyncMock()


@pytest.fixture
def auth_service(
    user_repository,
    refresh_token_repository,
):
    return AuthService(
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )


@pytest.mark.anyio
async def test_register_user_success(
    auth_service,
    user_repository,
):
    user_repository.get_by_email.return_value = None
    user_repository.get_by_username.return_value = None

    request = RegisterRequest(
        username="testuser",
        email="test@example.com",
        password="Password@123",
        first_name="Test",
        last_name="User",
    )

    created_user = create_mock_user(
        username=request.username,
        email=request.email,
    )

    user_repository.create.return_value = created_user

    with patch("app.services.auth.User") as mock_user_model:
        mock_user_model.return_value = created_user

        result = await auth_service.register_user(request)

    assert result.username == "testuser"
    assert result.email == "test@example.com"
    assert result.first_name == "Test"
    assert result.last_name == "User"
    assert result.id == "test-user-id"
    assert result.is_active is True
    assert result.is_verified is False
    assert result.created_at is not None

    user_repository.get_by_email.assert_awaited_once_with(
        request.email,
    )

    user_repository.get_by_username.assert_awaited_once_with(
        request.username,
    )

    user_repository.create.assert_awaited_once_with(
        created_user,
    )


@pytest.mark.anyio
async def test_register_duplicate_email(
    auth_service,
    user_repository,
):
    existing_user = create_mock_user(
        email="test@example.com",
    )

    user_repository.get_by_email.return_value = existing_user

    request = RegisterRequest(
        username="testuser",
        email="test@example.com",
        password="Password@123",
        first_name="Test",
        last_name="User",
    )

    with pytest.raises(UserAlreadyExistsException):
        await auth_service.register_user(request)

    user_repository.get_by_email.assert_awaited_once_with(
        request.email,
    )

    user_repository.get_by_username.assert_not_awaited()
    user_repository.create.assert_not_awaited()


@pytest.mark.anyio
async def test_register_duplicate_username(
    auth_service,
    user_repository,
):
    existing_user = create_mock_user(
        username="testuser",
        email="existing@example.com",
    )

    user_repository.get_by_email.return_value = None
    user_repository.get_by_username.return_value = existing_user

    request = RegisterRequest(
        username="testuser",
        email="test@example.com",
        password="Password@123",
        first_name="Test",
        last_name="User",
    )

    with pytest.raises(UsernameAlreadyExistsException):
        await auth_service.register_user(request)

    user_repository.get_by_email.assert_awaited_once_with(
        request.email,
    )

    user_repository.get_by_username.assert_awaited_once_with(
        request.username,
    )

    user_repository.create.assert_not_awaited()


@pytest.mark.anyio
async def test_login_invalid_email(
    auth_service,
    user_repository,
):
    user_repository.get_by_email.return_value = None

    request = LoginRequest(
        email="missing@example.com",
        password="Password@123",
    )

    with pytest.raises(InvalidCredentialsException):
        await auth_service.login_user(request)

    user_repository.get_by_email.assert_awaited_once_with(
        request.email,
    )


@pytest.mark.anyio
async def test_login_invalid_password(
    auth_service,
    user_repository,
):
    from app.core.security import hash_password

    user = create_mock_user()
    user.hashed_password = hash_password("CorrectPassword@123")

    user_repository.get_by_email.return_value = user

    request = LoginRequest(
        email="test@example.com",
        password="WrongPassword@123",
    )

    with pytest.raises(InvalidCredentialsException):
        await auth_service.login_user(request)

    user_repository.get_by_email.assert_awaited_once_with(
        request.email,
    )


@pytest.mark.anyio
async def test_login_inactive_user(
    auth_service,
    user_repository,
):
    from app.core.security import hash_password

    user = create_mock_user(is_active=False)
    user.hashed_password = hash_password("Password@123")

    user_repository.get_by_email.return_value = user

    request = LoginRequest(
        email="test@example.com",
        password="Password@123",
    )

    with pytest.raises(InactiveUserException):
        await auth_service.login_user(request)

    user_repository.get_by_email.assert_awaited_once_with(
        request.email,
    )


@pytest.mark.anyio
async def test_login_success(
    auth_service,
    user_repository,
    refresh_token_repository,
):
    from app.core.security import hash_password

    user = create_mock_user()
    user.hashed_password = hash_password("Password@123")

    user_repository.get_by_email.return_value = user

    request = LoginRequest(
        email="test@example.com",
        password="Password@123",
    )

    with patch("app.services.auth.RefreshToken") as mock_refresh_token:
        refresh_token_document = MagicMock()

        mock_refresh_token.return_value = refresh_token_document

        result = await auth_service.login_user(request)

    assert result is not None
    assert result.access_token
    assert result.refresh_token
    assert result.token_type == "bearer"

    user_repository.get_by_email.assert_awaited_once_with(
        request.email,
    )

    refresh_token_repository.create.assert_awaited_once_with(
        refresh_token_document,
    )
