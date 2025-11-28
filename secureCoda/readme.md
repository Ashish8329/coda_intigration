# SecureCoda – Audit & Monitoring System

SecureCoda is a lightweight Django-based system that integrates with **Coda’s API**, collects audit logs, detects anomalies, and displays alerts in a simple UI.  
The project also includes Docker support, Celery workers, scheduled scanning, and a basic Tailwind-powered frontend.

---

## 🚀 Features
- Coda API Integration (REST API + Token Authentication)
- Document Sync Service
- Audit Log Scanner (Anomaly Detection)
- Alerts Dashboard (Django Templates)
- Celery Worker for background scanning
- Celery Beat for scheduled tasks
- Docker + Docker Compose support
- Simple Django UI (Tailwind CSS)
- Log file tracking (`app.log`)

---

## 📁 Project Structure
secureCoda/
│
├── scanner/ # Sync + scanning logic
├── secureCoda/ # Django project settings
├── templates/ # Simple HTML UI
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt


---

## 🔧 Setup (Local)

### 1. Create virtual env
python3 -m venv venv
source venv/bin/activate


### 2. Install dependencies
pip install -r requirements.txt

### 2.1 Naviagate to Root Directory
cd secureCode

#### 2.2 Run migrate command
python manage.py migrate

### 3. Run Django
python manage.py runserver

### visit UI
visit -> http://127.0.0.1:8000/api/dashboard/alerts/ for alerts and documents

---

## 🐳 Docker Setup

### 1. Build & Run
docker-compose up --build

This runs:
- Django App  
- Celery Worker  
- Celery Beat Scheduler  

---

## 🔄 Celery Tasks

### Start Celery manually (if not using Docker):
celery -A secureCoda worker -l info
celery -A secureCoda beat -l info

Celery handles:
- Log syncing  
- Scheduled scanning  
- Writing logs to `app.log`

---

## 🌐 Web UI
After running the server, open:

http://localhost:8000


UI pages:
- `api/dashboard/documents` – Synced Coda Documents  
- `api/dashboard/alerts` – Detected anomalies  
- `/scan` – Manual scan trigger  

---

## 📝 Additional Notes
- We added a simple Django-based UI using Tailwind CSS.
- Dockerfile & docker-compose.yml included for easy deployment.
- Celery used for background processing & log tracking.

## Love to Hear any Suggestion and Improvements
