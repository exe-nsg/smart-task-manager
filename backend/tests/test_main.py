# ============================================
# test_main.py — Basic API Tests
# Jenkins runs these automatically
# ============================================

from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Smart Task Manager" in response.json()["message"]

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert "tasks" in response.json()
