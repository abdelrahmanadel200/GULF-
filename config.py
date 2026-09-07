"""Application-wide configuration for the AMECATH Executive Decision Engine."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    background: str = "#0b1628"
    card: str = "#13274c"
    gold: str = "#f59e0b"
    blue: str = "#3b82f6"
    text: str = "#e2e8f0"
    muted: str = "#94a3b8"
    border: str = "#25466f"
    success: str = "#34d399"
    danger: str = "#ef4444"


THEME = Theme()

APP_TITLE = "AMECATH | Executive Decision Engine"
DEFAULT_MARGIN_PCT = 0.35
MIN_MARGIN_PCT = 0.20
MAX_MARGIN_PCT = 0.60
