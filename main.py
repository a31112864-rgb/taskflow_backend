import os
from fastapi import FastAPI, Depends, Response, status
from sqlalchemy.orm import Session
from database_modals import Base, User, Task
from database import engine, session
from modals import Tasks, Users

app = FastAPI()

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
        httponly=True, 
        secure=True, 
        samesite="lax"
    )
    
    return {"message": "User registered successfully", "id": db_user.id}
