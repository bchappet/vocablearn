# FastAPI Tutorial Project

A web application built with FastAPI featuring group management, quiz functionality, settings, and keyboard handling.

## Features

- Group Management
- Quiz System
- Settings Configuration
- Keyboard Controls
- Static File Serving
- Template Rendering with Jinja2

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Project Structure

- `/static` - Static files (CSS, JS, images)
- `/templates` - Jinja2 HTML templates
- `/routers` - API route modules
- `main.py` - Application entry point
- `database.py` - Database configuration

## API Documentation

Once running, visit:
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc documentation
