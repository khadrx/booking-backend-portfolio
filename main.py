from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, field_serializer, ConfigDict
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Booking API - PostgreSQL")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # غير * لاحقًا
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection - PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model (نفس اللي قبل كده)
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String)
    date = Column(DateTime)
    time_slot = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# Pydantic schemas
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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Booking Backend - PostgreSQL is running"}

@app.post("/bookings/", response_model=BookingOut)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    try:
        booking_date = datetime.strptime(booking.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    db_booking = Booking(
        name=booking.name,
        email=booking.email,
        phone=booking.phone,
        date=booking_date,
        time_slot=booking.time_slot
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.get("/bookings/")
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@app.get("/available-slots/")
def get_available_slots(date: str = Query(...), db: Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(400, "Invalid date format")

    # كل الأوقات الممكنة
    all_slots = [
        "09:00-10:00", "10:00-11:00", "11:00-12:00",
        "14:00-15:00", "15:00-16:00", "16:00-17:00"
    ]

    # جيب الحجوزات في نفس اليوم
    booked = db.query(Booking.time_slot).filter(
        Booking.date == target_date
    ).all()

    booked_slots = {b[0] for b in booked}

    available = [s for s in all_slots if s not in booked_slots]

    return {"date": date, "available_slots": available or []}