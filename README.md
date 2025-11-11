# File Sharing API (Postgres)

This project implements a **file sharing REST API** built using **FastAPI** and **PostgreSQL**.  
It supports uploading, listing, and downloading files, with file data stored locally and metadata stored in a PostgreSQL database.  
The project enforces a **20MB upload limit**, provides structured JSON responses, and runs easily via **Docker Compose** or locally using a Python virtual environment.

---

## Endpoints Overview

- `POST /upload` → Upload a file (≤20MB). Returns `{id, name, size, uploaded_at}`  
- `GET /files` → List all uploaded file metadata  
- `GET /files/{id}` → Download a specific file by ID  
- `GET /health` → Check API and database connection status  



Files are stored on disk under the `uploads/` directory, and metadata is persisted in **PostgreSQL**.

---

## Run with Docker (Postgres + FastAPI)

This is the easiest way to run the application.

```bash
# Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# Copy environment variables
cp .env.example .env

# Build and start containers
docker compose up --build

## To  view the endpoints
- `http://127.0.0.1:8000/ui` → Upload, list, and download files interactively  
- `http://127.0.0.1:8000/docs` → Explore and test all endpoints directly  