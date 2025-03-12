import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "scoring-api")
    version: str = os.getenv("APP_VERSION", "0.4.0")
    # Below this score an application goes to manual review.
    review_threshold: int = int(os.getenv("REVIEW_THRESHOLD", "550"))


settings = Settings()
