from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    CITIZEN = "citizen"
    COLLECTOR = "collector"
    MUNICIPALITY = "municipality"
    RECYCLER = "recycler"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.CITIZEN)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    collector = relationship("Collector", back_populates="user", uselist=False)
    batches = relationship("Batch", back_populates="creator")
    reports = relationship("HotspotReport", back_populates="reporter")

class Collector(Base):
    __tablename__ = "collectors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    verification_status = Column(String, default="pending")  # pending, verified, rejected
    total_batches = Column(Integer, default=0)
    total_weight = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="collector")
    batches = relationship("Batch", back_populates="collector")

class Batch(Base):
    __tablename__ = "batches"
    
    id = Column(Integer, primary_key=True, index=True)
    collector_id = Column(Integer, ForeignKey("collectors.id"))
    material_type = Column(String)  # PET, HDPE, Aluminium
    weight = Column(Float)
    status = Column(String, default="registered")  # registered, transferred, confirmed
    qr_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    collector = relationship("Collector", back_populates="batches")
    transfers = relationship("Transfer", back_populates="batch")

class Hotspot(Base):
    __tablename__ = "hotspots"
    
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    report_count = Column(Integer, default=0)
    last_report = Column(DateTime, nullable=True)
    urgency_score = Column(Float, default=0.0)
    
    reports = relationship("HotspotReport", back_populates="hotspot")

class HotspotReport(Base):
    __tablename__ = "hotspot_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    hotspot_id = Column(Integer, ForeignKey("hotspots.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    report_type = Column(String)  # overflow, illegal_dump, missed_pickup
    created_at = Column(DateTime, default=datetime.utcnow)
    
    hotspot = relationship("Hotspot", back_populates="reports")
    reporter = relationship("User", back_populates="reports")

class Transfer(Base):
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    transfer_date = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
    
    batch = relationship("Batch", back_populates="transfers")

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    truck_id = Column(String)
    estimated_time = Column(Integer)  # minutes
    status = Column(String, default="planned")  # planned, in_progress, completed
    hotspots_visited = Column(Integer, default=0)

