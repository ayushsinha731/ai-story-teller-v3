"""User service for authentication and user management."""
from typing import Optional
from fastapi import HTTPException, status
from app.schemas.user import User
from app.models.user import UserSignUpRequest, UserLoginRequest, UserResponse
from app.utils.password import hash_password, verify_password
from app.exceptions import ValidationError, NotFoundError, UnauthorizedError
from app.utils.logger import logger


class UserService:
    """Service for user-related operations."""
    
    @staticmethod
    async def create_user(user_data: UserSignUpRequest) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User registration data
            
        Returns:
            Created user document
        """
        try:
            # Check if user already exists
            existing_user = await User.find_one(User.parent_email == user_data.parent_email)
            if existing_user:
                raise ValidationError("User already exists with this email")
            
            # Hash password
            hashed_password = hash_password(user_data.password)
            
            # Create user
            user = User(
                parent_name=user_data.parent_name,
                parent_email=user_data.parent_email,
                child_name=user_data.child_name,
                child_age=user_data.child_age,
                password=hashed_password,
                child_standard=user_data.child_standard
            )
            await user.insert()
            
            logger.info(f"User created: {user_data.parent_email}")
            return user
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise Exception(f"Failed to create user: {str(e)}")
    
    @staticmethod
    async def authenticate_user(login_data: UserLoginRequest) -> User:
        """
        Authenticate user and return user document.
        
        Args:
            login_data: User login credentials
            
        Returns:
            Authenticated user document
        """
        try:
            user = await User.find_one(User.parent_email == login_data.parent_email)
            if not user:
                raise UnauthorizedError("Invalid credentials")
            
            if not verify_password(login_data.password, user.password):
                raise UnauthorizedError("Invalid credentials")
            
            logger.info(f"User authenticated: {login_data.parent_email}")
            return user
            
        except UnauthorizedError:
            raise
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            raise UnauthorizedError("Authentication failed")
    
    @staticmethod
    def user_to_response(user: User) -> UserResponse:
        """
        Convert user document to response model.
        
        Args:
            user: User document
            
        Returns:
            User response model
        """
        return UserResponse(
            user_id=str(user.id),
            parent_name=user.parent_name,
            parent_email=user.parent_email,
            child_name=user.child_name,
            child_age=user.child_age,
            child_standard=user.child_standard
        )


user_service = UserService()

