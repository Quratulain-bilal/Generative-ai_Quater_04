# 🧩 Task Management System using FastAPI

# -----------------------------
# 📦 IMPORTS
# -----------------------------

from fastapi import FastAPI, HTTPException  # FastAPI framework aur error handling
from pydantic import BaseModel, EmailStr, constr, validator  # Data validation tools
from datetime import date  # For handling task due dates
from typing import Optional, List  # For optional fields and lists

# -------------------------------
# 🚀 INITIALIZATION
# -------------------------------

app = FastAPI()  # Create an instance of FastAPI

# -------------------------------
# 🗃️ IN-MEMORY DATABASE (Temporary Storage)
# -------------------------------

user_db = {}  # Dictionary to store users
task_db = {}  # Dictionary to store tasks

next_user_id = 1  # Auto-increment ID for new users
next_task_id = 1  # Auto-increment ID for new tasks

# -------------------------------
# 📌 DATA MODELS
# -------------------------------

# 👤 USER MODELS

class UserCreate(BaseModel):
    """
    Model used when creating a new user.
    - Username must be between 3 and 20 characters.
    - Email must be valid format.
    """
    username: constr(min_length=3, max_length=20)  # Constrained string
    email: EmailStr  # Valid email address


class UserInfo(BaseModel):
    """
    Model used to return user info after creation or lookup.
    """
    id: int
    username: str
    email: EmailStr


# ✅ TASK MODELS

class TaskInput(BaseModel):
    """
    Model used to receive input when adding a new task.
    - Title is required.
    - Description is optional.
    - Due date must be today or in the future.
    - Must assign to a valid user ID.
    """
    title: str
    description: Optional[str] = None  # ✅ Corrected: Using square brackets [str]
    due_date: date
    user_id: int

    @validator("due_date")
    def future_due_date(cls, value):
        if value < date.today():
            raise ValueError("Due date can't be in the past.")
        return value


class TaskDetails(BaseModel):
    """
    Model used to return full task details including status and ID.
    - Includes same due date validation.
    """
    id: int
    title: str
    description: Optional[str] = None
    due_date: date
    status: str
    user_id: int

    @validator("due_date")
    def check_due_date(cls, value):
        if value < date.today():
            raise ValueError("Due date must be today or later.")
        return value


class TaskStatusUpdate(BaseModel):
    """
    Model used to update task status.
    - Only allows specific values: pending, in_progress, completed.
    """
    status: str

    @validator("status")
    def validate_status(cls, val):
        valid_statuses = ["pending", "in_progress", "completed"]
        if val not in valid_statuses:
            raise ValueError(f"Invalid status. Choose from: {', '.join(valid_statuses)}")
        return val


# -------------------------------
# 👤 USER ENDPOINTS
# -------------------------------

@app.post("/users/", response_model=UserInfo)
def register_user(payload: UserCreate):
    """
    Creates a new user with auto-assigned ID.
    Adds user to in-memory database.
    Returns created user info.
    """
    global next_user_id
    user_info = payload.dict()
    user_info["id"] = next_user_id
    user_db[next_user_id] = user_info
    next_user_id += 1
    return user_info


@app.get("/users/{user_id}", response_model=UserInfo)
def fetch_user(user_id: int):
    """
    Fetches a user by their ID.
    Raises 404 error if user does not exist.
    """
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User does not exist")
    return user_db[user_id]


# -------------------------------
# ✅ TASK ENDPOINTS
# -------------------------------

@app.post("/tasks/", response_model=TaskDetails)
def add_task(payload: TaskInput):
    """
    Adds a new task to a valid user.
    Sets default status to 'pending'.
    Raises 404 if user doesn't exist.
    Returns added task.
    """
    global next_task_id
    if payload.user_id not in user_db:
        raise HTTPException(status_code=404, detail="No user with this ID")
    
    task_info = payload.dict()
    task_info["id"] = next_task_id
    task_info["status"] = "pending"
    task_db[next_task_id] = task_info
    next_task_id += 1
    return task_info


@app.get("/tasks/{task_id}", response_model=TaskDetails)
def fetch_task(task_id: int):
    """
    Fetches a task by its ID.
    Raises 404 if task does not exist.
    """
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_db[task_id]


@app.put("/tasks/{task_id}", response_model=TaskDetails)
def update_task(task_id: int, payload: TaskStatusUpdate):
    """
    Updates the status of an existing task.
    Validates new status before updating.
    Raises 404 if task does not exist.
    """
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    task_db[task_id]["status"] = payload.status
    return task_db[task_id]


@app.get("/users/{user_id}/tasks", response_model=List[TaskDetails])
def get_tasks_for_user(user_id: int):
    """
    Returns all tasks assigned to a particular user.
    Raises 404 if user does not exist.
    """
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return [task for task in task_db.values() if task["user_id"] == user_id]
