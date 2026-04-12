from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Smart Task Manager",
    description="AI-powered task manager using Gemini AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "medium"

tasks = []
task_counter = 1

@app.get("/")
def home():
    return {
        "message": "Smart Task Manager API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Server is running perfectly",
        "total_tasks": len(tasks)
    }

@app.get("/tasks")
def get_tasks():
    return {
        "status": "success",
        "total": len(tasks),
        "tasks": tasks
    }

@app.post("/tasks")
def create_task(task: Task):
    global task_counter

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    new_task = {
        "id": task_counter,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "completed": False,
        "ai_analysis": None
    }

    tasks.append(new_task)
    task_counter += 1

    return {
        "status": "success",
        "message": "Task created successfully",
        "task": new_task
    }

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks

    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found"
        )

    tasks = [t for t in tasks if t["id"] != task_id]

    return {
        "status": "success",
        "message": f"Task {task_id} deleted successfully"
    }