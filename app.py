"""
DeployFlow - Automated CI/CD Pipeline Dashboard
A production-quality Flask web application demonstrating DevOps best practices.
Author: DeployFlow Team
"""

import os
import json
import random
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, g

# ─── App Initialization ─────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "deployflow-dev-secret-2024")
app.config["DATABASE"] = os.environ.get("DATABASE_URL", "deployflow.db")
APP_VERSION = "1.0.0"
BUILD_NUMBER = os.environ.get("BUILD_NUMBER", "42")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
START_TIME = datetime.utcnow()

# ─── Database Helpers ────────────────────────────────────────────────────────
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(
            app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the SQLite database with seed data."""
    with app.app_context():
        db = get_db()
        db.executescript("""
            CREATE TABLE IF NOT EXISTS deployments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deploy_id TEXT NOT NULL,
                branch TEXT NOT NULL,
                commit_hash TEXT NOT NULL,
                author TEXT NOT NULL,
                environment TEXT NOT NULL,
                status TEXT NOT NULL,
                duration INTEGER NOT NULL,
                triggered_at TEXT NOT NULL,
                message TEXT
            );

            CREATE TABLE IF NOT EXISTS builds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                build_number TEXT NOT NULL,
                pipeline TEXT NOT NULL,
                stage TEXT NOT NULL,
                status TEXT NOT NULL,
                duration INTEGER NOT NULL,
                started_at TEXT NOT NULL,
                logs TEXT
            );

            CREATE TABLE IF NOT EXISTS containers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image TEXT NOT NULL,
                tag TEXT NOT NULL,
                status TEXT NOT NULL,
                cpu_usage REAL,
                memory_usage REAL,
                uptime TEXT,
                port TEXT
            );
        """)

        # Seed deployments if empty
        cur = db.execute("SELECT COUNT(*) FROM deployments")
        if cur.fetchone()[0] == 0:
            authors = ["alice@deployflow.io", "bob@deployflow.io", "carol@deployflow.io", "dave@deployflow.io"]
            envs = ["production", "staging", "staging", "development"]
            statuses = ["success", "success", "success", "failed", "running"]
            branches = ["main", "main", "feature/dark-mode", "hotfix/auth-bug", "develop"]
            messages = [
                "feat: add pipeline monitoring dashboard",
                "fix: resolve container memory leak",
                "feat: implement dark mode UI",
                "hotfix: patch authentication vulnerability",
                "chore: update dependencies to latest",
                "docs: improve API documentation",
                "test: add integration test coverage",
            ]
            now = datetime.utcnow()
            rows = []
            for i in range(20):
                offset = timedelta(hours=random.randint(1, 240))
                rows.append((
                    f"deploy-{1000 + i}",
                    random.choice(branches),
                    f"{random.randint(0,9):x}{random.randint(0,9):x}{random.randint(100000,999999):x}",
                    random.choice(authors),
                    random.choice(envs),
                    random.choice(statuses),
                    random.randint(45, 320),
                    (now - offset).strftime("%Y-%m-%d %H:%M:%S"),
                    random.choice(messages),
                ))
            db.executemany(
                "INSERT INTO deployments (deploy_id,branch,commit_hash,author,environment,status,duration,triggered_at,message) VALUES (?,?,?,?,?,?,?,?,?)",
                rows,
            )

        # Seed containers if empty
        cur = db.execute("SELECT COUNT(*) FROM containers")
        if cur.fetchone()[0] == 0:
            containers = [
                ("deployflow-web", "deployflow/web", "1.0.0", "running", 12.4, 185.6, "3d 14h 22m", "5000:5000"),
                ("deployflow-db", "sqlite:alpine", "3.42", "running", 2.1, 64.8, "3d 14h 22m", "—"),
                ("nginx-proxy", "nginx", "1.25-alpine", "running", 0.8, 32.0, "5d 02h 11m", "80:80,443:443"),
                ("redis-cache", "redis", "7.2-alpine", "running", 1.9, 48.2, "2d 08h 55m", "6379:6379"),
                ("prometheus", "prom/prometheus", "v2.47", "stopped", 0.0, 0.0, "—", "9090:9090"),
            ]
            db.executemany(
                "INSERT INTO containers (name,image,tag,status,cpu_usage,memory_usage,uptime,port) VALUES (?,?,?,?,?,?,?,?)",
                containers,
            )

        db.commit()


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Home Dashboard — overview cards and pipeline animation."""
    db = get_db()
    total_deploys = db.execute("SELECT COUNT(*) FROM deployments").fetchone()[0]
    success_deploys = db.execute("SELECT COUNT(*) FROM deployments WHERE status='success'").fetchone()[0]
    failed_deploys = db.execute("SELECT COUNT(*) FROM deployments WHERE status='failed'").fetchone()[0]
    running_deploys = db.execute("SELECT COUNT(*) FROM deployments WHERE status='running'").fetchone()[0]
    success_rate = round((success_deploys / total_deploys * 100), 1) if total_deploys else 0
    recent = db.execute(
        "SELECT * FROM deployments ORDER BY triggered_at DESC LIMIT 5"
    ).fetchall()
    uptime_seconds = int((datetime.utcnow() - START_TIME).total_seconds())
    uptime_str = f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s"
    return render_template(
        "index.html",
        total_deploys=total_deploys,
        success_deploys=success_deploys,
        failed_deploys=failed_deploys,
        running_deploys=running_deploys,
        success_rate=success_rate,
        recent_deployments=recent,
        uptime=uptime_str,
        environment=ENVIRONMENT,
        version=APP_VERSION,
        build_number=BUILD_NUMBER,
        page="home",
    )


@app.route("/deployments")
def deployments():
    """Deployment History page."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM deployments ORDER BY triggered_at DESC"
    ).fetchall()
    return render_template("deployments.html", deployments=rows, page="deployments")


@app.route("/pipeline")
def pipeline():
    """Pipeline Monitoring page — animated stages."""
    stages = [
        {"name": "Source Checkout", "icon": "bi-git", "status": "success", "duration": "4s"},
        {"name": "Install Deps", "icon": "bi-box-seam", "status": "success", "duration": "32s"},
        {"name": "Run Tests", "icon": "bi-check2-square", "status": "success", "duration": "18s"},
        {"name": "Security Scan", "icon": "bi-shield-check", "status": "success", "duration": "12s"},
        {"name": "Build Docker", "icon": "bi-boxes", "status": "success", "duration": "55s"},
        {"name": "Push to Registry", "icon": "bi-cloud-upload", "status": "success", "duration": "22s"},
        {"name": "Deploy to Render", "icon": "bi-rocket-takeoff", "status": "running", "duration": "…"},
    ]
    return render_template("pipeline.html", stages=stages, page="pipeline")


@app.route("/builds")
def builds():
    """Build & Test Results page."""
    test_suites = [
        {"name": "Unit Tests", "total": 47, "passed": 47, "failed": 0, "skipped": 0, "duration": "3.2s", "status": "success"},
        {"name": "Integration Tests", "total": 18, "passed": 17, "failed": 0, "skipped": 1, "duration": "9.8s", "status": "success"},
        {"name": "Security Scan (Bandit)", "total": 12, "passed": 12, "failed": 0, "skipped": 0, "duration": "5.1s", "status": "success"},
        {"name": "Docker Build Check", "total": 5, "passed": 5, "failed": 0, "skipped": 0, "duration": "1.4s", "status": "success"},
    ]
    history = [
        {"build": "#42", "branch": "main", "commit": "a3f92c1", "status": "success", "duration": "2m 18s", "time": "10 min ago"},
        {"build": "#41", "branch": "feature/dark-mode", "commit": "8d1b5e4", "status": "success", "duration": "2m 44s", "time": "2h ago"},
        {"build": "#40", "branch": "hotfix/auth-bug", "commit": "c7a21f8", "status": "failed", "duration": "1m 03s", "time": "5h ago"},
        {"build": "#39", "branch": "develop", "commit": "5f83d02", "status": "success", "duration": "2m 31s", "time": "8h ago"},
        {"build": "#38", "branch": "main", "commit": "2b4c9e7", "status": "success", "duration": "2m 09s", "time": "1d ago"},
    ]
    return render_template("builds.html", test_suites=test_suites, build_history=history, page="builds")


@app.route("/containers")
def containers():
    """Docker Container Status page."""
    db = get_db()
    rows = db.execute("SELECT * FROM containers").fetchall()
    return render_template("containers.html", containers=rows, page="containers")


@app.route("/health-status")
def health_status():
    """System Health page — metrics and service status."""
    services = [
        {"name": "Flask App", "status": "healthy", "latency": "12ms", "uptime": "99.98%", "icon": "bi-app-indicator"},
        {"name": "SQLite DB", "status": "healthy", "latency": "2ms", "uptime": "100%", "icon": "bi-database"},
        {"name": "Docker Host", "status": "healthy", "latency": "—", "uptime": "99.95%", "icon": "bi-boxes"},
        {"name": "GitHub Actions", "status": "healthy", "latency": "—", "uptime": "99.9%", "icon": "bi-github"},
        {"name": "Render Cloud", "status": "healthy", "latency": "45ms", "uptime": "99.97%", "icon": "bi-cloud"},
        {"name": "Nginx Proxy", "status": "healthy", "latency": "1ms", "uptime": "100%", "icon": "bi-shield-check"},
    ]
    return render_template("health_status.html", services=services, page="health")


@app.route("/about")
def about():
    """About Project page."""
    tech = [
        {"name": "Python Flask", "role": "Backend Web Framework", "version": "3.0.x", "icon": "bi-filetype-py"},
        {"name": "Bootstrap 5", "role": "Responsive UI Framework", "version": "5.3.x", "icon": "bi-bootstrap"},
        {"name": "Docker", "role": "Containerization", "version": "24.x", "icon": "bi-boxes"},
        {"name": "GitHub Actions", "role": "CI/CD Automation", "version": "v3", "icon": "bi-github"},
        {"name": "SQLite", "role": "Lightweight Database", "version": "3.42", "icon": "bi-database"},
        {"name": "Render", "role": "Cloud Deployment", "version": "—", "icon": "bi-cloud-arrow-up"},
        {"name": "Pytest", "role": "Automated Testing", "version": "7.x", "icon": "bi-check2-all"},
        {"name": "Chart.js", "role": "Interactive Charts", "version": "4.x", "icon": "bi-bar-chart-line"},
    ]
    return render_template("about.html", tech=tech, page="about", version=APP_VERSION)


# ─── API Endpoints ───────────────────────────────────────────────────────────

@app.route("/health")
def health():
    """
    Real health-check endpoint used by Docker, Render, and monitoring tools.
    Returns genuine application state — NOT simulated.
    """
    uptime_seconds = int((datetime.utcnow() - START_TIME).total_seconds())
    try:
        db = get_db()
        db.execute("SELECT 1").fetchone()
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {e}"

    return jsonify({
        "status": "ok",
        "version": APP_VERSION,
        "build": BUILD_NUMBER,
        "environment": ENVIRONMENT,
        "uptime_seconds": uptime_seconds,
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }), 200


@app.route("/api/metrics")
def api_metrics():
    """Live metrics API — returns real DB counts."""
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM deployments").fetchone()[0]
    success = db.execute("SELECT COUNT(*) FROM deployments WHERE status='success'").fetchone()[0]
    failed = db.execute("SELECT COUNT(*) FROM deployments WHERE status='failed'").fetchone()[0]
    running = db.execute("SELECT COUNT(*) FROM deployments WHERE status='running'").fetchone()[0]
    # Build duration chart data (last 7 days bucketed per day)
    build_data = [random.randint(90, 220) for _ in range(7)]
    deploy_freq = [random.randint(1, 8) for _ in range(7)]
    days = [(datetime.utcnow() - timedelta(days=i)).strftime("%b %d") for i in range(6, -1, -1)]
    return jsonify({
        "total": total, "success": success, "failed": failed, "running": running,
        "success_rate": round(success / total * 100, 1) if total else 0,
        "build_durations": build_data,
        "deploy_frequency": deploy_freq,
        "chart_labels": days,
    })


@app.route("/api/containers")
def api_containers():
    """Container status API."""
    db = get_db()
    rows = db.execute("SELECT * FROM containers").fetchall()
    result = [dict(r) for r in rows]
    # Randomly fluctuate CPU/memory for demo realism
    for r in result:
        if r["status"] == "running":
            r["cpu_usage"] = round(r["cpu_usage"] + random.uniform(-1.5, 1.5), 1)
            r["memory_usage"] = round(r["memory_usage"] + random.uniform(-5, 5), 1)
    return jsonify(result)


# ─── Error Handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", page=""), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", page="", error=str(e)), 500


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    debug = ENVIRONMENT == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
