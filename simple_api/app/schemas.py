from pydantic import BaseModel
from datetime import date

class TaskBase(BaseModel):
    title: str
    description: str
    due_date: date
    status: str

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

    class Config:
        orm_mode = True
