from pydantic import BaseModel, Field
from datetime import datetime


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=0, max_length=700)
    conclued: bool = Field(default=False)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    conclued: bool | None = None


class TaskResponse(TaskBase):
    id: int

    # faz com que o pydantic leia objetos Python
    class Config:
        from_attributes = True


class CreateTaskResponse(TaskResponse):
    created_at: datetime


class UpdateTaskResponse(TaskResponse):
    updated_at: datetime
