from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 1. กำหนดที่อยู่ของฐานข้อมูล (ใช้ environment variable หรือ default เป็น SQLite)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./my_database.db")

# 2. สร้าง Engine (ตัวขับเคลื่อนหลัก)
# check_same_thread=False จำเป็นสำหรับ SQLite เท่านั้น
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# 3. สร้าง SessionLocal (เพื่อเอาไว้คุยกับ DB ในแต่ละครั้ง)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. สร้าง Base Class (เพื่อให้โมเดลข้อมูลอื่นๆ มาสืบทอดไปใช้)
Base = declarative_base()
