"""
Create main.py for FastAPI application with:

Import FastAPI, Depends, HTTPException from fastapi
Import CORSMiddleware from fastapi.middleware.cors
Import JSONResponse from fastapi.responses
Import Session from sqlalchemy.orm
Import datetime, timedelta, jwt, os
Import load_dotenv from dotenv
Import get_db, engine from app.database
Import Base from app.models
Import logger from app.utils.logger
Import ErrorCatalog from app.utils.error_catalog
Call load_dotenv()
Create tables with Base.metadata.create_all(bind=engine)
Initialize FastAPI app with title="Waste Sorting & Recycling Optimization API", version="1.0.0", description="API for Barbecha onboarding and municipal route optimization in Ben Arous, Tunisia"
Add CORS middleware allowing all origins
Add logging middleware that logs request method and URL path
Add global HTTPException handler that logs errors
Create /health GET endpoint that returns status, timestamp, service name
Add JWT helper functions: create_access_token(data, expires_delta) and verify_token(token) using HS256 algorithm
Set SECRET_KEY from environment with default, ALGORITHM="HS256", ACCESS_TOKEN_EXPIRE_MINUTES=30
Add placeholder /api/v1 GET endpoint
"""
"""
COPILOT PROMPT USED:
...
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import os
from dotenv import load_dotenv

from .database import get_db, engine
from .models import Base
from .utils.logger import logger
from .utils.error_catalog import ErrorCatalog

# Load environment variables
load_dotenv()

# Create database tables
# Base.metadata.create_all(bind=engine)  # Commented out - will enable with Docker


# Initialize FastAPI app
app = FastAPI(
    title="Waste Sorting & Recycling Optimization API",
    version="1.0.0",
    description="API for Barbecha onboarding and municipal route optimization in Ben Arous, Tunisia"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Include routers
from app.api import auth
app.include_router(auth.router)

# Health Check Endpoint
@app.get("/health")
async def health_check():
    logger.info("Health check request received")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Waste Sorting & Recycling Optimization API"
    }

# Placeholder endpoint
@app.get("/api/v1")
async def api_v1_root():
    logger.info("API v1 root endpoint accessed")
    return {
        "message": "Welcome to Waste Sorting & Recycling Optimization API",
        "version": "1.0.0",
        "endpoints": "/docs for API documentation"
    }
