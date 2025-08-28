from pydantic import BaseModel,Field
from fastapi import Form, FastAPI,Depends,Request
from typing import Optional,List
from app.schemas.main_schem import RequestModel
from app.models import StatusEnum

class GoalQuery(RequestModel):
    cele: str = Field(...,min_length=1,max_length=100)
    ocena: int = Field(...,ge=1,le=4)
    
class DeleteGoal(RequestModel):
    id: int = Field(...)

class GoalEntrySchema(BaseModel):
    id: int
    cele: str = Field(...,alias="goal")
    status: StatusEnum   # tutaj Enum zostanie zserializowany jako string
    priority: int

    class Config:
        orm_mode = True
        populate_by_name = True  