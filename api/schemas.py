from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID

class SaintResponse(BaseModel):
    """
    Pydantic schema defining how Saint data is formatted as JSON in the API response.
    """
    id: UUID
    official_name: str
    current_status: str
    gender: Optional[str] = None
    feast_day: Optional[int] = None
    feast_month: Optional[int] = None
    birth_date: Optional[date] = None
    short_bio: Optional[str] = None

    class Config:
        from_attributes = True

class PopeResponse(BaseModel):
    """
    Pydantic schema for Pope data, supporting historical date modifiers.
    """
    id: UUID
    succession_number: int
    papal_name: str
    baptism_name: Optional[str] = None
    religious_order: Optional[str] = None
    
    pontificate_start: Optional[date] = None
    start_date_modifier: Optional[str] = None
    pontificate_end: Optional[date] = None
    end_date_modifier: Optional[str] = None

    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    episcopal_motto: Optional[str] = None
    
    cardinals_created: Optional[int] = 0
    documents_issued: Optional[int] = 0
    saints_proclaimed: Optional[int] = 0
    blesseds_proclaimed: Optional[int] = 0

    ordained_priest_date: Optional[date] = None
    consecrated_bishop_date: Optional[date] = None
    created_cardinal_date: Optional[date] = None
    elected_pontiff_date: Optional[date] = None
    death_date: Optional[date] = None
    death_place: Optional[str] = None
    beatified_date: Optional[date] = None
    canonised_date: Optional[date] = None
    
    feast_day: Optional[str] = None
    buried_at: Optional[str] = None

    class Config:
        from_attributes = True