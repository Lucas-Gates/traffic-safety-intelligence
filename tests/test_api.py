from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "traffic-safety-intelligence"}

def test_overview_stats_structure():
    response = client.get("/api/stats/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_crashes" in data
    assert "total_fatalities" in data
    assert isinstance(data["total_crashes"], int)

def test_state_rankings_limit():
    limit = 5
    response = client.get(f"/api/analytics/state-rankings?limit={limit}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= limit
    if len(data) > 0:
        assert "statename" in data[0]
        assert "crash_rank" in data[0]