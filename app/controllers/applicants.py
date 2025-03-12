"""Applicant rules. Per ADR-007 the domain logic lives under app/controllers: it is what
controls the domain."""

from app.entities.applicant import Applicant
from app.repositories.applicants import ApplicantsRepository


class ApplicantsService:
    def __init__(self, repository: ApplicantsRepository) -> None:
        self.repository = repository

    def list(self) -> list[Applicant]:
        return sorted(self.repository.all(), key=lambda a: a.id)

    def get(self, applicant_id: str) -> Applicant | None:
        return self.repository.get(applicant_id)
