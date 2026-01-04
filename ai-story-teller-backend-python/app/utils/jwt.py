"""JWT token utilities."""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Response
from app.config import settings
from app.utils.logger import logger


def create_access_token(user_id: str) -> str:
    """Create JWT token for user."""
    expire = datetime.utcnow() + timedelta(days=settings.jwt_expiration_days)
    to_encode = {"userId": user_id, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return user_id."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("userId")
        return user_id
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        return None


def set_auth_cookie(response: Response, token: str) -> None:
    """Set JWT token in HTTP-only cookie."""
    max_age = settings.jwt_expiration_days * 24 * 60 * 60  # seconds
    response.set_cookie(
        key="jwt",
        value=token,
        max_age=max_age,
        httponly=True,
        samesite="lax",
        secure=False  # Set to True in production with HTTPS
    )


def clear_auth_cookie(response: Response) -> None:
    """Clear JWT cookie."""
    response.delete_cookie(key="jwt", samesite="lax")

