# AI Threat Detector

AI Threat Detector is a professional, production-style cybersecurity monitoring platform built with FastAPI, SQLite, JWT authentication, and an AI anomaly detection engine.

## Features
- Secure JWT authentication with bcrypt password hashing
- Isolation Forest anomaly detection for realistic threat scoring
- Real-time dashboard updates with dynamic charts and alerts
- Threat logs stored in SQLite for persistence
- Exportable PDF and CSV reports
- Purple/black themed modern UI with animations and responsive layout
- Environment-based configuration with `.env`
- Docker-ready deployment

## Project Structure
- `main.py` - application entry point
- `config/` - environment and runtime settings
- `models/` - database schema definitions
- `routes/` - HTTP page and API routes
- `services/` - authentication, data generation, reporting, rate limiting
- `ai_engine/` - anomaly detection logic
- `templates/` - HTML views
- `static/` - assets (CSS/JavaScript)

## Setup
1. Create and activate a Python environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
4. Set `SECRET_KEY` and confirm admin values in `.env`
5. Run locally:
   ```bash
   uvicorn main:app --reload
   ```
6. Visit `http://localhost:8000/login`

## Deployment
- Use Docker:
  ```bash
  docker compose up --build
  ```
- The app is ready for hosting on Render, AWS EC2, or any container platform.

## Notes
- Do not commit `.env`
- If you want to customize admin credentials, update `.env`
- The system is designed for local development and production-ready deployment
