import os
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi import FastAPI, Depends, Response, status, Cookie
from sqlalchemy.orm import Session
from database_modals import Base, User, Task
from database import engine, session
from modals import Tasks, Users

origns = [
    "http://localhost:5500"
    "https://a31112864-rgb.github.io/TaskFlow/"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origns,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

IS_PROD = os.getenv("WEB_ENV") == "production"

Base.metadata.create_all(engine)

def get_db():
    db = session()

    try:
        yield db
    finally:
        db.close()

# Make sure to import your SQLAlchemy model at the top of your file
# from models import UserModel 

@app.post("/register")
def register_user(user: Users, response: Response, db: Session = Depends(get_db)):

    #  Change 'user' to your SQLAlchemy database model class (e.g., UserModel)
    db_user = User(
        phone_no=user.phone_no
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Works perfectly now!
    
    # Convert it to a string, because cookies can only store string values
    response.set_cookie(
        key="user_id", 
        value=str(db_user.id), 
        expires=200000000,
        httponly=True, 
        secure=True, 
        samesite="lax"
    )
    
    return {"message": "User registered successfully", "id": db_user.id}

@app.get("/tasks")
def show_tasks(user_id: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks

@app.post("/task")
def create_task(
    task: Tasks,
    user_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db)):
    db_task = Task(
        user_id = task.user_id,
        data = task.data
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)


    return f"task added successfully task_id = {db_task.id}"

@app.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    db.commit()

    return "task deleted successfully"




