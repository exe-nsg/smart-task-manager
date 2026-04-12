# main.py — FastAPI Server
# Day 3: Connected to SQLite database
# Tasks are now saved permanently

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from backend.app.database import engine, get_db, Base
from backend.app.models import Task

# Create all database tables automatically
# This reads all models and creates tables
# in SQLite if they do not exist yet

Base.metadata.create_all(bind=engine)

# Create FastAPI app

app = FastAPI(
    title="Smart Task Manager",
    description="AI-powered task manager using Gemini AI",
    version="2.0.0"
)


# CORS — allows React frontend to talk to backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model — what data user sends
# when creating a task

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "medium"

# Home endpoint

@app.get("/")
def home():
    return {
        "message": "Smart Task Manager API is running",
        "version": "2.0.0",
        "status": "healthy",
        "database": "SQLite connected"
    }


# Health check endpoint
# Used by Jenkins to verify server is alive

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    total_tasks = db.query(Task).count()
    return {
        "status": "healthy",
        "message": "Server is running perfectly",
        "total_tasks": total_tasks,
        "database": "connected"
    }

# GET /tasks — get all tasks from database
# db.query(Task) = look in tasks table
# .all()         = get every row


@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return {
        "status": "success",
        "total": len(tasks),
        "tasks": tasks
    }


# POST /tasks — create a new task
#
# db.add(new_task)    = prepare to save
# db.commit()         = actually save
# db.refresh(new_task) = get saved data back

@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):

    # Check title is not empty
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    # Create new task object
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        completed=False,
        ai_analysis=None
    )

    # Save to database
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "status": "success",
        "message": "Task created and saved to database",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "priority": new_task.priority,
            "completed": new_task.completed,
            "ai_analysis": new_task.ai_analysis,
            "created_at": str(new_task.created_at)
        }
    }


# DELETE /tasks/{task_id} — delete a task
#
# Find task by id
# If not found → send 404 error
# If found → delete from database

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    # Find the task
    task = db.query(Task).filter(Task.id == task_id).first()

    # If not found
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found"
        )

    # Delete from database
    db.delete(task)
    db.commit()

    return {
        "status": "success",
        "message": f"Task {task_id} deleted from database"
    }


# PUT /tasks/{task_id} — mark task as complete

@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):

    # Find the task
    task = db.query(Task).filter(Task.id == task_id).first()

    # If not found
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found"
        )

    # Mark as completed
    task.completed = True
    db.commit()
    db.refresh(task)

    return {
        "status": "success",
        "message": f"Task {task_id} marked as complete",
        "task": {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
    }