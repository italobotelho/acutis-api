import uuid
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from api.database import Base

class Saint(Base):
    """SQLAlchemy model for the 'saints' table."""
    __tablename__ = "saints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    official_name = Column(String(150), nullable=False)
    baptism_name = Column(String(150))
    gender = Column(String(1))
    current_status = Column(String(50), nullable=False)
    vocation = Column(String(100))
    civil_occupation = Column(String(100))
    feast_day = Column(Integer)
    feast_month = Column(Integer)
    birth_date = Column(Date)
    birth_place = Column(String(100))
    region_of_activity = Column(String(150))
    death_date = Column(Date)
    death_place = Column(String(100))
    is_doctor_of_church = Column(Boolean, default=False)
    profile_image_url = Column(String(255))
    short_bio = Column(String(500))
    full_bio = Column(Text)

class Pope(Base):
    """SQLAlchemy model for the 'popes' table."""
    __tablename__ = "popes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    succession_number = Column(Integer, nullable=False)
    papal_name = Column(String(100), nullable=False)
    baptism_name = Column(String(150), nullable=False)
    nationality = Column(String(100), nullable=False)
    religious_order = Column(String(100))
    papal_motto = Column(String(255))
    pontificate_start = Column(Date, nullable=False)
    pontificate_end = Column(Date)
    end_reason = Column(String(50))
    saint_id = Column(UUID(as_uuid=True), ForeignKey('saints.id'))