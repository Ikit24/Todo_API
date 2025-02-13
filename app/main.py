from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
from typing import Optional, Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "secret123"
    
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos/")
def read_todos(
    current_user: str = Depends(get_current_user),  # Add this line
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    todos = db.query(models.Todo).offset(skip).limit(limit).all()
    return todos
@app.post("/todos/")
def create_todo(title: str, description: str = None, db: Session = Depends(get_db)):
    todo = models.Todo(title=title, description=description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.get("/todos/{todo_id}")
def read_todos(todo_id: int, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todos is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos

@app.put("/todos/{todo_id}")
def update_todos(
    todo_id: int, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    completed: Optional[bool] = None, 
    db: Session = Depends(get_db)
):
    todos = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todos is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if title is not None:
        todos.title = title
    if description is not None:
        todos.description = description
    if completed is not None:
        todos.completed = completed
    
    db.commit()
    db.refresh(todos)
    return todos

@app.delete("/todos/{todo_id}")
def delete_todos(todo_id: int, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todos is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todos)
    db.commit()
    return {"message": "Todo deleted successfully"}