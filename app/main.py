from fastapi import FastAPI

from app.core.config import settings
from app.modules.applicants_module import ApplicantsModule
from app.modules.scores_module import ScoresModule

MODULES = [ApplicantsModule, ScoresModule]


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.version)
    for module in MODULES:
        module.register(app)

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
