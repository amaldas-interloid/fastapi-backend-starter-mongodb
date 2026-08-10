from app.core.config import settings


def test_settings_loaded():
    assert settings.APP_NAME
    assert settings.APP_VERSION
    assert settings.HOST
    assert settings.PORT > 0
    assert settings.MONGODB_URL
    assert settings.DATABASE_NAME
    assert settings.JWT_SECRET_KEY
    assert settings.JWT_ALGORITHM


def test_token_expiration_settings():
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
    assert settings.REFRESH_TOKEN_EXPIRE_DAYS > 0