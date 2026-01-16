"""
COPILOT PROMPT USED:
Create Pydantic v2 request and response schemas for waste API with these models:

1. UserRegister (username: str min 3 chars, phone: str regex for Tunisia +216, password: str min 6, role: UserRole enum)
2. UserLogin (username: str, password: str)
3. UserResponse (id, username, role, created_at) - use from_attributes=True
4. CollectorOnboard (user_id: int)
5. CollectorResponse (id, user_id, verification_status, total_batches, total_weight) - use from_attributes=True
6. BatchCreate (collector_id: int, material_type: str must be PET|HDPE|PP|Aluminium|Glass, weight: float > 0)
7. BatchResponse (id, collector_id, material_type, weight, status, qr_code, created_at) - use from_attributes=True
8. HotspotReportCreate (hotspot_id: int, report_type: str must be overflow|illegal_dump|missed_pickup)
9. HotspotResponse (id, location_name, latitude, longitude, urgency_score, report_count) - use from_attributes=True
10. RouteOptimize (date: datetime, available_trucks: int > 0, available_time: int > 0 minutes)

Use Pydantic Field for validation. Include the UserRole enum definition.

MODEL USED: Claude Haiku 4.5 via GitHub Copilot
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import enum
import re


# Enums
class UserRole(str, enum.Enum):
    CITIZEN = "citizen"
    COLLECTOR = "collector"
    MUNICIPALITY = "municipality"
    RECYCLER = "recycler"


class MaterialType(str, enum.Enum):
    PET = "PET"
    HDPE = "HDPE"
    PP = "PP"
    ALUMINIUM = "Aluminium"
    GLASS = "Glass"


class ReportType(str, enum.Enum):
    OVERFLOW = "overflow"
    ILLEGAL_DUMP = "illegal_dump"
    MISSED_PICKUP = "missed_pickup"


# User Schemas
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, description="Username must be at least 3 characters")
    phone: str = Field(..., description="Phone number for Tunisia (format: +216XXXXXXXX)")
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    role: UserRole = Field(default=UserRole.CITIZEN, description="User role")

    @field_validator("phone")
    def validate_phone(cls, v):
        # Tunisia phone number validation: +216 followed by 8 digits
        if not re.match(r"^\+216\d{8}$", v):
            raise ValueError("Phone must be a valid Tunisia number (format: +216XXXXXXXXX)")
        return v


class UserLogin(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


# Collector Schemas
class CollectorOnboard(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID must be positive")


class CollectorResponse(BaseModel):
    id: int
    user_id: int
    verification_status: str
    total_batches: int
    total_weight: float

    class Config:
        from_attributes = True


# Batch Schemas
class BatchCreate(BaseModel):
    collector_id: int = Field(..., gt=0, description="Collector ID must be positive")
    material_type: MaterialType = Field(..., description="Material type")
    weight: float = Field(..., gt=0, description="Weight must be greater than 0")


class BatchResponse(BaseModel):
    id: int
    collector_id: int
    material_type: str
    weight: float
    status: str
    qr_code: str
    created_at: datetime

    class Config:
        from_attributes = True


# Hotspot Schemas
class HotspotReportCreate(BaseModel):
    hotspot_id: int = Field(..., gt=0, description="Hotspot ID must be positive")
    report_type: ReportType = Field(..., description="Type of report")


class HotspotResponse(BaseModel):
    id: int
    location_name: str
    latitude: float
    longitude: float
    urgency_score: int
    report_count: int

    class Config:
        from_attributes = True


# Route Schemas
class RouteOptimize(BaseModel):
    date: datetime = Field(..., description="Route date")
    available_trucks: int = Field(..., gt=0, description="Number of available trucks must be greater than 0")
    available_time: int = Field(..., gt=0, description="Available time in minutes must be greater than 0")
