"""HTTP routes for applicants. Per ADR-007 the HTTP adapters live under app/services: they
are what the service exposes."""

from fastapi import APIRouter, Depends, HTTPException

from app.core.container import container
from app.dto.applicants import ApplicantOut
from app.services.applicants import ApplicantsService

router = APIRouter(prefix="/applicants", tags=["applicants"])


def get_service() -> ApplicantsService:
    return container.resolve(ApplicantsService)


@router.get("", response_model=list[ApplicantOut])
def list_applicants(service: ApplicantsService = Depends(get_service)) -> list[ApplicantOut]:
    return [ApplicantOut.from_entity(a) for a in service.list()]


@router.get("/{applicant_id}", response_model=ApplicantOut)
def get_applicant(
    applicant_id: str, service: ApplicantsService = Depends(get_service)
) -> ApplicantOut:
    applicant = service.get(applicant_id)
    if applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return ApplicantOut.from_entity(applicant)
