"""Authentication middleware for protected routes."""
from fastapi import Request, HTTPException, status, Cookie
from typing import Optional
from app.utils.jwt import verify_token
from app.schemas.user import User
from app.exceptions import UnauthorizedError
from app.utils.logger import logger


async def get_current_user(request: Request) -> User:
    """
    Dependency function for protected routes.
    Extracts JWT token from cookie and returns authenticated user.
    """
    # Try to get token from cookie
    token = request.cookies.get("jwt")
    
    if not token:
        logger.warning("No JWT token found in cookies")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify token
    user_id = verify_token(token)
    if not user_id:
        logger.warning("Invalid or expired JWT token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Get user from database
    try:
        user = await User.get(user_id)
        if not user:
            logger.warning(f"User not found for ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return user
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error authenticating user"
        )

