from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.exceptions.exception_handlers import register_exception_handlers
from app.exceptions.exceptions import (
    ForbiddenException,
    InactiveUserException,
    InvalidCredentialsException,
    InvalidRefreshTokenException,
    UserAlreadyExistsException,
    UsernameAlreadyExistsException,
)


def create_test_app(
    exception_class: type[Exception],
) -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/test")
    async def test_endpoint():
        raise exception_class()

    return app


def assert_error_response(
    exception_class: type[Exception],
    expected_status: int,
    expected_message: str,
) -> None:
    app = create_test_app(exception_class)
    client = TestClient(app)

    response = client.get("/test")

    assert response.status_code == expected_status
    assert response.json() == {
        "success": False,
        "message": expected_message,
        "data": None,
    }


def test_user_already_exists_exception():
    assert_error_response(
        UserAlreadyExistsException,
        409,
        "Email already exists.",
    )


def test_username_already_exists_exception():
    assert_error_response(
        UsernameAlreadyExistsException,
        409,
        "Username already exists.",
    )


def test_invalid_credentials_exception():
    assert_error_response(
        InvalidCredentialsException,
        401,
        "Invalid email or password.",
    )


def test_inactive_user_exception():
    assert_error_response(
        InactiveUserException,
        403,
        "User account is inactive.",
    )


def test_invalid_refresh_token_exception():
    assert_error_response(
        InvalidRefreshTokenException,
        401,
        "Invalid refresh token.",
    )


def test_forbidden_exception():
    assert_error_response(
        ForbiddenException,
        403,
        "You do not have permission to perform this action.",
    )
