# -*- coding: utf-8 -*-
"""
data_utils.py
--------------
Parsing, extraction, and metric-calculation utilities for the AMECATH
Executive Market Intelligence Dashboard.

Deliberately kept free of any Streamlit import so it can be unit-tested
in a plain Python environment.
"""
from __future__ import annotations

import re
import glob
import os
from pathlib import Path
from functools import lru_cache

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Static configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent 

COUNTRY_FILES = {
    "Saudi Arabia": "AMECATH_Saudi_Arabia_Executive_Dashboard.xlsx",
    "UAE": "AMECATH_UAE_Executive_Dashboard.xlsx",
    "Qatar": "AMECATH_Qatar_Executive_Dashboard.xlsx",
    "Kuwait": "AMECATH_Kuwait_Executive_Dashboard.xlsx",
    "Oman": "AMECATH_Oman_Executive_Dashboard.xlsx",
    "Bahrain": "AMECATH_Bahrain_Executive_Dashboard.xlsx",
    "Jordan": "AMECATH_Jordan_Executive_Dashboard.xlsx",
    "Lebanon": "AMECATH_Lebanon_Executive_Dashboard.xlsx",
}

COUNTRY_META = {
    "Saudi Arabia": {"flag": "🇸🇦", "tier": "Tier 1", "region": "GCC"},
    "UAE":          {"flag": "🇦🇪", "tier": "Tier 1", "region": "GCC"},
    "Qatar":        {"flag": "🇶🇦", "tier": "Tier 2", "region": "GCC"},
    "Kuwait":       {"flag": "🇰🇼", "tier": "Tier 2", "region": "GCC"},
    "Oman":         {"flag": "🇴🇲", "tier": "Tier 3", "region": "GCC"},
    "Bahrain":      {"flag": "🇧🇭", "tier": "Tier 3", "region": "GCC"},
    "Jordan":       {"flag": "🇯🇴", "tier": "Tier 3", "region": "Levant"},
    "Lebanon":      {"flag": "🇱🇧", "tier": "Tier 3", "region": "Levant"},
}

TIER_COLORS = {
    "Tier 1": "#14B8A6",   # medical teal
    "Tier 2": "#38BDF8",   # cyan
    "Tier 3": "#94A3B8",   # slate gray
}

SHEET_ORDER = [
    "1. Macro & Exec Summary",
    "2. Hospitals & Infrastructure",
    "3. Regulatory & Compliance",
    "4. Competitors & Pricing",
    "5. Distribution Channels",
    "6. KOLs & Decision-Makers",
    "7. Sources & Methodology",
]

SHEET_ICONS = {
    "1. Macro & Exec Summary": "📊",
    "2. Hospitals & Infrastructure": "🏥",
    "3. Regulatory & Compliance": "📜",
    "4. Competitors & Pricing": "⚔️",
    "5. Distribution Channels": "🚚",
    "6. KOLs & Decision-Makers": "🩺",
    "7. Sources & Methodology": "📚",
}

# Regional planning benchmarks used ONLY to fill visible gaps in the
# regional roll-up (never silently substituted into a country's own sheet).
REGIONAL_BENCHMARKS = {
    "prevalence_pmp": 850.0,       # dialysis prevalence, patients per million population, GCC/Levant planning midpoint
    "hd_share_pct": 88.0,          # typical HD share of dialysis patients in the region
    "pd_share_pct": 12.0,          # typical PD share
    "public_bed_share_pct": 65.0,  # typical public-sector share of dialysis capacity
}

COMPETITORS = ["BD / Bard", "Teleflex / Arrow", "Medtronic / Covidien", "AngioDynamics", "Merit Medical"]

# Master competitor intelligence profiles (curated, consistent across all
# 8 country files; used for the interactive competitor drill-down cards).
COMPETITOR_PROFILES = {
    "BD / Bard": {
        "parent": "Becton, Dickinson and Company (NYSE: BDX)",
        "brief": (
            "The dominant global vascular-access brand in dialysis catheters, built on "
            "decades of clinician trust and the widest distribution footprint of any "
            "incumbent in the GCC/Levant. Bard's acute and chronic HD catheter lines are "
            "the default reference point most nephrologists compare new entrants against."
        ),
        "portfolio": [
            "Hickman / Broviac-style tunneled dialysis catheters",
            "PowerHemo and Hemo-Cath acute dual-lumen catheters",
            "PICC lines and broader vascular-access accessories",
            "Introducer / peel-away sheath systems",
        ],
        "strengths": [
            "Strongest brand recognition among nephrologists and interventional radiologists",
            "Deep, multi-country distributor relationships with tender history",
            "Premium clinical evidence base and long track record",
        ],
        "gaps": [
            "Premium pricing makes it vulnerable in liquidity-constrained or tender-driven markets (Lebanon, Jordan)",
            "Longer local switching cycle once a hospital is anchored on Bard — but also slower to react to price-led entrants",
            "Less flexible on GCC-specific bundling/tender structures than smaller challengers",
        ],
        "materials": "Primarily polyurethane for acute lines; premium biocompatible polymers on select chronic tunneled SKUs.",
        "tip_design": "Mostly symmetric-tip designs on legacy chronic lines, split-tip options on newer acute/PICC platforms.",
    },
    "Teleflex / Arrow": {
        "parent": "Teleflex Incorporated (NYSE: TFX)",
        "brief": (
            "Teleflex's Arrow franchise is the strongest acute-CVC and ICU-oriented "
            "competitor in the region, well embedded in critical-care and nephrology "
            "acute-access protocols across MOH and academic medical centers."
        ),
        "portfolio": [
            "Arrow acute triple/dual-lumen hemodialysis catheters",
            "Arrow chronic tunneled dialysis catheters (split-tip)",
            "Central venous catheter (CVC) and introducer kits",
            "Antimicrobial-coated catheter options",
        ],
        "strengths": [
            "Deep penetration into ICU and acute-care protocols",
            "Strong clinical/procedural training support for interventionalists",
            "Broad acute + chronic dual-line presence",
        ],
        "gaps": [
            "Facing sustained pricing pressure in public-sector tenders",
            "Chronic tunneled portfolio is less differentiated than acute lines",
            "Regional supply lead times longer than Egypt-proximate competitors",
        ],
        "materials": "Polyurethane-based acute catheters; Carbothane-class materials on select chronic tunneled lines.",
        "tip_design": "Signature split/staggered-tip design on chronic catheters; symmetric on most acute SKUs.",
    },
    "Medtronic / Covidien": {
        "parent": "Medtronic plc (NYSE: MDT)",
        "brief": (
            "A broad-portfolio medtech giant where vascular access is one line among many. "
            "Regional strength comes from overall distribution muscle and bundled hospital "
            "contracts rather than category-specific specialization."
        ),
        "portfolio": [
            "Acute and chronic HD catheter lines (legacy Covidien)",
            "Vascular access accessories and introducer sets",
            "Broader interventional and surgical device portfolio used as bundling leverage",
        ],
        "strengths": [
            "Very broad hospital-wide distribution and contracting relationships",
            "Can bundle vascular access with other high-value Medtronic categories",
            "Strong regulatory/quality infrastructure",
        ],
        "gaps": [
            "Vascular access is not a top strategic priority within the broader portfolio",
            "Less nephrology-specific KOL engagement than dedicated competitors",
            "Slower product refresh cadence in the catheter line specifically",
        ],
        "materials": "Standard-grade polyurethane across most of the catheter range.",
        "tip_design": "Predominantly symmetric-tip acute and chronic designs; limited staggered-tip options.",
    },
    "AngioDynamics": {
        "parent": "AngioDynamics, Inc. (NASDAQ: ANGO)",
        "brief": (
            "A focused vascular-access specialist with a credible chronic dialysis catheter "
            "line, but a materially smaller regional footprint and distributor network than "
            "the top-two incumbents."
        ),
        "portfolio": [
            "Chronic tunneled dialysis catheters",
            "Acute dialysis catheters",
            "PICC and midline vascular access devices",
        ],
        "strengths": [
            "Genuine access-device specialization (not a bundled afterthought)",
            "Competitive clinical positioning on chronic tunneled design",
        ],
        "gaps": [
            "Smaller regional distributor footprint than BD/Teleflex — real white-space for AMECATH",
            "Less brand recognition among regional nephrologists outside flagship academic centers",
            "Limited local/Arabic-language clinical marketing presence",
        ],
        "materials": "Polyurethane and premium chronic-catheter polymer blends on tunneled SKUs.",
        "tip_design": "Symmetric and staggered-tip variants both offered; protocol-driven selection.",
    },
    "Merit Medical": {
        "parent": "Merit Medical Systems, Inc. (NASDAQ: MMSI)",
        "brief": (
            "Strong in procedural kits and access accessories rather than the catheter itself "
            "as the anchor product — a channel competitor more than a head-on catheter rival."
        ),
        "portfolio": [
            "Dialysis catheter procedural kits and trays",
            "Access accessories (guidewires, dilators, sheaths)",
            "Selective chronic/acute catheter SKUs",
        ],
        "strengths": [
            "Strong kit/accessory bundling that simplifies procurement for hospitals",
            "Good price-to-completeness ratio on procedural trays",
        ],
        "gaps": [
            "Lower brand gravity on the core catheter itself vs. BD/Teleflex/AngioDynamics",
            "Less differentiated material/tip-design story",
            "Weaker standalone nephrology KOL relationships",
        ],
        "materials": "Standard polyurethane across most kit-bundled catheter SKUs.",
        "tip_design": "Primarily symmetric-tip, standard-geometry catheters bundled into procedural kits.",
    },
}


# ---------------------------------------------------------------------------
# Excel parsing
# ---------------------------------------------------------------------------

def _is_blank_row(row) -> bool:
    return all(pd.isna(v) for v in row)


def parse_workbook(path: str | Path) -> dict:
    """
    Parse one AMECATH country workbook into:
        {sheet_name: [(table_title, DataFrame), ...], ...}

    Each sheet follows a consistent layout produced by the AMECATH build
    scripts: page title (row 0), subtitle (row 1), blank spacer (row 2),
    then one or more stacked tables, each introduced by a merged title
    row and separated from the next table by a blank spacer row.
    """
    xls = pd.ExcelFile(path)
    result: dict[str, list[tuple[str, pd.DataFrame]]] = {}

    for sheet in xls.sheet_names:
        raw = pd.read_excel(xls, sheet_name=sheet, header=None)
        rows = raw.values.tolist()
        n = len(rows)
        i = 3  # skip page title / subtitle / spacer
        tables = []

        while i < n:
            if _is_blank_row(rows[i]):
                i += 1
                continue

            title = rows[i][0]
            i += 1
            if i >= n:
                break

            header_row = rows[i]
            headers = [h for h in header_row if not pd.isna(h)]
            i += 1

            data_rows = []
            while i < n and not _is_blank_row(rows[i]):
                data_rows.append(rows[i][: len(headers)])
                i += 1

            df = pd.DataFrame(data_rows, columns=headers)
            tables.append((str(title), df))

        result[sheet] = tables

    return result


def load_all_countries() -> dict:
    """Load and parse every country workbook found in DATA_DIR."""
    out = {}
    for country, filename in COUNTRY_FILES.items():
        path = DATA_DIR / filename
        if path.exists():
            out[country] = parse_workbook(path)
    return out


def get_table(country_data: dict, sheet_name: str, title_contains: str) -> pd.DataFrame | None:
    """Fetch a table from a parsed sheet by a case-insensitive title substring."""
    tables = country_data.get(sheet_name, [])
    needle = title_contains.lower()
    for title, df in tables:
        if needle in title.lower():
            return df
    return None


# ---------------------------------------------------------------------------
# Numeric extraction from free-text metric cells
# ---------------------------------------------------------------------------

_NUM_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)")
_NEGATIVE_MARKERS = ("not publicly verified", "not fully verified", "not retrieved",
                     "not found", "not directly verified", "—")


def extract_first_number(text) -> float | None:
    """Pull the first plausible numeric figure out of a free-text cell."""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None
    s = str(text).strip()
    low = s.lower()
    if any(marker in low for marker in _NEGATIVE_MARKERS):
        return None
    m = _NUM_RE.search(s)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def classify_metric_name(name: str) -> str | None:
    """Bucket a free-text metric label into a standard category."""
    n = str(name).lower()
    if "population" in n and "dialysis" not in n and "patient" not in n:
        return "population"
    if ("hd patient" in n) or ("hd share" in n) or n.strip() == "hd patients":
        return "hd_patients_or_share"
    if ("pd patient" in n) or ("pd share" in n):
        return "pd_patients_or_share"
    if "home hd" in n or "assisted home" in n:
        return "home_hd"
    if (("total" in n or "active" in n) and ("dialysis" in n or "esrd" in n or "rrt" in n)
            and ("patient" in n or "population" in n)):
        return "total_patients"
    if "market size" in n or "addressable market" in n or "market value" in n:
        return "market_size"
    if any(k in n for k in ["dialysis units", "dialysis clinics", "hd centers", "hd units",
                             "dialysis centers / sites"]):
        return "centers"
    if "total" in n and any(k in n for k in ["center", "clinic", "unit"]):
        return "centers"
    if "machine" in n or "station" in n:
        return "machines"
    if "prevalence" in n and "pmp" in n:
        return "prevalence_pmp"
    if "incidence" in n and "pmp" in n:
        return "incidence_pmp"
    return None


def extract_country_kpis(country_data: dict) -> dict:
    """
    Pull a best-effort, clearly-flagged set of headline KPIs out of a
    country's Macro & Exec Summary table. Anything that cannot be parsed
    is left as None rather than guessed.
    """
    kpis = {
        "population": None,
        "total_patients": None,
        "hd_share_pct": None,
        "pd_share_pct": None,
        "centers": None,
        "machines": None,
        "prevalence_pmp": None,
        "market_size_note": None,
        "estimated_total_patients": False,
    }

    macro_table = get_table(country_data, "1. Macro & Exec Summary", "Key Registry")
    if macro_table is None:
        return kpis

    value_col = macro_table.columns[1] if len(macro_table.columns) > 1 else None
    if value_col is None:
        return kpis

    for _, row in macro_table.iterrows():
        metric_name = row.iloc[0]
        value_text = row[value_col]
        bucket = classify_metric_name(metric_name)
        if bucket is None:
            continue
        num = extract_first_number(value_text)

        if bucket == "population" and num is not None:
            kpis["population"] = num
        elif bucket == "total_patients" and num is not None:
            kpis["total_patients"] = num
        elif bucket == "hd_patients_or_share" and num is not None:
            if "%" in str(value_text):
                kpis["hd_share_pct"] = num
        elif bucket == "pd_patients_or_share" and num is not None:
            if "%" in str(value_text):
                kpis["pd_share_pct"] = num
        elif bucket == "centers" and num is not None:
            kpis["centers"] = num
        elif bucket == "machines" and num is not None:
            kpis["machines"] = num
        elif bucket == "prevalence_pmp" and num is not None:
            kpis["prevalence_pmp"] = num
        elif bucket == "market_size" and isinstance(value_text, str):
            kpis["market_size_note"] = value_text

    # Regional-benchmark interpolation ONLY when a figure is genuinely
    # missing, and always flagged so the UI can label it "(estimated)".
    if kpis["total_patients"] is None and kpis["population"] is not None:
        kpis["total_patients"] = kpis["population"] * (REGIONAL_BENCHMARKS["prevalence_pmp"] / 1_000_000.0)
        kpis["estimated_total_patients"] = True

    return kpis


def parse_timeline_days(text) -> float | None:
    """Convert a free-text regulatory timeline (months or working days) to an approximate day count."""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None
    s = str(text).lower()
    m = re.search(r"(\d+)\s*[-–]\s*(\d+)\s*(?:working\s+)?(month|day)", s)
    if not m:
        return None
    lo, hi, unit = int(m.group(1)), int(m.group(2)), m.group(3)
    avg = (lo + hi) / 2.0
    return avg * 30 if unit == "month" else avg


def build_regional_snapshot(all_country_data: dict) -> pd.DataFrame:
    """Build a one-row-per-country snapshot table with extracted KPIs + metadata."""
    rows = []
    for country, data in all_country_data.items():
        kpis = extract_country_kpis(data)
        meta = COUNTRY_META.get(country, {})
        reg_table = get_table(data, "3. Regulatory & Compliance", "Regulatory Blueprint")
        timeline_days = None
        if reg_table is not None and len(reg_table.columns) > 1:
            timeline_row = reg_table[reg_table.iloc[:, 0].astype(str).str.contains("Timeline", case=False, na=False)]
            if not timeline_row.empty:
                timeline_days = parse_timeline_days(timeline_row.iloc[0, 1])

        rows.append({
            "Country": country,
            "Flag": meta.get("flag", ""),
            "Tier": meta.get("tier", ""),
            "Region": meta.get("region", ""),
            "Population": kpis["population"],
            "Total Patients": kpis["total_patients"],
            "Patients Estimated": kpis["estimated_total_patients"],
            "Centers": kpis["centers"],
            "Machines": kpis["machines"],
            "Prevalence (pmp)": kpis["prevalence_pmp"],
            "Reg. Timeline (days, approx.)": timeline_days,
        })
    return pd.DataFrame(rows)


def build_competitor_country_matrix(all_country_data: dict) -> pd.DataFrame:
    """Long-form table of Competitor x Country strengths/weaknesses drawn straight from each country's Competitor Matrix table."""
    rows = []
    for country, data in all_country_data.items():
        comp_table = get_table(data, "4. Competitors & Pricing", "Competitor Matrix")
        if comp_table is None or comp_table.empty:
            continue
        cols = list(comp_table.columns)
        strength_col = cols[1] if len(cols) > 1 else None
        weakness_col = cols[2] if len(cols) > 2 else None
        for _, r in comp_table.iterrows():
            rows.append({
                "Country": country,
                "Competitor": r.iloc[0],
                "Strengths": r[strength_col] if strength_col else "",
                "Weaknesses / Gaps": r[weakness_col] if weakness_col else "",
            })
    return pd.DataFrame(rows)
