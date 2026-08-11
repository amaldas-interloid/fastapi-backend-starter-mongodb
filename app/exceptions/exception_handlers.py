from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    ForbiddenException,
    InactiveUserException,
    InvalidCredentialsException,
    InvalidRefreshTokenException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UsernameAlreadyExistsException,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_exception_handler(
        request: Request,
        exc: UserAlreadyExistsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "message": "Email already exists.",
                "data": None,
            },
        )

    @app.exception_handler(UsernameAlreadyExistsException)
    async def username_already_exists_exception_handler(
        request: Request,
        exc: UsernameAlreadyExistsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "message": "Username already exists.",
                "data": None,
            },
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_exception_handler(
        request: Request,
        exc: InvalidCredentialsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": "Invalid email or password.",
                "data": None,
            },
        )

    @app.exception_handler(InactiveUserException)
    async def inactive_user_exception_handler(
        request: Request,
        exc: InactiveUserException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "success": False,
                "message": "User account is inactive.",
                "data": None,
            },
        )

    @app.exception_handler(InvalidRefreshTokenException)
    async def invalid_refresh_token_exception_handler(
        request: Request,
        exc: InvalidRefreshTokenException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": "Invalid refresh token.",
                "data": None,
            },
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_exception_handler(
        request: Request,
        exc: ForbiddenException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "success": False,
                "message": (
                    "You do not have permission "
                    "to perform this action."
                ),
                "data": None,
            },
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exception_handler(
        request: Request,
        exc: InvalidTokenException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": str(exc.detail),
                "data": None,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": "Validation error.",
                "data": None,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "An unexpected error occurred.",
                "data": None,
            },
        )

