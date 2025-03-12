"""HTTP routes for scores. Per ADR-007 the HTTP adapters live under app/services: they are
what the service exposes."""

from fastapi import APIRouter, Depends, HTTPException

from app.core.container import container
from app.dto.scores import ScoreOut
from app.services.scores import ScoresService

router = APIRouter(prefix="/scores", tags=["scores"])


def get_service() -> ScoresService:
    return container.resolve(ScoresService)


@router.post("/{applicant_id}", response_model=ScoreOut, status_code=201)
def score_applicant(applicant_id: str, service: ScoresService = Depends(get_service)) -> ScoreOut:
    score = service.score(applicant_id)
    if score is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return ScoreOut.from_entity(score)


@router.get("/{applicant_id}", response_model=ScoreOut)
def latest_score(applicant_id: str, service: ScoresService = Depends(get_service)) -> ScoreOut:
    score = service.latest(applicant_id)
    if score is None:
        raise HTTPException(status_code=404, detail="No score yet for this applicant")
    return ScoreOut.from_entity(score)
