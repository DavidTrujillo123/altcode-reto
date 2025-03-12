from datetime import datetime

from pydantic import BaseModel

from app.entities.score import Score


class ScoreOut(BaseModel):
    applicant_id: str
    value: int
    band: str
    needs_review: bool
    reasons: list[str]
    computed_at: datetime

    @classmethod
    def from_entity(cls, score: Score) -> "ScoreOut":
        return cls(**score.__dict__)
