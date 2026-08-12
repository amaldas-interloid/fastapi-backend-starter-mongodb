from unittest.mock import AsyncMock, MagicMock

import pytest

from app.exceptions.exceptions import (
    UserAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from app.repositories.user import UserRepository
from app.schemas.user import UserCreateRequest, UserUpdateRequest
from app.services.user import UserService


def create_mock_user(
    user_id: str = "test-user-id",
) -> MagicMock:
    user = MagicMock()
    user.id = user_id
    user.email = "test@example.com"
    user.username = "testuser"
    user.first_name = "Test"
    user.last_name = "User"
    user.is_active = True
    user.is_verified = False
    user.is_deleted = False

    return user


@pytest.fixture
def user_repository() -> MagicMock:
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(
    user_repository: MagicMock,
) -> UserService:
    return UserService(user_repository)


@pytest.mark.anyio
async def test_create_user_success( 
    user_service: UserService, 
    user_repository: MagicMock, 
    monkeypatch,
): 
    user_repository.get_by_email = AsyncMock( 
        return_value=None,
    ) 
    user_repository.get_by_username = AsyncMock( 
        return_value=None,
    )
    created_user = create_mock_user() 
    user_repository.create = AsyncMock( 
        return_value=created_user, 
    ) 
    mock_user = MagicMock( 
        return_value=created_user, 
    ) 
    monkeypatch.setattr( 
        "app.services.user.User", mock_user, 
    ) 
    request = UserCreateRequest(
         username="testuser", 
         email="test@example.com", 
         password="password123", 
         first_name="Test", 
         last_name="User", 
    ) 
    result = await user_service.create_user(request) 
    assert result is created_user 
    user_repository.get_by_email.assert_awaited_once_with( request.email, )
    user_repository.get_by_username.assert_awaited_once_with( request.username, )
    user_repository.create.assert_awaited_once_with( created_user, )
    mock_user.assert_called_once() 
    call_kwargs = mock_user.call_args.kwargs

    assert call_kwargs["email"] == request.email 
    assert call_kwargs["username"] == request.username
    assert call_kwargs["first_name"] == request.first_name
    assert call_kwargs["last_name"] == request.last_name
    assert call_kwargs["hashed_password"] != request.password

@pytest.mark.anyio
async def test_create_user_duplicate_email(
    user_service: UserService,
    user_repository: MagicMock,
):
    existing_user = create_mock_user()

    user_repository.get_by_email = AsyncMock(
        return_value=existing_user,
    )

    request = UserCreateRequest(
        username="testuser",
        email="test@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
    )

    with pytest.raises(UserAlreadyExistsException):
        await user_service.create_user(request)

    user_repository.get_by_email.assert_awaited_once_with(
        request.email,
    )


@pytest.mark.anyio
async def test_create_user_duplicate_username(
    user_service: UserService,
    user_repository: MagicMock,
):
    user_repository.get_by_email = AsyncMock(
        return_value=None,
    )

    existing_user = create_mock_user()

    user_repository.get_by_username = AsyncMock(
        return_value=existing_user,
    )

    request = UserCreateRequest(
        username="testuser",
        email="test@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
    )

    with pytest.raises(UsernameAlreadyExistsException):
        await user_service.create_user(request)

    user_repository.get_by_email.assert_awaited_once_with(
        request.email,
    )

    user_repository.get_by_username.assert_awaited_once_with(
        request.username,
    )


@pytest.mark.anyio
async def test_get_users(
    user_service: UserService,
    user_repository: MagicMock,
):
    users = [
        create_mock_user("user-1"),
        create_mock_user("user-2"),
    ]

    user_repository.get_all_users = AsyncMock(
        return_value=users,
    )

    user_repository.count_users = AsyncMock(
        return_value=10,
    )

    result_users, total = await user_service.get_users(
        page=2,
        page_size=2,
    )

    assert result_users == users
    assert total == 10

    user_repository.get_all_users.assert_awaited_once_with(
        skip=2,
        limit=2,
        username=None,
        email=None,
        is_active=None,
        is_verified=None,
        sort_by="created_at",
        sort_order=-1,
    )

    user_repository.count_users.assert_awaited_once_with(
        username=None,
        email=None,
        is_active=None,
        is_verified=None,
    )


@pytest.mark.anyio
async def test_get_user(
    user_service: UserService,
    user_repository: MagicMock,
):
    user = create_mock_user()

    user_repository.get_by_id = AsyncMock(
        return_value=user,
    )

    result = await user_service.get_user(
        "test-user-id",
    )

    assert result is user

    user_repository.get_by_id.assert_awaited_once_with(
        "test-user-id",
    )


@pytest.mark.anyio
async def test_get_user_not_found(
    user_service: UserService,
    user_repository: MagicMock,
):
    user_repository.get_by_id = AsyncMock(
        return_value=None,
    )

    result = await user_service.get_user(
        "unknown-user-id",
    )

    assert result is None

    user_repository.get_by_id.assert_awaited_once_with(
        "unknown-user-id",
    )


@pytest.mark.anyio
async def test_update_user_success(
    user_service: UserService,
    user_repository: MagicMock,
):
    user = create_mock_user()

    user_repository.get_by_email = AsyncMock(
        return_value=None,
    )

    user_repository.get_by_username = AsyncMock(
        return_value=None,
    )

    user_repository.update_user = AsyncMock(
        return_value=user,
    )

    request = UserUpdateRequest(
        first_name="Updated",
        last_name="Name",
    )

    result = await user_service.update_user(
        user,
        request,
    )

    assert result is user

    user_repository.update_user.assert_awaited_once()

    update_data = user_repository.update_user.call_args.args[1]

    assert update_data == {
        "first_name": "Updated",
        "last_name": "Name",
    }


@pytest.mark.anyio
async def test_update_user_duplicate_email(
    user_service: UserService,
    user_repository: MagicMock,
):
    user = create_mock_user()

    another_user = create_mock_user(
        "another-user-id",
    )

    user_repository.get_by_email = AsyncMock(
        return_value=another_user,
    )

    request = UserUpdateRequest(
        email="another@example.com",
    )

    with pytest.raises(UserAlreadyExistsException):
        await user_service.update_user(
            user,
            request,
        )


@pytest.mark.anyio
async def test_update_user_duplicate_username(
    user_service: UserService,
    user_repository: MagicMock,
):
    user = create_mock_user()

    another_user = create_mock_user(
        "another-user-id",
    )

    user_repository.get_by_username = AsyncMock(
        return_value=another_user,
    )

    request = UserUpdateRequest(
        username="anotheruser",
    )

    with pytest.raises(UsernameAlreadyExistsException):
        await user_service.update_user(
            user,
            request,
        )


@pytest.mark.anyio
async def test_update_user_password(
    user_service: UserService,
    user_repository: MagicMock,
):
    user = create_mock_user()

    user_repository.update_user = AsyncMock(
        return_value=user,
    )

    request = UserUpdateRequest(
        password="newpassword123",
    )

    result = await user_service.update_user(
        user,
        request,
    )

    assert result is user

    user_repository.update_user.assert_awaited_once()

    update_data = user_repository.update_user.call_args.args[1]

    assert "password" not in update_data
    assert "hashed_password" in update_data
    assert update_data["hashed_password"] != "newpassword123"


@pytest.mark.anyio
async def test_delete_user(
    user_service: UserService,
    user_repository: MagicMock,
):
    user = create_mock_user()

    user_repository.soft_delete = AsyncMock(
        return_value=user,
    )

    result = await user_service.delete_user(user)

    assert result is user

    user_repository.soft_delete.assert_awaited_once_with(
        user,
    )

