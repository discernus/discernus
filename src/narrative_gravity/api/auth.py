"""
Authentication endpoints for Narrative Gravity Analysis.
Implements Epic 1 requirement G: Security & Access Control.
"""

from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models.models import User
from ..models.base import get_db
from ..utils.auth import (
    authenticate_user, create_access_token, create_refresh_token, 
    hash_password, get_current_user, get_current_admin_user,
    decode_token, AuthenticationError, ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..utils.sanitization import (
    validate_username, validate_email, sanitize_string, SanitizationError
)
from ..utils.logging_config import get_logger, ErrorCodes, metrics_collector
from .schemas import (
    UserCreate, UserLogin, UserResponse, UserUpdate, PasswordChange,
    TokenResponse, TokenRefresh
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = get_logger(__name__)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    Note: Only admins can create other admin users.
    """
    try:
        # Sanitize input
        username = validate_username(user_data.username)
        email = validate_email(user_data.email)
        full_name = sanitize_string(user_data.full_name, max_length=255) if user_data.full_name else None
        organization = sanitize_string(user_data.organization, max_length=255) if user_data.organization else None
        
        # Check if username already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                logger.warning("Registration attempt with existing username", 
                              error_code=ErrorCodes.API_VALIDATION_ERROR,
                              extra_data={"username": username})
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )
            else:
                logger.warning("Registration attempt with existing email", 
                              error_code=ErrorCodes.API_VALIDATION_ERROR,
                              extra_data={"email": email})
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user (only admins can create admin users)
        role = "user"  # Default role for self-registration
        if user_data.role == "admin":
            # For demo purposes, allow the first user to be admin
            # In production, this would require admin approval
            user_count = db.query(User).count()
            if user_count == 0:
                role = "admin"
                logger.info("First user registered as admin", 
                           extra_data={"username": username})
            else:
                logger.warning("Non-admin user attempted to register as admin", 
                              error_code=ErrorCodes.API_AUTHORIZATION_ERROR,
                              extra_data={"username": username})
                role = "user"  # Override to user role
        
        # Create user
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            organization=organization,
            role=role,
            is_active=True,
            is_verified=False
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info("User registered successfully", 
                   extra_data={"user_id": user.id, "username": username, "role": role})
        metrics_collector.increment_metric("users_registered_total", {"role": role})
        
        return user
        
    except SanitizationError as e:
        logger.warning("Registration input sanitization error", 
                      error_code=ErrorCodes.API_VALIDATION_ERROR,
                      extra_data={"error": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("User registration error", 
                    error_code=ErrorCodes.DATABASE_CONNECTION_ERROR,
                    exception=e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    try:
        # Sanitize input
        username = sanitize_string(login_data.username, max_length=255)
        
        # Authenticate user
        user = authenticate_user(db, username, login_data.password)
        if not user:
            logger.warning("Failed login attempt", 
                          error_code=ErrorCodes.API_AUTHENTICATION_ERROR,
                          extra_data={"username": username})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create tokens
        token_data = {"user_id": user.id, "username": user.username, "role": user.role}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        logger.info("User logged in successfully", 
                   extra_data={"user_id": user.id, "username": user.username, "role": user.role})
        metrics_collector.increment_metric("user_logins_total", {"role": user.role})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user
        )
        
    except SanitizationError as e:
        logger.warning("Login input sanitization error", 
                      error_code=ErrorCodes.API_VALIDATION_ERROR,
                      extra_data={"error": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    try:
        # Decode refresh token
        payload = decode_token(token_data.refresh_token)
        
        if payload.get("type") != "refresh":
            raise AuthenticationError("Invalid token type")
        
        user_id = payload.get("user_id")
        username = payload.get("username")
        
        if not user_id or not username:
            raise AuthenticationError("Invalid token payload")
        
        # Get user
        user = db.query(User).filter(User.id == user_id, User.username == username).first()
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        # Create new tokens
        token_data = {"user_id": user.id, "username": user.username, "role": user.role}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        logger.info("Token refreshed successfully", 
                   extra_data={"user_id": user.id, "username": user.username})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user
        )
        
    except AuthenticationError as e:
        logger.warning("Token refresh failed", 
                      error_code=ErrorCodes.API_AUTHENTICATION_ERROR,
                      extra_data={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user information."""
    try:
        # Sanitize input
        if user_data.full_name:
            current_user.full_name = sanitize_string(user_data.full_name, max_length=255)
        
        if user_data.organization:
            current_user.organization = sanitize_string(user_data.organization, max_length=255)
        
        if user_data.email:
            # Check if email already exists
            email = validate_email(user_data.email)
            existing_user = db.query(User).filter(
                User.email == email, User.id != current_user.id
            ).first()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            
            current_user.email = email
        
        db.commit()
        db.refresh(current_user)
        
        logger.info("User updated profile", 
                   extra_data={"user_id": current_user.id, "username": current_user.username})
        
        return current_user
        
    except SanitizationError as e:
        logger.warning("Profile update input sanitization error", 
                      error_code=ErrorCodes.API_VALIDATION_ERROR,
                      extra_data={"error": str(e), "user_id": current_user.id})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Profile update error", 
                    error_code=ErrorCodes.DATABASE_CONNECTION_ERROR,
                    exception=e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password."""
    try:
        from ..utils.auth import verify_password
        
        # Verify current password
        if not verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Hash new password
        current_user.hashed_password = hash_password(password_data.new_password)
        
        # Reset failed login attempts
        current_user.failed_login_attempts = 0
        current_user.locked_until = None
        
        db.commit()
        
        logger.info("User changed password", 
                   extra_data={"user_id": current_user.id, "username": current_user.username})
        
        return {"message": "Password changed successfully"}
        
    except Exception as e:
        logger.error("Password change error", 
                    error_code=ErrorCodes.DATABASE_CONNECTION_ERROR,
                    exception=e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )

# Admin endpoints

@router.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """List all users (admin only)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    role: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update user role (admin only)."""
    if role not in ["admin", "user"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.id == current_user.id and role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Cannot remove admin role from yourself"
        )
    
    old_role = user.role
    user.role = role
    db.commit()
    
    logger.info("User role updated", 
               extra_data={"user_id": user.id, "username": user.username, 
                         "old_role": old_role, "new_role": role, 
                         "updated_by": current_user.username})
    
    return {"message": f"User role updated to {role}"}

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    is_active: bool,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update user active status (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.id == current_user.id and not is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Cannot deactivate yourself"
        )
    
    user.is_active = is_active
    db.commit()
    
    logger.info("User status updated", 
               extra_data={"user_id": user.id, "username": user.username, 
                         "is_active": is_active, "updated_by": current_user.username})
    
    return {"message": f"User {'activated' if is_active else 'deactivated'}"}

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Cannot delete yourself"
        )
    
    db.delete(user)
    db.commit()
    
    logger.info("User deleted", 
               extra_data={"user_id": user.id, "username": user.username, 
                         "deleted_by": current_user.username})
    
    return {"message": "User deleted"} 