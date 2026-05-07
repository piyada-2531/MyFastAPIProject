from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Todo(Base):
    __tablename__ = "todos" # ชื่อตารางในฐานข้อมูล

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_done = Column(Boolean, default=False)
