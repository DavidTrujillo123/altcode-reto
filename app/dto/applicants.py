from pydantic import BaseModel

from app.entities.applicant import Applicant


class ApplicantOut(BaseModel):
    id: str
    display_name: str
    monthly_income: float
    monthly_debt: float
    months_employed: int
    late_payments: int

    @classmethod
    def from_entity(cls, applicant: Applicant) -> "ApplicantOut":
        return cls(**applicant.__dict__)
