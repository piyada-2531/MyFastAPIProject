from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import models
import os
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates

# สร้างตารางในฐานข้อมูล (ถ้ายังไม่มี)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ต้องระบุ directory ให้ชัดเจนเผื่อกรณีรันบน Cloudflare
base_dir = os.path.dirname(os.path.abspath(__file__))
# ตั้งค่า Templates
templates = Jinja2Templates(directory="templates")

# ฟังก์ชันช่วยเปิด-ปิด Database (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 5. API สำหรับดูรายการทั้งหมด
@app.get("/todos")
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

# 6. API สำหรับเพิ่มรายการจากฟอร์ม HTML
@app.post("/add")
def add_todo(title: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    new_item = models.Todo(title=title, description=description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return RedirectResponse(url="/", status_code=303)

# 7. API สำหรับลบรายการ
@app.get("/delete/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

# 8. API สำหรับสลับสถานะเสร็จ/ไม่เสร็จ
@app.get("/toggle/{todo_id}")
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        todo.is_done = not todo.is_done
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # ในตัวอย่างรูปนี้ยังไม่มีการดึงข้อมูล Todo มาโชว์ 
    # เราแค่เรนเดอร์หน้าเปล่าๆ ก่อนได้ครับ
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={}
    )

# เพิ่มโค้ดนี้ลงใน main.py ต่อจากหน้าแรก
@app.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="about.html", 
        context={}
    )

@app.get("/services", response_class=HTMLResponse)
def services_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="services.html", 
        context={}
    )

@app.get("/services", response_class=HTMLResponse)
def services_page(request: Request):
    return templates.TemplateResponse(
        "services.html", 
        {"request": request} # ห้ามลืมบรรทัดนี้เด็ดขาด
    )

@app.get("/links", response_class=HTMLResponse)
def useful_links(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="links.html", 
        context={}
    )

@app.get("/careers", response_class=HTMLResponse)
def careers_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="careers.html", 
        context={}
    )

@app.get("/contact", response_class=HTMLResponse)
def contact_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="contact.html", 
        context={}
    )

from mangum import Mangum
handler = Mangum(app) # นี่คือหัวใจสำคัญที่ทำให้รันบน Cloudflare ได้