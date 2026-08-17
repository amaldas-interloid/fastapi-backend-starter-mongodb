from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import (
    get_current_user,
    require_permission,
)
from app.enums.permission import PermissionName
from app.enums.sort import SortOrder, UserSortField
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.common import APIResponse
from app.schemas.pagination import (
    PaginatedResponse,
    PaginationResponse,
)
from app.schemas.user import (
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
)
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service() -> UserService:
    return UserService(UserRepository())


@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> APIResponse[UserResponse]:
    return APIResponse(
        success=True,
        message="User profile retrieved successfully.",
        data=UserResponse.model_validate(current_user),
    )


@router.get(
    "",
    response_model=APIResponse[PaginatedResponse[UserResponse]],
    dependencies=[Depends(require_permission(PermissionName.USERS_READ))],
)
async def get_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    username: str | None = Query(
        default=None,
        min_length=1,
        max_length=50,
    ),
    email: str | None = Query(
        default=None,
        min_length=1,
        max_length=255,
    ),
    is_active: bool | None = Query(
        default=None,
    ),
    is_verified: bool | None = Query(
        default=None,
    ),
    sort_by: UserSortField = Query(
        default=UserSortField.CREATED_AT,
    ),
    sort_order: SortOrder = Query(
        default=SortOrder.DESC,
    ),
    service: UserService = Depends(get_user_service),
) -> APIResponse[PaginatedResponse[UserResponse]]:
    users, total = await service.get_users(
        page=page,
        page_size=page_size,
        username=username,
        email=email,
        is_active=is_active,
        is_verified=is_verified,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    data = PaginatedResponse(
        items=[UserResponse.model_validate(user) for user in users],
        pagination=PaginationResponse(
            page=page,
            page_size=page_size,
            total=total,
            pages=total_pages,
        ),
    )

    return APIResponse(
        success=True,
        message="Users retrieved successfully.",
        data=data,
    )


@router.get(
    "/{user_id}",
    response_model=APIResponse[UserResponse],
    dependencies=[Depends(require_permission(PermissionName.USERS_READ))],
)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> APIResponse[UserResponse]:
    user = await service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return APIResponse(
        success=True,
        message="User retrieved successfully.",
        data=UserResponse.model_validate(user),
    )


@router.post(
    "",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(PermissionName.USERS_CREATE))],
)
async def create_user(
    request: UserCreateRequest,
    service: UserService = Depends(get_user_service),
) -> APIResponse[UserResponse]:
    user_response = await service.create_user(request)

    return APIResponse(
        success=True,
        message="User created successfully",
        data=user_response,
    )


@router.patch(
    "/{user_id}",
    response_model=APIResponse[UserResponse],
    dependencies=[Depends(require_permission(PermissionName.USERS_UPDATE))],
)
async def update_user(
    user_id: str,
    request: UserUpdateRequest,
    service: UserService = Depends(get_user_service),
) -> APIResponse[UserResponse]:
    user = await service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    update_user = await service.update_user(
        user,
        request,
    )

    return APIResponse(
        success=True,
        message="User updated successfully",
        data=UserResponse.model_validate(update_user),
    )


@router.delete(
    "/{user_id}",
    response_model=APIResponse[UserResponse],
    dependencies=[Depends(require_permission(PermissionName.USERS_DELETE))],
)
async def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> APIResponse[UserResponse]:
    user = await service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    deleted_user = await service.delete_user(user)
    return APIResponse(
        success=True,
        message="User deleted successfully.",
        data=UserResponse.model_validate(deleted_user),
    )
