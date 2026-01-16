""" Create FastAPI router for authentication in api/auth.py:

Import APIRouter, Depends, HTTPException, status from fastapi
Import Session from sqlalchemy.orm
Import CryptContext from passlib.context
Import datetime, timedelta, jwt
Import get_db from app.database
Import User, UserRole from app.models
Import UserRegister, UserLogin, UserResponse from app.schemas
Import create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES from app.main
Import logger from app.utils.logger
Import ErrorCatalog from app.utils.error_catalog
Create router with prefix="/api/v1/auth" and tags=["Auth"]
Create pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Create hash_password(password) function
Create verify_password(plain, hashed) function
POST /register endpoint: check if user exists, hash password, create user, log action, return UserResponse
POST /login endpoint: verify credentials, create JWT token, log action, return access_token and token_type"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserRegister, UserLogin, UserResponse
from app.utils.jwt_helper import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.logger import logger
from app.utils.error_catalog import ErrorCatalog

# Create router
router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to check against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        UserResponse: Newly created user details
        
    Raises:
        HTTPException: If user already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        error = ErrorCatalog.get_error("USER_001")
        logger.warning(f"Registration failed: User '{user_data.username}' already exists")
        raise HTTPException(
            status_code=error["code"],
            detail=error["message"]
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        phone=user_data.phone,
        password_hash=hashed_password,
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"User '{user_data.username}' registered successfully with role '{user_data.role}'")
    
    return new_user


@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint.
    
    Args:
        credentials: User login credentials
        db: Database session
        
    Returns:
        dict: Access token and token type
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by username
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        error = ErrorCatalog.get_error("AUTH_001")
        logger.warning(f"Login failed: Invalid credentials for user '{credentials.username}'")
        raise HTTPException(
            status_code=error["code"],
            detail=error["message"]
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User '{user.username}' logged in successfully")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
