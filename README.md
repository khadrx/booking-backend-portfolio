# Booking Backend – نظام حجز مواعيد (API)

FastAPI + PostgreSQL + SQLAlchemy

### المميزات
- CRUD للحجوزات
- endpoint للأوقات المتاحة ديناميكيًا (يمنع الحجز المكرر)
- CORS مفتوح للـfrontend
- PostgreSQL connection

### Tech Stack
- FastAPI
- SQLAlchemy
- Pydantic v2
- PostgreSQL

### Run locally
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
uvicorn main:app --reload

Docs: http://localhost:8000/docs

### Frontend repo
https://github.com/khadrDev/booking-frontend-portfolio