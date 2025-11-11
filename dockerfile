
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Setting the working directory inside the container
WORKDIR /app

# Copying requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying application and UI source code
COPY app app
COPY ui ui
COPY .env.example .

# Creating uploads directory inside the container
RUN mkdir -p uploads

# Expose FastAPI port
EXPOSE 8000

# Running the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
