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


class InvalidRefreshTokenException(AppException):
    pass


class ForbiddenException(AppException):
    """Raised when an authenticated user lacks permission."""
