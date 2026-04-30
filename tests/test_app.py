from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.ACEest_Fitness import create_app


def test_health_endpoint() -> None:
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "OK"}


def test_members_endpoint() -> None:
    app = create_app()
    client = app.test_client()

    response = client.get("/members")
    data = response.get_json()

    assert response.status_code == 200
    assert data["count"] == 3
    assert isinstance(data["members"], list)
    assert {"id": 1, "name": "Aarav Sharma", "membership": "active", "plan_id": "basic"} in data[
        "members"
    ]
