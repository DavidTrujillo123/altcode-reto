from dataclasses import dataclass


@dataclass(frozen=True)
class Applicant:
    """A credit applicant. All sample data in this repo is fictitious."""

    id: str
    display_name: str
    monthly_income: float
    monthly_debt: float
    months_employed: int
    late_payments: int = 0
