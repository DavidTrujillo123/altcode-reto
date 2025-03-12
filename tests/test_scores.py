"""Scoring tests.

NOTE: some import paths here still predate ADR-007; they get updated as part of #412.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.applicants import SAMPLE_APPLICANTS
from app.services.scores import ScoresService

client = TestClient(app)
BY_ID = {a.id: a for a in SAMPLE_APPLICANTS}


@pytest.mark.parametrize(
    ("applicant_id", "value", "band"),
    [("app-001", 850, "A"), ("app-002", 670, "B"), ("app-003", 300, "E"), ("app-004", 770, "A")],
)
def test_compute(applicant_id, value, band):
    score = ScoresService.compute(BY_ID[applicant_id])
    assert (score.value, score.band) == (value, band)


def test_low_scores_go_to_review():
    assert ScoresService.compute(BY_ID["app-003"]).needs_review


def test_score_endpoint_stores_latest():
    created = client.post("/scores/app-002")
    assert created.status_code == 201
    latest = client.get("/scores/app-002")
    assert latest.json()["value"] == created.json()["value"]


def test_score_unknown_applicant_is_404():
    assert client.post("/scores/nope").status_code == 404
