"""Detection data structures."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Finding:
    """A lightweight analysis finding."""

    rule: str
    message: str
    severity: str = "info"
    metadata: dict[str, str] = field(default_factory=dict)
