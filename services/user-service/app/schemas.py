from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional


class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    tc_kimlik: Optional[str] = None
    gender: Optional[str] = None


class ProfileOut(BaseModel):
    id: UUID
    auth_user_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    tc_kimlik: Optional[str] = None
    gender: Optional[str] = None
    model_config = {"from_attributes": True}
