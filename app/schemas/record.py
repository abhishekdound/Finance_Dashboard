from pydantic import BaseModel, Field, validator, field_validator
from datetime import datetime
from typing import Optional

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0, description="The amount must be greater than zero")
    type: str
    category: str
    description: Optional[str] = None

    @field_validator('type')
    def validate_type(cls, v):
        if v.lower() not in ['income', 'expense']:
            raise ValueError('Type must be either "income" or "expense"')
        return v.lower()

class RecordCreate(RecordBase):
    pass

class Record(RecordBase):
    id: int
    date: datetime
    owner_id: int

    class Config:
        from_attributes = True
