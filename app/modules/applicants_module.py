from fastapi import FastAPI

from app.core.container import container
from app.repositories.applicants import ApplicantsRepository
from app.services.applicants import ApplicantsService


class ApplicantsModule:
    """Feature module: registers the layer providers and mounts the router."""

    @staticmethod
    def register(app: FastAPI) -> None:
        # Lazy import: importing the router at module level brings back the cycle (#412).
        from app.controllers.applicants import router

        container.register(ApplicantsRepository)
        container.register(
            ApplicantsService, lambda c: ApplicantsService(c.resolve(ApplicantsRepository))
        )
        app.include_router(router)
