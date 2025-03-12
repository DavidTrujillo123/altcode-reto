from app.entities.applicant import Applicant

# Fictitious sample applicants for local development and tests.
SAMPLE_APPLICANTS = [
    Applicant("app-001", "Cliente Demo Uno", 3200.0, 400.0, 48, 0),
    Applicant("app-002", "Cliente Demo Dos", 1800.0, 650.0, 14, 1),
    Applicant("app-003", "Cliente Demo Tres", 950.0, 520.0, 3, 4),
    Applicant("app-004", "Cliente Demo Cuatro", 2500.0, 900.0, 30, 0),
]


class ApplicantsRepository:
    """In-memory store. Swap for a real database adapter in production."""

    def __init__(self) -> None:
        self._items = {a.id: a for a in SAMPLE_APPLICANTS}

    def all(self) -> list[Applicant]:
        return list(self._items.values())

    def get(self, applicant_id: str) -> Applicant | None:
        return self._items.get(applicant_id)
