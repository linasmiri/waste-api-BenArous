"""
JWT helper functions for authentication
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time delta
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify JWT access token.
    
    Args:
        token: JWT token to verify
        
    Returns:
        dict: Decoded token payload
        
    Raises:
        jwt.ExpiredSignatureError: If token is expired
        jwt.InvalidTokenError: If token is invalid
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
