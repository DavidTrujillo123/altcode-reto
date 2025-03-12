from app.entities.score import Score


class ScoresRepository:
    """Keeps the latest score per applicant, in memory."""

    def __init__(self) -> None:
        self._latest: dict[str, Score] = {}

    def save(self, score: Score) -> Score:
        self._latest[score.applicant_id] = score
        return score

    def latest(self, applicant_id: str) -> Score | None:
        return self._latest.get(applicant_id)
