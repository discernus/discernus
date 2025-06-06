"""
Authentication utilities for Narrative Gravity Analysis.
Implements Epic 1 requirement G: Security & Access Control with JWT tokens and role-based access.
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..models.models import User
from ..models.base import get_db
from ..utils.logging_config import get_logger, ErrorCodes, metrics_collector

logger = get_logger(__name__)

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token extractor
security = HTTPBearer(auto_error=False)

class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass

class AuthorizationError(Exception):
    """Custom exception for authorization errors."""
    pass

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token (user_id, username, role, etc.)
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a JWT refresh token with longer expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        AuthenticationError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.error("JWT decode failed", error_code=ErrorCodes.API_AUTHENTICATION_ERROR, 
                    extra_data={"error": str(e)}, exception=e)
        raise AuthenticationError("Invalid token")

def get_current_user_from_token(token: str, db: Session) -> User:
    """
    Get current user from JWT token.
    
    Args:
        token: JWT token string
        db: Database session
        
    Returns:
        User object
        
    Raises:
        AuthenticationError: If token is invalid or user not found
    """
    try:
        payload = decode_token(token)
        user_id: int = payload.get("user_id")
        username: str = payload.get("username")
        
        if user_id is None or username is None:
            raise AuthenticationError("Invalid token payload")
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id, User.username == username).first()
        if user is None:
            logger.warning("User not found for valid token", 
                         error_code=ErrorCodes.API_AUTHENTICATION_ERROR,
                         extra_data={"user_id": user_id, "username": username})
            raise AuthenticationError("User not found")
        
        if not user.is_active:
            logger.warning("Inactive user attempted access", 
                         error_code=ErrorCodes.API_AUTHENTICATION_ERROR,
                         extra_data={"user_id": user_id, "username": username})
            raise AuthenticationError("Inactive user")
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user
        
    except AuthenticationError:
        raise
    except Exception as e:
        logger.error("Authentication error", error_code=ErrorCodes.API_AUTHENTICATION_ERROR, 
                    exception=e)
        raise AuthenticationError("Authentication failed")

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate user with username and password.
    
    Args:
        db: Database session
        username: Username or email
        password: Plain text password
        
    Returns:
        User object if authentication successful, None otherwise
    """
    # Look up user by username or email
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    if not user:
        logger.warning("Authentication attempt for non-existent user", 
                      error_code=ErrorCodes.API_AUTHENTICATION_ERROR,
                      extra_data={"username": username})
        return None
    
    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        logger.warning("Authentication attempt for locked account", 
                      error_code=ErrorCodes.API_AUTHENTICATION_ERROR,
                      extra_data={"user_id": user.id, "username": username, 
                                "locked_until": user.locked_until.isoformat()})
        return None
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        # Increment failed login attempts
        user.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(hours=1)
            logger.warning("Account locked due to failed login attempts", 
                          error_code=ErrorCodes.API_AUTHENTICATION_ERROR,
                          extra_data={"user_id": user.id, "username": username})
        
        db.commit()
        logger.warning("Failed password verification", 
                      error_code=ErrorCodes.API_AUTHENTICATION_ERROR,
                      extra_data={"user_id": user.id, "username": username, 
                                "failed_attempts": user.failed_login_attempts})
        return None
    
    # Reset failed login attempts on successful authentication
    if user.failed_login_attempts > 0:
        user.failed_login_attempts = 0
        user.locked_until = None
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    logger.info("User authenticated successfully", 
                extra_data={"user_id": user.id, "username": username, "role": user.role})
    return user

# FastAPI Dependencies

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency to get current authenticated user.
    
    Raises:
        HTTPException: If authentication fails
    """
    if not credentials:
        logger.warning("Missing authorization header", 
                      error_code=ErrorCodes.API_AUTHENTICATION_ERROR)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user = get_current_user_from_token(credentials.credentials, db)
        return user
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    FastAPI dependency to ensure current user has admin role.
    Implements Epic 1 requirement: only admins can upload corpora and start jobs.
    
    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != "admin":
        logger.warning("Non-admin user attempted admin operation", 
                      error_code=ErrorCodes.API_AUTHORIZATION_ERROR,
                      extra_data={"user_id": current_user.id, "username": current_user.username, 
                                "role": current_user.role})
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    FastAPI dependency to get current user if authenticated, None otherwise.
    Used for endpoints that have optional authentication.
    """
    if not credentials:
        return None
    
    try:
        user = get_current_user_from_token(credentials.credentials, db)
        return user
    except AuthenticationError:
        return None

def check_rate_limit(user: User, endpoint: str) -> bool:
    """
    Check if user has exceeded rate limits.
    
    Args:
        user: User object
        endpoint: Endpoint being accessed
        
    Returns:
        True if within rate limit, False otherwise
    """
    # TODO: Implement Redis-based rate limiting
    # For now, just return True (no rate limiting)
    return True

def has_permission(user: User, operation: str, resource: str = None) -> bool:
    """
    Check if user has permission for a specific operation.
    
    Args:
        user: User object
        operation: Operation type (create, read, update, delete)
        resource: Optional resource type (corpus, job, etc.)
        
    Returns:
        True if user has permission, False otherwise
    """
    # Admin users have all permissions
    if user.role == "admin":
        return True
    
    # Regular users can read most resources
    if operation == "read":
        return True
    
    # Regular users cannot create corpora or jobs
    if operation == "create" and resource in ["corpus", "job"]:
        return False
    
    # Default deny for other operations
    return False 