from pydantic import BaseModel, Field
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskOut(BaseModel):
    id: int
    title: str
    status: str
    completed_at: datetime | None

    class Config:
        from_attributes = True
