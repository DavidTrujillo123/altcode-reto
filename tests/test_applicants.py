"""API tests for applicants.

NOTE: some import paths here still predate ADR-007; they get updated as part of #412.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_applicants_is_sorted():
    resp = client.get("/applicants")
    assert resp.status_code == 200
    ids = [a["id"] for a in resp.json()]
    assert ids == sorted(ids)
    assert len(ids) == 4


def test_get_applicant():
    resp = client.get("/applicants/app-002")
    assert resp.status_code == 200
    assert resp.json()["display_name"] == "Cliente Demo Dos"


def test_unknown_applicant_is_404():
    assert client.get("/applicants/nope").status_code == 404
