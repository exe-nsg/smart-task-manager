# ── Start with Python 3.12 base image ──
# This is like a clean computer with Python already installed
FROM python:3.12-slim

# ── Set working directory inside container ──
# All commands will run from this folder
WORKDIR /app

# ── Copy requirements first ──
# We copy this before the code so Docker caches packages
# This makes rebuilding faster
COPY backend/requirements.txt .

# ── Install all Python packages ──
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy the entire project ──
COPY . .

# ── Tell Docker which port this app uses ──
EXPOSE 8000

# ── Command to start the server ──
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]