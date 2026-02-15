from pydantic import BaseModel, field_serializer, ConfigDict
from datetime import datetime

class BookingCreate(BaseModel):
    name: str
    email: str
    phone: str
    date: str
    time_slot: str

class BookingOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    date: datetime
    time_slot: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('date', 'created_at')
    def serialize_datetime(self, dt: datetime, _info):
        return dt.isoformat()