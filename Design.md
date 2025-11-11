
# Design Document — File Sharing API (FastAPI + PostgreSQL)

This document describes the complete design and architecture of the **File Sharing API** built using **FastAPI** and **PostgreSQL**, containerized with **Docker Compose**. It explains how the system works, how the APIs are designed, and how the database, file storage, backend, frontend, and Docker components interact together. This serves as the overall design reference for the project.

---

## Overview

The **File Sharing API** enables users to upload, list, and download files through RESTful endpoints. Uploaded files are stored locally on disk, while metadata (filename, size, timestamp, and file path) is stored in a PostgreSQL database. The system enforces a **20MB upload limit**, provides clear JSON responses, and offers a health check endpoint to verify database connectivity.  
The project runs locally or through **Docker Compose**, which orchestrates the FastAPI application and PostgreSQL database. A lightweight **frontend UI** served from `/ui` allows easy interaction and testing.

---

## System Architecture

The system follows a **three-layer design**:
1. **Frontend** — A simple web interface (HTML, JS) that allows users to upload, list, and download files.
2. **Backend** — A FastAPI application managing business logic, file I/O, and database operations.
3. **Database** — A PostgreSQL instance storing metadata for uploaded files.

---

## Database Design

The PostgreSQL database manages all metadata related to uploaded files in a single table called **`files`**.  
The schema is optimized for quick lookups and sorting.

**Table: files**

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Unique file identifier |
| name | VARCHAR | Original file name |
| path | VARCHAR | Local file path |
| size | BIGINT | File size in bytes |
| uploaded_at | BIGINT | UNIX timestamp when the file was uploaded |

Each record is uniquely identified by a UUID. Indexes are placed on `id` and `uploaded_at` for efficient retrieval.  
Database connection parameters are loaded from `.env`, and **SQLAlchemy ORM** is used for interactions, ensuring type safety and clean query abstractions.

---

## File Storage Design

All uploaded files are saved under an **`uploads/`** directory in the FastAPI container.  
Each file name is replaced with a unique UUID to avoid duplication, and the original name and path are recorded in PostgreSQL.


The uploads folder is mounted as a **persistent Docker volume**, ensuring files remain available even after container restarts or rebuilds.

---

## Backend Design

The backend uses **FastAPI**, a high-performance Python web framework for building RESTful APIs.

**Structure Overview:**
- **main.py** — Defines routes, endpoints, and serves the frontend.
- **models.py** — SQLAlchemy model for the `files` table.
- **schemas.py** — Pydantic models for input/output validation.
- **db.py** — Handles database connections and session management.
- **config.py** — Loads environment variables for configuration.
- **Dockerfile** — Defines container build for FastAPI service.

The backend provides:
- **Swagger UI** for API documentation at `/docs`
- **Frontend UI** for user interaction at `/ui`
- **Structured JSON responses** and error handling.

---

## Frontend Design

The **frontend** for this is a lightweight HTML and JavaScript interface enabling users to:
- Upload files (via `POST /upload`)
- View all uploaded files (via `GET /files`)
- Download specific files (via `GET /files/{id}`)

It uses **Fetch API** for asynchronous operations and dynamically updates the list of files after each upload.  
The interface is automatically served from FastAPI at [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui) and includes clear buttons and progress indicators for better usability.

---

## Docker Design

The entire project is **containerized** using Docker Compose for simple setup and teardown.  
Two containers are defined:

- **FastAPI App Container** — Runs the backend and serves the frontend.
- **PostgreSQL Container** — Stores file metadata.

**docker-compose.yml** includes:
- Environment variables
- Network configuration
- Volume mounting for persistence
- Automatic dependency linking between `app` and `db`.

**Commands:**
```bash
# Build and start services
docker compose up --build

# Access
Frontend UI → http://127.0.0.1:8000/ui
Swagger Docs → http://127.0.0.1:8000/docs

# Stop and remove containers
docker compose down -v
