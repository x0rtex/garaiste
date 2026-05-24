from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), onupdate=lambda: datetime.now(timezone.UTC), nullable=False)

    vehicles = relationship("Vehicle", back_populates="user", cascade="all, delete-orphan")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    registration = Column(String, unique=True, index=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    fuel_type = Column(String)
    image_url = Column(String)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), onupdate=lambda: datetime.now(timezone.UTC), nullable=False)

    user = relationship("User", back_populates="vehicles")
    odometer_records = relationship("OdometerRecord", back_populates="vehicle", cascade="all, delete-orphan")
    tax_records = relationship("TaxRecord", back_populates="vehicle", cascade="all, delete-orphan")
    nct_records = relationship("NctRecord", back_populates="vehicle", cascade="all, delete-orphan")
    service_records = relationship("ServiceRecord", back_populates="vehicle", cascade="all, delete-orphan")


class OdometerRecord(Base):
    __tablename__ = "odometer_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    value = Column(Integer)
    notes = Column(Text)
    date = Column(DateTime)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), onupdate=lambda: datetime.now(timezone.UTC), nullable=False)

    vehicle = relationship("Vehicle", back_populates="odometer_records")


class TaxRecord(Base):
    __tablename__ = "tax_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    amount_cents = Column(Integer)
    notes = Column(Text)
    date = Column(DateTime)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), onupdate=lambda: datetime.now(timezone.UTC), nullable=False)

    vehicle = relationship("Vehicle", back_populates="tax_records")


class NctRecord(Base):
    __tablename__ = "nct_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    amount_cents = Column(Integer)
    passed = Column(Boolean)
    retest = Column(Boolean)
    notes = Column(Text)
    date = Column(DateTime)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), onupdate=lambda: datetime.now(timezone.UTC), nullable=False)

    vehicle = relationship("Vehicle", back_populates="nct_records")


class ServiceRecord(Base):
    __tablename__ = "service_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    amount_cents = Column(Integer)
    notes = Column(Text)
    date = Column(DateTime)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), onupdate=lambda: datetime.now(timezone.UTC), nullable=False)

    vehicle = relationship("Vehicle", back_populates="service_records")
