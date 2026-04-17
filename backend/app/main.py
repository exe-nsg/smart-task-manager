# main.py — FastAPI Server
# Day 3: Connected to Groq AI
# Tasks now get AI-powered analysis

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import json

from backend.app.database import engine, get_db, Base
from backend.app.models import Task
from backend.app.ai_service import analyze_task, get_fallback_analysis

# Create all database tables automatically
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Smart Task Manager",
    description="AI-powered task manager using Groq AI",
    version="3.0.0"
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
        "version": "3.0.0",
        "status": "healthy",
        "database": "SQLite connected",
        "ai": "Groq AI connected"
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
        "database": "connected",
        "ai": "Groq AI ready"
    }

# GET /tasks — get all tasks from database
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()

    task_list = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "completed": task.completed,
            "created_at": str(task.created_at),
            "ai_analysis": json.loads(task.ai_analysis) if task.ai_analysis else None
        }
        task_list.append(task_dict)

    return {
        "status": "success",
        "total": len(task_list),
        "tasks": task_list
    }

# POST /tasks — create task + get AI analysis
@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):

    # Check title is not empty
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    # Step 1 — Save task to database first
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        completed=False,
        ai_analysis=None
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Step 2 — Send to Groq AI for analysis
    # try = attempt to call Groq
    # except = if anything fails use fallback
    try:
        analysis = analyze_task(task.title, task.description)
    except Exception:
        analysis = get_fallback_analysis(task.title)

    # Step 3 — Save AI analysis to database
    new_task.ai_analysis = json.dumps(analysis)
    db.commit()
    db.refresh(new_task)

    # Step 4 — Return task with AI analysis
    return {
        "status": "success",
        "message": "Task created and analyzed by Groq AI",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "priority": new_task.priority,
            "completed": new_task.completed,
            "created_at": str(new_task.created_at),
            "ai_analysis": analysis
        }
    }

# DELETE /tasks/{task_id} — delete a task
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

# PUT /tasks/{task_id}/complete — mark task as complete
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