from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
import models
from database import SessionLocal, engine

# สร้างตารางในฐานข้อมูลถ้ายังไม่มี
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

base_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Dependency Injection สำหรับฐานข้อมูล
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos")
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

@app.post("/add")
def add_todo(title: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    new_item = models.Todo(title=title, description=description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/toggle/{todo_id}")
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        todo.is_done = not todo.is_done
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "todos": todos}
    )

@app.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )

@app.get("/services", response_class=HTMLResponse)
def services_page(request: Request):
    return templates.TemplateResponse(
        "services.html",
        {"request": request}
    )

@app.get("/links", response_class=HTMLResponse)
def useful_links(request: Request):
    return templates.TemplateResponse(
        "links.html",
        {"request": request}
    )

@app.get("/careers", response_class=HTMLResponse)
def careers_page(request: Request):
    return templates.TemplateResponse(
        "careers.html",
        {"request": request}
    )

@app.get("/contact", response_class=HTMLResponse)
def contact_page(request: Request):
    return templates.TemplateResponse(
        "contact.html",
        {"request": request}
    )

from mangum import Mangum
on_fetch = Mangum(app)
