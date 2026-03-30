from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .models import Task
from .schemas import TaskCreate, TaskOut, TaskUpdate
from .models import Notification
from .schemas import NotificationOut
from .models import Task
from .schemas import AssignTask
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base, SessionLocal
from .models import User, Project
from .schemas import UserCreate, ProjectCreate, ProjectOut, ProjectUpdate
from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}


# ---------------- REGISTER ----------------
@app.post("/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered"}


# ---------------- LOGIN ----------------
@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ---------------- AUTH ----------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


# ---------------- PROFILE ----------------
@app.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}


# ---------------- CREATE PROJECT ----------------
@app.post("/projects", response_model=ProjectOut)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_project = Project(
        project_name=project.project_name,
        description=project.description,
        owner_id=current_user["user_id"]
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# ---------------- GET PROJECTS ----------------
@app.get("/projects", response_model=list[ProjectOut])
def get_projects(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Project).filter(
        Project.owner_id == current_user["user_id"]
    ).all()


# ---------------- UPDATE PROJECT ----------------
@app.put("/projects/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user["user_id"]
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.project_name = data.project_name
    project.description = data.description

    db.commit()
    db.refresh(project)

    return project


# ---------------- DELETE PROJECT ----------------
@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user["user_id"]
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Deleted successfully"}
import traceback   # 👈 add at top

@app.post("/projects/{project_id}/tasks", response_model=TaskOut)
def create_task(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        print("DEBUG START 🚀")

        # Check project
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.owner_id == current_user["user_id"]
        ).first()

        print("PROJECT:", project)

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Create task
        new_task = Task(
            title=task.title,
            description=task.description,
            project_id=project_id,
            status="pending",
            assigned_to=None
        )

        print("TASK CREATED:", new_task)

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        print("TASK SAVED ✅")

        return new_task

    except Exception as e:
        print("ERROR ❌")
        print(traceback.format_exc())   # 👈 THIS SHOWS REAL ERROR
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/projects/{project_id}/tasks", response_model=list[TaskOut])
def get_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Task).filter(Task.project_id == project_id).all()
@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status

    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user["user_id"]
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}
def create_notification(db, user_id, message):
    notif = Notification(
        user_id=user_id,
        message=message
    )
    db.add(notif)
    db.commit()

@app.get("/notifications", response_model=list[NotificationOut])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Notification).filter(
        Notification.user_id == current_user["user_id"]
    ).all()
@app.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    # Total tasks
    total_tasks = db.query(Task).join(Project).filter(
        Project.owner_id == user_id
    ).count()

    # Completed tasks
    completed_tasks = db.query(Task).join(Project).filter(
        Project.owner_id == user_id,
        Task.status == "completed"
    ).count()

    # Pending tasks
    pending_tasks = db.query(Task).join(Project).filter(
        Project.owner_id == user_id,
        Task.status == "pending"
    ).count()

    # Tasks per project
    projects = db.query(Project).filter(Project.owner_id == user_id).all()

    tasks_per_project = []
    for project in projects:
        count = db.query(Task).filter(Task.project_id == project.id).count()
        tasks_per_project.append({
            "project_name": project.project_name,
            "task_count": count
        })

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "tasks_per_project": tasks_per_project
    }
from fastapi import HTTPException

@app.post("/tasks/{task_id}/assign")
def assign_task(
    task_id: int,
    data: AssignTask,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Assign user
    task.assigned_to = data.user_id

    # Create notification
    notification = Notification(
        message=f"You have been assigned task: {task.title}",
        user_id=data.user_id
    )

    db.add(notification)
    db.commit()

    return {"message": "Task assigned successfully"}

@app.get("/tasks/assigned", response_model=list[TaskOut])
def get_assigned_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tasks = db.query(Task).filter(
        Task.assigned_to == current_user["user_id"]
    ).all()

    return tasks
    