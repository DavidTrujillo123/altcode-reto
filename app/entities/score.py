from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class Score:
    applicant_id: str
    value: int
    band: str
    needs_review: bool
    reasons: list[str] = field(default_factory=list)
    computed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
