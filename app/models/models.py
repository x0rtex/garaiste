from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow():
    return datetime.now(timezone.UTC)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    garages: Mapped[list[Garage]] = relationship("Garage", back_populates="user")
    garage_collaborations: Mapped[list[GarageCollaborator]] = relationship("GarageCollaborator", back_populates="user")
    vehicle_collaborations: Mapped[list[VehicleCollaborator]] = relationship("VehicleCollaborator", back_populates="user")


class Garage(Base):
    __tablename__ = "garages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    name: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    owner: Mapped[User] = relationship("User", back_populates="garages")
    vehicles: Mapped[list[Vehicle]] = relationship("Vehicle", back_populates="garage", cascade="all, delete-orphan")
    collaborators: Mapped[list[GarageCollaborator]] = relationship("GarageCollaborator", back_populates="garage")


class GarageCollaborator(Base):
    __tablename__ = "garage_collaborators"

    garage_id: Mapped[int] = mapped_column(ForeignKey("garages.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    role: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    garage: Mapped[Garage] = relationship("Garage", back_populates="collaborators")
    user: Mapped[User] = relationship("User", back_populates="garage_collaborations")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    garage_id: Mapped[int] = mapped_column(ForeignKey("garages.id"))

    registration: Mapped[str] = mapped_column(String(12), unique=True, index=True)
    make: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(SmallInteger)
    fuel_type: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    garage: Mapped[Garage] = relationship("Garage", back_populates="vehicles")
    collaborators: Mapped[list[VehicleCollaborator]] = relationship("VehicleCollaborator", back_populates="vehicle")
    odometer_records: Mapped[list[OdometerRecord]] = relationship("OdometerRecord", back_populates="vehicle", cascade="all, delete-orphan")
    service_records: Mapped[list[ServiceRecord]] = relationship("ServiceRecord", back_populates="vehicle", cascade="all, delete-orphan")


class VehicleCollaborator(Base):
    __tablename__ = "vehicle_collaborators"

    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    role: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    vehicle: Mapped[Vehicle] = relationship("Vehicle", back_populates="collaborators")
    user: Mapped[User] = relationship("User", back_populates="vehicle_collaborations")


class OdometerRecord(Base):
    __tablename__ = "odometer_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))

    value_km: Mapped[int]
    notes: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    vehicle: Mapped[Vehicle] = relationship("Vehicle", back_populates="odometer_records")


class ServiceRecord(Base):
    __tablename__ = "service_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))

    amount_cents: Mapped[int]
    notes: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    vehicle: Mapped[Vehicle] = relationship("Vehicle", back_populates="service_records")
