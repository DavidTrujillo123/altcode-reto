"""Scoring rules. Per ADR-007 the domain logic lives under app/controllers: it is what
controls the domain."""

from app.core.config import settings
from app.entities.applicant import Applicant
from app.entities.score import Score
from app.repositories.applicants import ApplicantsRepository
from app.repositories.scores import ScoresRepository

BANDS = [(750, "A"), (650, "B"), (550, "C"), (450, "D")]
MAX_SCORE, MIN_SCORE = 850, 300


class ScoresService:
    def __init__(self, applicants: ApplicantsRepository, scores: ScoresRepository) -> None:
        self.applicants = applicants
        self.scores = scores

    def score(self, applicant_id: str) -> Score | None:
        applicant = self.applicants.get(applicant_id)
        if applicant is None:
            return None
        return self.scores.save(self.compute(applicant))

    def latest(self, applicant_id: str) -> Score | None:
        return self.scores.latest(applicant_id)

    @staticmethod
    def compute(applicant: Applicant) -> Score:
        value, reasons = MAX_SCORE, []
        income = applicant.monthly_income
        ratio = applicant.monthly_debt / income if income > 0 else 1.0
        if ratio > 0.4:
            value -= 200
            reasons.append("debt_to_income_high")
        elif ratio > 0.25:
            value -= 80
            reasons.append("debt_to_income_medium")
        if applicant.months_employed < 6:
            value -= 120
            reasons.append("short_employment")
        elif applicant.months_employed < 24:
            value -= 40
        if applicant.late_payments:
            value -= 60 * min(applicant.late_payments, 5)
            reasons.append("late_payments")
        value = max(MIN_SCORE, min(MAX_SCORE, value))
        band = next((b for floor, b in BANDS if value >= floor), "E")
        return Score(
            applicant_id=applicant.id,
            value=value,
            band=band,
            needs_review=value < settings.review_threshold,
            reasons=reasons,
        )
