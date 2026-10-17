from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr

class TaskCreate(BaseModel):
    title: StrictStr

class TaskCompletedUpdate(BaseModel):
    completed: StrictBool

class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    completed: bool
