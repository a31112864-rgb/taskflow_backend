from pydantic import BaseModel

class Users(BaseModel):
    phone_no: int

class Tasks(BaseModel):
    user_id: int
    data: str