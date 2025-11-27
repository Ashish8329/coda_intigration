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

yaml
Copy code

---

## 🔧 Setup (Local)

### 1. Create virtual env
python3 -m venv venv
source venv/bin/activate

shell
Copy code

### 2. Install dependencies
pip install -r requirements.txt

shell
Copy code

### 3. Run Django
python manage.py runserver

yaml
Copy code

---

## 🐳 Docker Setup

### 1. Create `.env` in root
DEBUG=True
SECRET_KEY=your-secret-key
CODA_API_KEY=your-api-key

shell
Copy code

### 2. Build & Run
docker-compose up --build

yaml
Copy code

This runs:
- Django App  
- Celery Worker  
- Celery Beat Scheduler  

---

## 🔄 Celery Tasks

### Start Celery manually (if not using Docker):
celery -A secureCoda worker -l info
celery -A secureCoda beat -l info

yaml
Copy code

Celery handles:
- Log syncing  
- Scheduled scanning  
- Writing logs to `app.log`

---

## 🌐 Web UI
After running the server, open:

http://localhost:8000

yaml
Copy code

UI pages:
- `/documents` – Synced Coda Documents  
- `/alerts` – Detected anomalies  
- `/scan` – Manual scan trigger  

---

## 📝 Additional Notes
- We added a simple Django-based UI using Tailwind CSS.
- Dockerfile & docker-compose.yml included for easy deployment.
- Celery used for background processing & log tracking.

---

## ⚠️ Current Status
We are facing **some minor issues with the Docker setup**, so for now you are free to use the **Django development server**, which works perfectly.

