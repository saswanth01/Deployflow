# 🚀 DeployFlow — Automated CI/CD Pipeline for a Containerized Web Application

<div align="center">

![DeployFlow Banner](https://img.shields.io/badge/DeployFlow-CI%2FCD%20Dashboard-6366f1?style=for-the-badge&logo=rocket&logoColor=white)

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/deployflow/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/YOUR_USERNAME/deployflow/actions)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**A production-quality DevOps monitoring dashboard with a fully automated CI/CD pipeline.**  
*Final Year Engineering Project — Demonstrating End-to-End DevOps Workflow*

[🌐 Live Demo](#deployment) · [📋 Features](#features) · [🛠️ Installation](#installation) · [🐳 Docker](#docker) · [🔄 CI/CD](#cicd)

</div>

---

## 📖 Project Overview

**DeployFlow** is a professional-grade DevOps monitoring dashboard built with Python Flask. It demonstrates a complete, automated CI/CD (Continuous Integration / Continuous Deployment) pipeline that:

1. **Automatically tests** every code push with Pytest
2. **Containerizes** the app with Docker on every successful test
3. **Deploys** to Render cloud hosting on every merge to `main`

This project is designed as a **final-year engineering project** to showcase end-to-end DevOps engineering practices in a visually impressive, fully functional application.

---

## 🎯 Objectives

| # | Objective | Technology |
|---|-----------|------------|
| 1 | Build a modern, responsive web application | Flask, Bootstrap 5, Chart.js |
| 2 | Containerize the application | Docker, Dockerfile, docker-compose |
| 3 | Automate testing on every push | Pytest, GitHub Actions |
| 4 | Build and validate Docker images in CI | Docker Buildx, GitHub Actions |
| 5 | Deploy automatically to cloud | Render, Deploy Hook |
| 6 | Monitor deployment pipeline | DeployFlow Dashboard |

---

## ✨ Features

### 🖥️ Application Pages
| Page | Route | Description |
|------|-------|-------------|
| **Home Dashboard** | `/` | KPI cards, charts, recent deployments |
| **Deployment History** | `/deployments` | Filterable table of all deployments |
| **Pipeline Monitoring** | `/pipeline` | Animated CI/CD stage visualization |
| **Build & Test Results** | `/builds` | Test suite results and build history |
| **Docker Container Status** | `/containers` | Container cards with CPU/memory metrics |
| **System Health** | `/health-status` | Service uptime and health monitoring |
| **About Project** | `/about` | Architecture, tech stack, project info |

### 🔌 API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | **Real** app health check (used by Docker & Render) |
| `/api/metrics` | GET | Deployment metrics and chart data |
| `/api/containers` | GET | Container status data |

### 🎨 UI/UX Features
- 🌙 **Dark navy theme** with blue, purple, and cyan accents
- 📱 **Fully responsive** — desktop, tablet, and mobile
- ✨ **Animated pipeline** stage visualization
- 📊 **Interactive charts** (Chart.js) for build duration and deploy frequency
- 🟢 **Live health status** indicator with real endpoint data
- 🔍 **Filterable** deployment history table
- 🐋 **Docker command reference** panel

---

## 🏗️ Architecture

```
Developer → git push → GitHub → GitHub Actions CI/CD Pipeline
                                      │
                            ┌─────────┴──────────┐
                            │                    │
                        🧪 Test Job         (after test passes)
                        pytest -v               │
                            │                   ▼
                            └──────→ 🐋 Docker Build Job
                                     docker build + health check
                                            │
                                    (on main branch only)
                                            ▼
                                    🌐 Deploy Job
                                    Render Deploy Hook
                                            │
                                            ▼
                                    ✅ Live Website
                                    yourapp.onrender.com
```

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Backend** | Python Flask | 3.0.3 | Web framework and API |
| **Database** | SQLite | 3.42 | Lightweight persistence |
| **Frontend** | Bootstrap 5 | 5.3.2 | Responsive UI framework |
| **Charts** | Chart.js | 4.4.0 | Interactive data visualizations |
| **Icons** | Bootstrap Icons | 1.11.3 | Professional icon set |
| **WSGI** | Gunicorn | 21.2.0 | Production-grade server |
| **Containers** | Docker | 24.x | Application containerization |
| **CI/CD** | GitHub Actions | v4 | Automated pipeline |
| **Deployment** | Render | — | Cloud hosting |
| **Testing** | Pytest | 7.4.4 | Automated test suite |

---

## 📁 Project Structure

```
deployflow/
├── app.py                        # Flask application — routes, DB, API
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Production Docker image (non-root, Gunicorn)
├── docker-compose.yml            # Local multi-service compose setup
├── .dockerignore                 # Docker build exclusions
├── .gitignore                    # Git exclusions
├── README.md                     # This documentation
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # GitHub Actions CI/CD pipeline
│
├── templates/
│   ├── base.html                 # Shared layout: sidebar, topbar, footer
│   ├── index.html                # Home Dashboard with KPI cards + charts
│   ├── deployments.html          # Deployment history with filter
│   ├── pipeline.html             # Animated pipeline visualization
│   ├── builds.html               # Test results and build history
│   ├── containers.html           # Docker container status cards
│   ├── health_status.html        # System health monitoring
│   ├── about.html                # Project info and architecture
│   ├── 404.html                  # 404 error page
│   └── 500.html                  # 500 error page
│
├── static/
│   ├── css/
│   │   └── style.css             # Complete dark theme (1,000+ lines)
│   └── js/
│       └── main.js               # Sidebar, clock, animations
│
└── tests/
    ├── __init__.py
    └── test_app.py               # 38 unit + integration tests
```

---

## 🛠️ Installation (Local Development)

### Prerequisites
- Python 3.9+ (3.11 recommended)
- Git
- Docker Desktop (for containerization)

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/deployflow.git
cd deployflow
```

### Step 2 — Create a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the application
```bash
python app.py
```

> The application initializes the SQLite database automatically on first run.

### Step 5 — Open in browser
```
http://localhost:5000
```

### Step 6 — Verify health endpoint
```bash
curl http://localhost:5000/health
```
Expected response:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "build": "42",
  "environment": "development",
  "uptime_seconds": 12,
  "database": "ok",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🧪 Testing

### Run all tests
```bash
pytest tests/ -v
```

### Run with coverage report
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Expected output
```
collected 38 items

tests/test_app.py::TestPageRoutes::test_home_route_ok PASSED         [  2%]
tests/test_app.py::TestHealthEndpoint::test_health_returns_200 PASSED [ 28%]
tests/test_app.py::TestHealthEndpoint::test_health_status_ok PASSED   [ 34%]
...

====================== 38 passed in 3.21s ======================
```

### Test categories
| Category | Count | Tests |
|----------|-------|-------|
| Page Routes | 10 | All 7 pages + content checks |
| Health Endpoint | 10 | Status, JSON, fields, DB |
| API Endpoints | 9 | Metrics and containers APIs |
| Error Handlers | 2 | 404 handling |
| Database | 3 | Seeding and integrity |
| Page Content | 4 | UI element presence |

---

## 🐳 Docker

### Build the image
```bash
docker build -t deployflow:latest .
```

### Run the container
```bash
docker run -d \
  --name deployflow \
  -p 5000:5000 \
  -e ENVIRONMENT=production \
  -e SECRET_KEY=your-secret-key-here \
  deployflow:latest
```

### View logs
```bash
docker logs -f deployflow
```

### Inspect container health
```bash
docker inspect --format='{{json .State.Health}}' deployflow
```

### Stop and remove
```bash
docker stop deployflow
docker rm deployflow
```

---

## 🐳 Docker Compose (Recommended)

### Start all services
```bash
docker-compose up -d --build
```

### View running services
```bash
docker-compose ps
```

### View logs
```bash
docker-compose logs -f
```

### Stop all services
```bash
docker-compose down
```

### Stop and remove volumes
```bash
docker-compose down -v
```

> **Note:** The SQLite database is persisted in a Docker named volume (`deployflow-data`), so data survives container restarts.

---

## 🔄 CI/CD Pipeline — GitHub Actions

### Pipeline Overview

```
Push to main / Pull Request
         │
         ▼
┌─────────────────┐
│  🧪 Test Job    │  → checkout → setup python → pip install
│  (always runs)  │  → pytest tests/ -v → validate /health
└────────┬────────┘
         │ (passes)
         ▼
┌─────────────────┐
│  🐋 Docker Job  │  → build image → run container
│  (after tests)  │  → curl /health → check HTTP 200
└────────┬────────┘
         │ (passes + main branch only)
         ▼
┌─────────────────┐
│  🌐 Deploy Job  │  → POST to RENDER_DEPLOY_HOOK
│  (main only)    │  → print deployment summary
└─────────────────┘
```

### Setting Up GitHub Actions

**1. Push your code to GitHub:**
```bash
git init
git add .
git commit -m "feat: initial DeployFlow application"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/deployflow.git
git push -u origin main
```

**2. Watch the pipeline run:**
- Go to your GitHub repo
- Click the **Actions** tab
- Watch "🚀 DeployFlow CI/CD" workflow execute

**3. Required GitHub Secret (for deployment):**

| Secret Name | Value | Where to Get |
|-------------|-------|--------------|
| `RENDER_DEPLOY_HOOK` | Your Render deploy hook URL | Render Dashboard → Service → Settings → Deploy Hook |

**To add secrets:** GitHub repo → Settings → Secrets and variables → Actions → New repository secret

---

## 🌐 Render Deployment

### Step-by-Step Render Setup

**1. Create a Render account** at [render.com](https://render.com)

**2. Create a new Web Service:**
- Click "New" → "Web Service"
- Connect your GitHub repository
- Render will auto-detect the `Dockerfile`

**3. Configure the service:**

| Setting | Value |
|---------|-------|
| **Name** | `deployflow` |
| **Environment** | Docker |
| **Branch** | `main` |
| **Health Check Path** | `/health` |

**4. Set environment variables in Render:**

| Variable | Value |
|----------|-------|
| `ENVIRONMENT` | `production` |
| `SECRET_KEY` | (generate a random 32-char string) |
| `PORT` | `5000` |

**5. Get the Deploy Hook:**
- Render Dashboard → Your Service → Settings → "Deploy Hook"
- Copy the URL and add it as `RENDER_DEPLOY_HOOK` secret in GitHub

**6. First manual deploy:**
- Click "Manual Deploy" → "Deploy Latest Commit"
- Wait ~3-5 minutes for the first build

**7. Verify deployment:**
```bash
curl https://your-app-name.onrender.com/health
```

> ⚠️ **Free Render tier:** Services spin down after 15 minutes of inactivity and take ~30s to restart on the next request. This is normal for the free tier.

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5000` | Application port |
| `ENVIRONMENT` | `development` | Environment name |
| `SECRET_KEY` | `deployflow-dev-secret-2024` | Flask session secret |
| `DATABASE_URL` | `deployflow.db` | SQLite database path |
| `BUILD_NUMBER` | `42` | Build number (set by CI) |

> ⚠️ **Never commit `SECRET_KEY` to source control.** Use environment variables or GitHub Secrets.

---

## 🔧 Troubleshooting

### App won't start locally
```bash
# Check Python version (needs 3.9+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for port conflicts
netstat -an | grep 5000
```

### Docker build fails
```bash
# Build with verbose output
docker build --no-cache -t deployflow:latest . 2>&1

# Check Docker daemon is running
docker info
```

### Tests fail
```bash
# Run tests with verbose traceback
pytest tests/ -v --tb=long

# Run a single test
pytest tests/test_app.py::TestHealthEndpoint::test_health_returns_200 -v
```

### GitHub Actions fails
1. Check the **Actions** tab for detailed logs
2. Verify `requirements.txt` is up to date
3. Ensure `RENDER_DEPLOY_HOOK` secret is set (for deploy step)

### Render not deploying
1. Check the deploy hook URL is correct in GitHub Secrets
2. Verify Render service is not suspended (free tier limits)
3. Check Render dashboard logs for startup errors

---

## 📸 Screenshots

> *Replace these placeholders with actual screenshots after deployment*

| Page | Screenshot |
|------|-----------|
| Home Dashboard | `screenshots/dashboard.png` |
| Pipeline Monitoring | `screenshots/pipeline.png` |
| Docker Containers | `screenshots/containers.png` |
| GitHub Actions | `screenshots/github-actions.png` |
| Render Dashboard | `screenshots/render.png` |

---

## 👥 Project Team

**DeployFlow — Final Year Engineering Project**

> *Built to demonstrate end-to-end DevOps engineering: application development, containerization, automated testing, CI/CD pipeline configuration, and cloud deployment.*

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**Built with ❤️ using Flask · Docker · GitHub Actions · Render**

*⭐ Star this repo if it helped your DevOps learning journey!*

</div>
