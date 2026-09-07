"""Central data loader.

Workbook loading is optional. The app starts from mock_data so the scaffold can
run independently, then can be switched to the AMECATH workbook when desired.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


SHEET_MAP = {
    "Macro_Summary": "macro",
    "Competitor_Matrix": "competitors",
    "Financials_Tenders": "tenders",
    "our ASP": "our_asp",
}


def load_workbook(path: str | Path) -> dict[str, pd.DataFrame]:
    """Load selected workbook sheets as raw DataFrames."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Workbook not found: {path}")

    return {
        output_name: pd.read_excel(path, sheet_name=sheet_name)
        for sheet_name, output_name in SHEET_MAP.items()
    }


def get_default_data() -> dict[str, pd.DataFrame]:
    """Return centralized seed DataFrames."""
    from data.mock_data import (
        ACTIVE_TENDERS,
        CATHETER_PRICING_BENCHMARKS,
        COMPETITOR_PROFILES,
        DIALYSIS_CENTER_DENSITIES,
        MACRO_MARKETS,
    )

    return {
        "macro": MACRO_MARKETS.copy(),
        "competitors": COMPETITOR_PROFILES.copy(),
        "tenders": ACTIVE_TENDERS.copy(),
        "pricing": CATHETER_PRICING_BENCHMARKS.copy(),
        "densities": DIALYSIS_CENTER_DENSITIES.copy(),
    }
