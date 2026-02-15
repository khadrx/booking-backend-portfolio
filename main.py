from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel, field_serializer, ConfigDict

from database import engine, SessionLocal, Base
from models import Booking
from schemas import BookingCreate, BookingOut

app = FastAPI(title="Booking API - PostgreSQL")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

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

    all_slots = [
        "09:00-10:00", "10:00-11:00", "11:00-12:00",
        "14:00-15:00", "15:00-16:00", "16:00-17:00"
    ]

    booked = db.query(Booking.time_slot).filter(
        Booking.date == target_date
    ).all()

    booked_slots = {b[0] for b in booked}
    available = [s for s in all_slots if s not in booked_slots]

    return {"date": date, "available_slots": available or []}