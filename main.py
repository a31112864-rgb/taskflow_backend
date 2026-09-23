from fastapi import FastAPI, Depends, Response
from sqlalchemy.orm import Session
from database_modals import Base
from database import engine

app = FastAPI()

Base.metadata.create_all(engine)