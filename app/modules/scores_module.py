from fastapi import FastAPI

from app.core.container import container
from app.repositories.applicants import ApplicantsRepository
from app.repositories.scores import ScoresRepository
from app.services.scores import ScoresService


class ScoresModule:
    """Feature module: registers the layer providers and mounts the router."""

    @staticmethod
    def register(app: FastAPI) -> None:
        # Lazy import: importing the router at module level brings back the cycle (#412).
        from app.controllers.scores import router

        container.register(ScoresRepository)
        container.register(
            ScoresService,
            lambda c: ScoresService(c.resolve(ApplicantsRepository), c.resolve(ScoresRepository)),
        )
        app.include_router(router)
