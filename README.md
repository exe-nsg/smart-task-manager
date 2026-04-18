# Smart Task Manager

A full-stack AI-powered task manager where users add tasks and Groq AI automatically prioritizes them, estimates completion time, suggests optimal work order, and provides motivational insights.

---

## Live Demo

Run locally with one command:

```bash
git clone git@github.com:exe-nsg/smart-task-manager.git
cd smart-task-manager
echo "GROQ_API_KEY=your_key_here" > .env
docker-compose up
```

Visit → **http://localhost:3000**

---

## ✨ Features

- Add tasks with title, description, and priority
- Groq AI analyzes every task instantly
- Priority score (0-100) with animated ring
- Time estimation per task
- Personalized motivation message
- 3 actionable steps per task
- Due date and time picker
- Mark tasks complete
- Delete tasks
- Stats dashboard — Total, Done, Pending

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + TailwindCSS |
| Backend | Python + FastAPI |
| AI | Groq AI (llama-3.3-70b) |
| Database | SQLite + SQLAlchemy |
| Containers | Docker + Docker Compose |
| CI/CD | Jenkins |
| Testing | pytest |

---

## Project Structure
smart-task-manager/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── ai_service.py
│   │   ├── database.py
│   │   └── models.py
│   ├── tests/
│   │   └── test_main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── App.css
│   └── Dockerfile
├── jenkins/
│   └── Jenkinsfile
├── docker-compose.yml
└── .env.example

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home |
| GET | /health | Health check |
| GET | /tasks | Get all tasks |
| POST | /tasks | Create task + AI analysis |
| PUT | /tasks/{id}/complete | Mark complete |
| DELETE | /tasks/{id} | Delete task |

---

## Setup

### Run with Docker
```bash
git clone git@github.com:exe-nsg/smart-task-manager.git
cd smart-task-manager
echo "GROQ_API_KEY=your_key_here" > .env
docker-compose up
```

### Run locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000

cd frontend
npm install
npm start
```

---

## Tests

```bash
pytest backend/tests/ -v
```

---

## Author

**Naga Sai Ganesh Pasumarthi**
- GitHub: [@exe-nsg](https://github.com/exe-nsg)
- University: Texas State University
- Program: MS Data Analytics and Information Systems
EOF