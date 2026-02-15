from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String)
    date = Column(DateTime)
    time_slot = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)