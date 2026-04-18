# models.py — Database Models
# This file defines what a Task looks like
# in the database

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from backend.app.database import Base

# Task Model
# This creates a "tasks" table in SQLite
# with these exact columns

class Task(Base):

    # Name of the table in database
    __tablename__ = "tasks"

    # Unique ID — auto generated
    # primary_key=True means this is the unique identifier
    # index=True makes searching faster
    id = Column(Integer, primary_key=True, index=True)

    # Task title — required
    # index=True makes searching by title faster
    title = Column(String, index=True)

    # Task description — optional
    # nullable=True means it can be empty
    description = Column(String, nullable=True, default="")

    # Priority level — high, medium, low
    # defaults to "medium"
    priority = Column(String, default="medium")

    # Is task done?
    # False by default — new tasks are not completed
    completed = Column(Boolean, default=False)

    # AI analysis from Groq
    # Empty now — filled on Day 4
    ai_analysis = Column(String, nullable=True)

    # When the task was created
    # server_default=func.now() means
    # database sets this automatically
    due_date = Column(DateTime, nullable=True)
    user_email = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    user_email = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())