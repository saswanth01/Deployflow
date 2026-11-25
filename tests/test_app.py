"""
DeployFlow — Automated Test Suite
Tests the Flask routes, health endpoint, API endpoints, and application behavior.
Run with: pytest tests/ -v --tb=short
"""

import json
import os
import sys
import pytest

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, init_db


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def client(tmp_path):
    """Create a test client with an isolated temp database."""
    db_path = str(tmp_path / "test_deployflow.db")
    app.config["TESTING"] = True
    app.config["DATABASE"] = db_path
    app.config["SECRET_KEY"] = "test-secret-key"
    with app.app_context():
        init_db()
    with app.test_client() as client:
        yield client


# ─── Route Tests ──────────────────────────────────────────────────────────────

class TestPageRoutes:
    """Test that all navigation pages return HTTP 200."""

    def test_home_route_ok(self, client):
        """Home dashboard should return 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_home_contains_deployflow(self, client):
        """Home page should contain the DeployFlow brand name."""
        response = client.get("/")
        assert b"DeployFlow" in response.data

    def test_deployments_route(self, client):
        """Deployments history page should return 200."""
        response = client.get("/deployments")
        assert response.status_code == 200

    def test_deployments_has_table(self, client):
        """Deployments page should include a table."""
        response = client.get("/deployments")
        assert b"<table" in response.data

    def test_pipeline_route(self, client):
        """Pipeline monitoring page should return 200."""
        response = client.get("/pipeline")
        assert response.status_code == 200

    def test_pipeline_has_stages(self, client):
        """Pipeline page should show stage names."""
        response = client.get("/pipeline")
        assert b"Source Checkout" in response.data or b"pipeline" in response.data.lower()

    def test_builds_route(self, client):
        """Build & test results page should return 200."""
        response = client.get("/builds")
        assert response.status_code == 200

    def test_containers_route(self, client):
        """Docker container status page should return 200."""
        response = client.get("/containers")
        assert response.status_code == 200

    def test_health_status_route(self, client):
        """System health page should return 200."""
        response = client.get("/health-status")
        assert response.status_code == 200

    def test_about_route(self, client):
        """About project page should return 200."""
        response = client.get("/about")
        assert response.status_code == 200


# ─── Health Endpoint Tests ────────────────────────────────────────────────────

class TestHealthEndpoint:
    """Test the /health API endpoint returns correct data."""

    def test_health_returns_200(self, client):
        """Health endpoint must return HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self, client):
        """Health endpoint must return valid JSON."""
        response = client.get("/health")
        assert response.content_type == "application/json"

    def test_health_status_ok(self, client):
        """Health response must have status = 'ok'."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert data["status"] == "ok"

    def test_health_has_version(self, client):
        """Health response must include version field."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_health_has_uptime(self, client):
        """Health response must include uptime_seconds."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], int)
        assert data["uptime_seconds"] >= 0

    def test_health_has_database_field(self, client):
        """Health response must include database status."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert "database" in data

    def test_health_database_ok(self, client):
        """Health endpoint must report database as 'ok'."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert data["database"] == "ok"

    def test_health_has_timestamp(self, client):
        """Health response must include an ISO timestamp."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert "timestamp" in data
        assert "Z" in data["timestamp"]

    def test_health_has_environment(self, client):
        """Health response must include environment field."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert "environment" in data

    def test_health_has_build(self, client):
        """Health response must include build number."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert "build" in data


# ─── API Endpoint Tests ───────────────────────────────────────────────────────

class TestAPIEndpoints:
    """Test the JSON API endpoints."""

    def test_api_metrics_returns_200(self, client):
        """Metrics API must return HTTP 200."""
        response = client.get("/api/metrics")
        assert response.status_code == 200

    def test_api_metrics_returns_json(self, client):
        """Metrics API must return valid JSON."""
        response = client.get("/api/metrics")
        assert response.content_type == "application/json"

    def test_api_metrics_has_total(self, client):
        """Metrics must include total deployment count."""
        response = client.get("/api/metrics")
        data = json.loads(response.data)
        assert "total" in data
        assert isinstance(data["total"], int)

    def test_api_metrics_has_success_rate(self, client):
        """Metrics must include success_rate."""
        response = client.get("/api/metrics")
        data = json.loads(response.data)
        assert "success_rate" in data

    def test_api_metrics_has_chart_data(self, client):
        """Metrics must include chart labels and build durations."""
        response = client.get("/api/metrics")
        data = json.loads(response.data)
        assert "chart_labels" in data
        assert "build_durations" in data
        assert len(data["chart_labels"]) == 7
        assert len(data["build_durations"]) == 7

    def test_api_containers_returns_200(self, client):
        """Containers API must return HTTP 200."""
        response = client.get("/api/containers")
        assert response.status_code == 200

    def test_api_containers_returns_list(self, client):
        """Containers API must return a JSON array."""
        response = client.get("/api/containers")
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_api_containers_has_items(self, client):
        """Containers API must return at least one container."""
        response = client.get("/api/containers")
        data = json.loads(response.data)
        assert len(data) > 0

    def test_api_containers_item_structure(self, client):
        """Each container must have name, image, status fields."""
        response = client.get("/api/containers")
        data = json.loads(response.data)
        item = data[0]
        assert "name" in item
        assert "image" in item
        assert "status" in item


# ─── Error Handler Tests ──────────────────────────────────────────────────────

class TestErrorHandlers:
    """Test HTTP error pages."""

    def test_404_handler(self, client):
        """Non-existent route should return 404."""
        response = client.get("/this-page-does-not-exist-xyz")
        assert response.status_code == 404

    def test_404_contains_message(self, client):
        """404 page should contain helpful text."""
        response = client.get("/nonexistent-route-abc")
        assert b"404" in response.data or b"Not Found" in response.data


# ─── Database Tests ───────────────────────────────────────────────────────────

class TestDatabase:
    """Test database initialization and seeding."""

    def test_deployments_seeded(self, client):
        """Database should be seeded with deployment records."""
        response = client.get("/api/metrics")
        data = json.loads(response.data)
        assert data["total"] > 0

    def test_containers_seeded(self, client):
        """Database should be seeded with container records."""
        response = client.get("/api/containers")
        data = json.loads(response.data)
        assert len(data) > 0

    def test_success_plus_failed_le_total(self, client):
        """Sum of success + failed must be <= total deployments."""
        response = client.get("/api/metrics")
        data = json.loads(response.data)
        assert data["success"] + data["failed"] <= data["total"]


# ─── Content Tests ────────────────────────────────────────────────────────────

class TestPageContent:
    """Test that pages contain expected content."""

    def test_home_has_kpi_cards(self, client):
        """Home page should contain KPI data."""
        response = client.get("/")
        assert b"Total Deployments" in response.data or b"kpi" in response.data.lower()

    def test_containers_has_docker_name(self, client):
        """Containers page should mention docker or container content."""
        response = client.get("/containers")
        assert b"deployflow" in response.data.lower() or b"container" in response.data.lower()

    def test_about_has_tech_stack(self, client):
        """About page should list technologies."""
        response = client.get("/about")
        assert b"Flask" in response.data or b"Docker" in response.data

    def test_sidebar_navigation_links(self, client):
        """Pages should contain sidebar navigation."""
        response = client.get("/")
        assert b"sidebar" in response.data.lower() or b"nav-link" in response.data
