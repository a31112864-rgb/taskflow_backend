from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    phone_no = Column(String(20), unique = True, nullable=False)
    items = relationship("Task", back_populates = "owner")
    

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    data = Column(String(100), nullable=False)
    owner = relationship("User", back_populates = "items")
    