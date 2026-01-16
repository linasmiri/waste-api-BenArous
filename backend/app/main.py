from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from typing import Optional

from .database import get_db, engine
from .models import Base
from .utils.logger import logger
from .utils.error_catalog import ErrorCatalog

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Waste Sorting & Recycling Optimization API",
    version="1.0.0",
    description="API for Barbecha onboarding and municipal route optimization in Ben Arous, Tunisia"
)

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response


# Global HTTPException handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# JWT Helper Functions
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
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        error = ErrorCatalog.get_error("AUTH_001")
        logger.error("Token expired")
        raise HTTPException(
            status_code=error["code"],
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        error = ErrorCatalog.get_error("AUTH_001")
        logger.error("Invalid token")
        raise HTTPException(
            status_code=error["code"],
            detail="Invalid token"
        )


# Health Check Endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        dict: Status, timestamp, and service name
    """
    logger.info("Health check request received")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Waste Sorting & Recycling Optimization API"
    }


# Placeholder endpoint
@app.get("/api/v1")
async def api_v1_root():
    """
    API v1 root endpoint.
    
    Returns:
        dict: Welcome message and API information
    """
    logger.info("API v1 root endpoint accessed")
    return {
        "message": "Welcome to Waste Sorting & Recycling Optimization API",
        "version": "1.0.0",
        "endpoints": "/docs for API documentation"
    }
