"""User authentication and management routes."""
from fastapi import APIRouter, Depends, Response, status
from app.models.user import UserSignUpRequest, UserLoginRequest, LoginResponse, UserResponse
from app.services.user_service import user_service
from app.utils.jwt import create_access_token, set_auth_cookie, clear_auth_cookie
from app.middleware.auth import get_current_user
from app.schemas.user import User
from app.exceptions import ValidationError
from app.utils.logger import logger

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserSignUpRequest,
    response: Response
):
    """
    User registration endpoint.
    Creates a new user account and sets authentication cookie.
    """
    try:
        user = await user_service.create_user(user_data)
        token = create_access_token(str(user.id))
        set_auth_cookie(response, token)
        
        # Return flat response
        return {
            "userId": str(user.id),
            "parentName": user.parent_name,
            "parentEmail": user.parent_email,
            "childName": user.child_name,
            "childAge": user.child_age,
            "childStandard": user.child_standard,
            "message": "User created successfully"
        }
    except ValidationError as e:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    login_data: UserLoginRequest,
    response: Response
):
    """
    User login endpoint.
    Authenticates user and sets authentication cookie.
    """
    try:
        user = await user_service.authenticate_user(login_data)
        token = create_access_token(str(user.id))
        set_auth_cookie(response, token)
        
        return LoginResponse(
            user_id=str(user.id),
            parent_name=user.parent_name,
            parent_email=user.parent_email,
            child_name=user.child_name,
            child_age=user.child_age,
            child_standard=user.child_standard,
            message="User logged in successfully"
        )
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    """
    User logout endpoint.
    Clears authentication cookie.
    """
    try:
        clear_auth_cookie(response)
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information.
    Protected route that returns authenticated user's data.
    """
    return user_service.user_to_response(current_user)

