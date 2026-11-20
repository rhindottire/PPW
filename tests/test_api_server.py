"""Integration tests for deploy/server.py FastAPI application."""

from starlette.testclient import TestClient

from deploy.server import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.0.0"


def test_serve_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "PageRank Research Workbench" in response.text
    assert "<!DOCTYPE html>" in response.text


def test_get_graph_endpoint():
    response = client.get("/api/graph")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert "stats" in data
    assert "table" in data
    assert "vector_history" in data
    assert "matrix_sample" in data
    assert data["stats"]["total_nodes"] >= 65
    assert len(data["table"]) >= 65
    assert data["table"][0]["website"] == "trunojoyo.ac.id"


def test_recalculate_pagerank_endpoint():
    payload = {"damping": 0.70, "tolerance": 1e-6, "max_iter": 150}
    response = client.post("/api/pagerank/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "table" in data
    assert "iterations" in data
    assert "vector_history" in data
    assert data["converged"] is True
    assert len(data["table"]) >= 65


def test_probe_crawler_validation():
    # Bad URL format should raise 400
    response = client.post("/api/crawler/probe", json={"url": "not-a-valid-url"})
    assert response.status_code == 400


def test_node_breakdown_endpoint():
    response = client.get("/api/node/siakad.trunojoyo.ac.id/breakdown")
    assert response.status_code == 200
    data = response.json()
    assert data["target_node"] == "siakad.trunojoyo.ac.id"
    assert "current_pagerank" in data
    assert "referrers" in data
    assert isinstance(data["referrers"], list)
    assert len(data["referrers"]) > 0


def test_simulate_pagerank_endpoint():
    payload = {
        "target_node": "siakad.trunojoyo.ac.id",
        "added_in_links": ["trunojoyo.ac.id"],
        "removed_in_links": [],
        "damping": 0.85,
    }
    response = client.post("/api/pagerank/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target_node"] == "siakad.trunojoyo.ac.id"
    assert "delta_pr" in data
    assert "new_pagerank" in data
