from pydantic import BaseModel
from typing import Optional

# ---------------- USER ----------------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# ---------------- PROJECT ----------------
class ProjectCreate(BaseModel):
    project_name: str
    description: str


class ProjectUpdate(BaseModel):
    project_name: str
    description: str


class ProjectOut(BaseModel):
    id: int
    project_name: str
    description: str
    owner_id: int

    class Config:
        from_attributes = True


# ---------------- TASK ----------------
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    project_id: int
    assigned_to: int | None

    class Config:
        from_attributes = True 

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    project_id: int
    assigned_to: int | None

    class Config:
        from_attributes = True


# ---------------- ASSIGN TASK ----------------
class AssignTask(BaseModel):
    user_id: int


# ---------------- NOTIFICATION ----------------
class NotificationOut(BaseModel):
    id: int
    message: str
    user_id: int

    class Config:
        from_attributes = True