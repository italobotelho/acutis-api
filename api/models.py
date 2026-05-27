import uuid
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from api.database import Base

class Saint(Base):
    """SQLAlchemy model for the 'saints' table."""
    __tablename__ = "saints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    official_name = Column(String(150))
    baptism_name = Column(String(150))
    gender = Column(String(1))
    current_status = Column(String(50))
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
    religious_order = Column(String(100))
    pontificate_start = Column(Date)
    start_date_modifier = Column(String(20), default="exact")
    pontificate_end = Column(Date)
    end_date_modifier = Column(String(20), default="exact")
    saint_id = Column(UUID(as_uuid=True), ForeignKey('saints.id'))
    birth_date = Column(Date)
    birth_place = Column(String(255))
    episcopal_motto = Column(String(255))
    cardinals_created = Column(Integer, default=0)
    documents_issued = Column(Integer, default=0)
    saints_proclaimed = Column(Integer, default=0)
    blesseds_proclaimed = Column(Integer, default=0)
    ordained_priest_date = Column(Date)
    consecrated_bishop_date = Column(Date)
    created_cardinal_date = Column(Date)
    elected_pontiff_date = Column(Date)
    installed_pontiff_date = Column(Date)
    death_date = Column(Date)
    death_place = Column(String(255))
    beatified_date = Column(Date)
    canonised_date = Column(Date)
    feast_day = Column(String(50))
    buried_at = Column(String(500))