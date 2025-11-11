# Design Document — File Sharing API (FastAPI + PostgreSQL)

This document describes the design and architecture of the **File Sharing API** built with **FastAPI** and **PostgreSQL**, containerized using **Docker Compose**.  
It explains how the system works, how each component interacts, and how the backend, frontend, database, and Docker setup come together to form a reliable file-sharing service.

---

## Overview

The **File Sharing API** is a lightweight application that allows users to upload, list, and download files through RESTful endpoints.  
Uploaded files are stored locally on disk, while metadata — such as filename, size, upload time, and file path — is stored in a PostgreSQL database.  

The API enforces a **20 MB upload limit**, provides clear JSON responses, and exposes a **health-check endpoint** to verify service and database availability.  
Everything runs seamlessly either on your local machine or inside Docker containers managed through **Docker Compose**.  
A small **frontend UI** served from `/ui` allows quick testing and interaction with the service.

---

## System Architecture

The overall architecture follows a clean three-layer design:

1. **Frontend Layer** – A simple HTML + JavaScript interface that communicates with the API to upload, view, and download files.
2. **Backend Layer** – A FastAPI application that implements the business logic, file handling, and database interactions.
3. **Database Layer** – A PostgreSQL instance that stores all file metadata securely and efficiently.

All components are orchestrated through Docker Compose, which handles networking, volume persistence, and environment setup automatically.

---

## Database Design

The database uses a single table, `files`, to store metadata about every uploaded file.  
The schema is intentionally simple for fast lookup and easy scalability.

| Column | Type | Description |
|:-------|:------|:------------|
| **id** | UUID | Unique file identifier |
| **name** | VARCHAR | Original file name |
| **path** | VARCHAR | Local file path on disk |
| **size** | BIGINT | File size in bytes |
| **uploaded_at** | BIGINT | UNIX timestamp of upload time |

Each file is uniquely identified by its UUID. Indexes are applied on `id` and `uploaded_at` for faster queries.  
Database credentials and connection parameters are defined in `.env`, and all operations are handled via **SQLAlchemy ORM** for safety and maintainability.

---

## File Storage Design

Uploaded files are stored in the `uploads/` directory inside the FastAPI container.  
To avoid filename conflicts, every uploaded file is renamed using a generated UUID, while its original name and path are stored in the database.  

This directory is mounted as a **Docker volume**, ensuring that uploaded files remain available even if the container is restarted or rebuilt.



---

## Backend Design

The backend is built with **FastAPI**, chosen for its speed, clean syntax, and automatic OpenAPI documentation.

**Key modules:**
- `main.py` — Entry point defining all endpoints and serving the frontend.
- `models.py` — SQLAlchemy model for the `files` table.
- `schemas.py` — Pydantic models for validating request and response data.
- `db.py` — Handles the database connection and session management.
- `config.py` — Loads environment variables from `.env`.
- `Dockerfile` — Defines how the FastAPI app image is built.

The backend provides two built-in interfaces:
- **Swagger UI** at `/docs` for testing all API routes.
- **Frontend UI** at `/ui` for uploading, listing, and downloading files directly in the browser.

---

## Frontend Design

The frontend is a small, static web page made with HTML and vanilla JavaScript.  
It uses the Fetch API to interact with the backend endpoints:
- `POST /upload` for uploading files,
- `GET /files` for listing all uploaded files,
- `GET /files/{id}` for downloading specific files.

The interface automatically refreshes the list after every upload and displays live responses from the API.  
It is served directly from FastAPI at [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui).

---

## Docker Design

The entire setup runs through Docker Compose, which defines two containers:

1. **FastAPI App Container** — Runs the backend and serves the UI.
2. **PostgreSQL Container** — Hosts the database for file metadata.

**docker-compose.yml** handles:
- Service networking between app and database,
- Environment variable injection,
- Volume mounting for persistent storage.

Common commands:
```bash
# Build and start containers
docker compose up --build

# Stop and remove containers
docker compose down -v
