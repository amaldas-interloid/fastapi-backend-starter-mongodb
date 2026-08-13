class AppException(Exception):
    """Base application exception."""


class UserAlreadyExistsException(AppException):
    """Raised when a user already exists."""


class UsernameAlreadyExistsException(AppException):
    """Raised when a username already exists."""


class InvalidCredentialsException(AppException):
    """Raised when email or password is invalid."""


class InactiveUserException(AppException):
    """Raised when the user account is inactive."""


class InvalidTokenException(Exception):
    def __init__(self, message: str = "Invalid or expired token."):
        self.message = message
        super().__init__(message)


class InvalidRefreshTokenException(AppException):
    pass


class ForbiddenException(AppException):
    """Raised when an authenticated user lacks permission."""

class RequestValidationError(AppException):
    pass
