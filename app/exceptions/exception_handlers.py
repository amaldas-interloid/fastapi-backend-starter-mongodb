from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    ForbiddenException,
    InactiveUserException,
    InvalidCredentialsException,
    InvalidRefreshTokenException,
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
                "detail": "Email already exists.",
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
                "detail": "Username already exists.",
            },
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_exception_handler(
        request: Request,
        exc: InvalidCredentialsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid email or password."},
        )

    @app.exception_handler(InactiveUserException)
    async def inactive_user_exception_handler(
        request: Request,
        exc: InactiveUserException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "User account is inactive."},
        )

    @app.exception_handler(InvalidRefreshTokenException)
    async def invalid_refresh_token_exception_handler(
        request: Request,
        exc: InvalidRefreshTokenException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid Refresh_token"},
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_exception_handler(
        request: Request,
        exc: ForbiddenException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": "You do not have permission to perform this action.",
            },
        )
