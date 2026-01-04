"""Custom exception classes for the application."""
from typing import Any, Dict, Optional


class AppException(Exception):
    """Base exception for the application."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppException):
    """Raised when validation fails."""
    
    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class NotFoundError(AppException):
    """Raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=404, details=details)


class UnauthorizedError(AppException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)


class ForbiddenError(AppException):
    """Raised when access is forbidden."""
    
    def __init__(self, message: str = "Forbidden", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=403, details=details)


class BadRequestError(AppException):
    """Raised when a bad request is made."""
    
    def __init__(self, message: str = "Bad request", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)

