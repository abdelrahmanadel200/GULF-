"""
AMECATH Executive Intelligence Hub — v2
========================================
Single-file Streamlit dashboard with:
  - Single-file data source (AMECATH_Dash.xlsx)
  - Overview tab (9-country consolidated KPI panel + mini-cards)
  - Forecast tab (trend projections per country)
  - All original tabs preserved

Repository layout expected:
  amecath_dashboard/
  ├── dash_v2.py                  ← this file
  ├── AMECATH_Dash.xlsx    ← single source of truth
  ├── assets/
  │   ├── logos/
  │   │   └── amecath_logo.png
  │   └── landscapes/
  │       ├── Saudi Arabia landscape.jpeg
  │       ├── UAE landscape.jpeg
  │       ├── Qatar landscape.jpeg
  │       ├── Kuwait landscape.jpeg
  │       ├── Oman landscape.jpeg
  │       ├── Bahrain landscape.jpeg
  │       ├── Jordan landscape.jpeg
  │       └── Lebanon landscape.jpeg
  └── requirements.txt
"""

import base64
import glob
import os
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────
# 0. CONFIGURATION
# ─────────────────────────────────────────────

# Single master data file — all countries in one workbook
MASTER_FILE = "AMECATH_Master_Data.xlsx"

# Assets directory (images committed to the repo)
ASSETS_DIR = Path("assets")
LANDSCAPE_DIR = ASSETS_DIR / "landscapes"
LOGO_DIR = ASSETS_DIR / "logos"

# Required sheets and their canonical names in the master file
REQUIRED_SHEETS = {
    "overview":    "Overview_KPIs",       # consolidated 9-country metrics
    "macro":       "Macro_Summary",       # country macro data (country column required)
    "questions":   "7_Questions_Summary", # strategic Q&A
    "hospitals":   "Hospitals_Infra",     # facility data
    "competitors": "Competitor_Matrix",   # competitor table
    "financials":  "Financials_Tenders",  # tender/financial projections
    "forecast":    "Forecast_Data",       # forecast series per country
}

# Expected columns in Overview_KPIs sheet
OVERVIEW_SCHEMA = {
    "country":           str,
    "dialysis_patients": (int, float),
    "market_size_usd_m": (int, float),
    "cagr_pct":          (int, float),
    "top_competitor":    str,
    "amecath_share_pct": (int, float),
    "confidence_score":  (int, float),   # 0–100
    "trend":             str,            # "up" | "down" | "stable"
    "last_updated":      str,
}

COUNTRY_THEMES = {
    "Saudi Arabia": {"flag": "🇸🇦", "primary": "#006C35", "accent": "#C5A059",
                     "bg": "#0D1B1E", "card_bg": "rgba(19,42,47,0.85)", "text": "#E6F1FF",
                     "landmark": "Kingdom Centre & Riyadh Skyline"},
    "UAE":          {"flag": "🇦🇪", "primary": "#CE1126", "accent": "#00732F",
                     "bg": "#1A0F10", "card_bg": "rgba(42,22,24,0.85)",  "text": "#FFFFFF",
                     "landmark": "Burj Khalifa & Dubai Skyline"},
    "Qatar":        {"flag": "🇶🇦", "primary": "#8A1538", "accent": "#E0A96D",
                     "bg": "#1C0D12", "card_bg": "rgba(46,21,30,0.85)",  "text": "#FFF5F5",
                     "landmark": "Doha Corniche & Museum of Islamic Art"},
    "Kuwait":       {"flag": "🇰🇼", "primary": "#007A3D", "accent": "#CE1126",
                     "bg": "#0A1816", "card_bg": "rgba(17,41,37,0.85)",  "text": "#E6FFFA",
                     "landmark": "Kuwait Towers"},
    "Oman":         {"flag": "🇴🇲", "primary": "#DB162F", "accent": "#008000",
                     "bg": "#1C0D10", "card_bg": "rgba(46,22,26,0.85)",  "text": "#FFF0F0",
                     "landmark": "Al Alam Palace & Muscat Forts"},
    "Bahrain":      {"flag": "🇧🇭", "primary": "#CE1126", "accent": "#FFFFFF",
                     "bg": "#1A0F10", "card_bg": "rgba(42,22,24,0.85)",  "text": "#FFFFFF",
                     "landmark": "Bahrain World Trade Center"},
    "Jordan":       {"flag": "🇯🇴", "primary": "#000000", "accent": "#CE1126",
                     "bg": "#121212", "card_bg": "rgba(31,31,31,0.85)",  "text": "#F5F5F5",
                     "landmark": "Petra & Amman Citadel"},
    "Lebanon":      {"flag": "🇱🇧", "primary": "#CE1126", "accent": "#007A3D",
                     "bg": "#1A0D0D", "card_bg": "rgba(43,22,22,0.85)",  "text": "#FFF0F0",
                     "landmark": "Jeita Grotto & Beirut Skyline"},
    "Egypt":        {"flag": "🇪🇬", "primary": "#C8102E", "accent": "#C09300",
                     "bg": "#1A110C", "card_bg": "rgba(43,28,18,0.85)",  "text": "#FFF8F0",
                     "landmark": "Pyramids of Giza & Cairo Skyline"},
}

TREND_ICONS = {"up": "▲", "down": "▼", "stable": "◆"}
TREND_COLORS = {"up": "#00C853", "down": "#FF1744", "stable": "#FFD600"}


# ─────────────────────────────────────────────
# 1. STREAMLIT PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AMECATH Executive Intelligence Hub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────
# 2. IMAGE HELPERS
# ─────────────────────────────────────────────

def _image_to_b64(path: Path) -> str:
    """Return base64 string for a local image file, or '' if not found."""
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return ""


def find_landscape_b64(country: str) -> str:
    """Search assets/landscapes/ for <Country> landscape.* (jpeg/jpg/png)."""
    for ext in ("jpeg", "jpg", "png"):
        p = LANDSCAPE_DIR / f"{country} landscape.{ext}"
        b64 = _image_to_b64(p)
        if b64:
            return b64
    # Fallback: glob with any capitalisation
    matches = list(LANDSCAPE_DIR.glob(f"{country}*landscape*"))
    if matches:
        return _image_to_b64(matches[0])
    return ""


def logo_b64() -> str:
    """Return AMECATH logo as base64, or '' if not present."""
    for ext in ("png", "jpeg", "jpg"):
        b64 = _image_to_b64(LOGO_DIR / f"amecath_logo.{ext}")
        if b64:
            return b64
    return ""


# ─────────────────────────────────────────────
# 3. DATA LOADING — SINGLE FILE
# ─────────────────────────────────────────────

@st.cache_data(ttl=300)   # re-reads file every 5 minutes (live-update friendly)
def load_master_data(filepath: str) -> dict[str, pd.DataFrame]:
    """
    Load all sheets from the master Excel file.
    Returns a dict {sheet_name: DataFrame}.
    Raises FileNotFoundError if the file is missing.
    Logs a warning for any expected sheet that is absent.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Master data file '{filepath}' not found. "
            "Place AMECATH_Master_Data.xlsx in the project root."
        )

    xls = pd.ExcelFile(filepath)
    sheets: dict[str, pd.DataFrame] = {}
    for name in xls.sheet_names:
        df = pd.read_excel(filepath, sheet_name=name)
        # Drop completely empty rows
        sheets[name] = df.dropna(how="all").reset_index(drop=True)

    # Warn about missing expected sheets
    missing = [v for v in REQUIRED_SHEETS.values() if v not in sheets]
    if missing:
        st.warning(
            f"⚠️ Expected sheet(s) not found in master file: {missing}. "
            "Some sections may be unavailable."
        )
    return sheets


def validate_overview_schema(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Check that Overview_KPIs contains required columns.
    Returns (is_valid, list_of_issues).
    """
    issues = []
    for col, expected_type in OVERVIEW_SCHEMA.items():
        if col not in df.columns:
            issues.append(f"Missing column: '{col}'")
    return (len(issues) == 0, issues)


def get_sheet(data: dict, key: str) -> Optional[pd.DataFrame]:
    """Safely retrieve a sheet by its canonical key from REQUIRED_SHEETS."""
    sheet_name = REQUIRED_SHEETS.get(key)
    return data.get(sheet_name)


# ─────────────────────────────────────────────
# 4. CSS INJECTION
# ─────────────────────────────────────────────

def inject_css(theme: dict, bg_b64: str = "") -> None:
    if bg_b64:
        bg_css = f"""
        .stApp {{
            background: linear-gradient(rgba(10,15,20,0.78), rgba(10,15,20,0.90)),
                        url("data:image/jpeg;base64,{bg_b64}") no-repeat center center fixed !important;
            background-size: cover !important;
        }}"""
    else:
        bg_css = f".stApp {{ background-color: {theme['bg']} !important; }}"

    st.markdown(f"""
    <style>
    {bg_css}
    body, .stApp {{ color: {theme['text']}; }}

    /* ── Metric cards ── */
    .metric-card {{
        background: {theme['card_bg']};
        border: 1px solid {theme['primary']};
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        text-align: center;
        backdrop-filter: blur(6px);
    }}

    /* ── Country mini-cards (Overview tab) ── */
    .country-mini-card {{
        background: {theme['card_bg']};
        border-left: 5px solid {theme['primary']};
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 14px;
        backdrop-filter: blur(6px);
        box-shadow: 0 3px 10px rgba(0,0,0,0.35);
        transition: border-color 0.2s;
    }}
    .country-mini-card:hover {{ border-left-color: {theme['accent']}; }}

    /* ── Hero banner ── */
    .hero-banner {{
        background: linear-gradient(135deg, {theme['primary']}CC, {theme['card_bg']});
        padding: 20px 25px;
        border-radius: 15px;
        border-left: 6px solid {theme['accent']};
        margin-bottom: 25px;
        backdrop-filter: blur(8px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.4);
    }}
    .header-container {{ display: flex; align-items: center; gap: 15px; }}
    .header-flag {{
        width: 60px; height: 40px; object-fit: cover;
        border-radius: 6px; border: 2px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.6);
    }}
    .header-title {{ color: white; margin: 0; font-size: 26px; font-weight: bold; }}

    /* ── Competitor cards ── */
    .competitor-card {{
        background: {theme['card_bg']};
        border-left: 4px solid {theme['accent']};
        padding: 15px; border-radius: 8px;
        margin-bottom: 10px; backdrop-filter: blur(6px);
    }}

    /* ── KPI summary strip ── */
    .kpi-strip {{
        background: linear-gradient(90deg, {theme['primary']}44, {theme['card_bg']});
        border: 1px solid {theme['primary']};
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(6px);
    }}

    /* ── Forecast chart frame ── */
    .forecast-frame {{
        background: {theme['card_bg']};
        border: 1px solid {theme['accent']};
        border-radius: 12px;
        padding: 18px;
        backdrop-filter: blur(6px);
    }}

    /* ── Trend pill ── */
    .trend-up   {{ color: #00C853; font-weight: bold; }}
    .trend-down {{ color: #FF1744; font-weight: bold; }}
    .trend-stable {{ color: #FFD600; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 5. HERO HEADER
# ─────────────────────────────────────────────

def render_hero(country: str, theme: dict) -> None:
    flag_html = f'<span style="font-size:36px;">{theme["flag"]}</span>'
    logo = logo_b64()
    logo_html = (
        f'<img src="data:image/png;base64,{logo}" '
        f'style="height:48px;margin-left:auto;" alt="AMECATH logo">'
        if logo else ""
    )
    st.markdown(f"""
    <div class="hero-banner">
      <div class="header-container">
        {flag_html}
        <h1 class="header-title">{country.upper()} — EXECUTIVE MARKET DOSSIER</h1>
        {logo_html}
      </div>
      <p style="color:{theme['accent']};font-size:15px;margin-top:10px;margin-bottom:0;">
        Strategic Landmark: <b>{theme['landmark']}</b>
      </p>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 6. OVERVIEW TAB
# ─────────────────────────────────────────────

def render_overview(data: dict, theme: dict) -> None:
    """
    Consolidated 9-country overview:
      • Summary KPI strip (totals / averages across all countries)
      • Per-country mini-cards with key metrics
    Reads from Overview_KPIs sheet.
    """
    st.subheader("🌍 Regional Overview — All Markets at a Glance")

    df_ov = get_sheet(data, "overview")
    if df_ov is None:
        st.info(
            "Overview data not found. Ensure the master file contains "
            f"a sheet named '{REQUIRED_SHEETS['overview']}' "
            "with columns: country, dialysis_patients, market_size_usd_m, "
            "cagr_pct, top_competitor, amecath_share_pct, confidence_score, trend."
        )
        return

    valid, issues = validate_overview_schema(df_ov)
    if not valid:
        st.error("Overview schema issues — check the master file:\n" + "\n".join(issues))
        return

    # ── Summary KPI strip ──────────────────────────────────────────
    total_patients  = df_ov["dialysis_patients"].sum()
    total_market    = df_ov["market_size_usd_m"].sum()
    avg_cagr        = df_ov["cagr_pct"].mean()
    avg_share       = df_ov["amecath_share_pct"].mean()
    n_countries     = len(df_ov)

    k1, k2, k3, k4, k5 = st.columns(5)
    kpi_style = f"background:{theme['card_bg']};border:1px solid {theme['primary']};" \
                f"border-radius:10px;padding:14px;text-align:center;"
    for col, label, value in [
        (k1, "Markets Covered",       f"{n_countries}"),
        (k2, "Total Dialysis Patients", f"{total_patients:,.0f}"),
        (k3, "Total Addressable Market", f"${total_market:,.1f}M"),
        (k4, "Avg. Market CAGR",       f"{avg_cagr:.1f}%"),
        (k5, "Avg. AMECATH Share",     f"{avg_share:.1f}%"),
    ]:
        col.markdown(
            f'<div style="{kpi_style}">'
            f'<div style="font-size:11px;opacity:.7;margin-bottom:4px;">{label}</div>'
            f'<div style="font-size:22px;font-weight:bold;color:{theme["accent"]}">{value}</div>'
            f'</div>', unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Per-country mini-cards (3 columns) ────────────────────────
    st.markdown("### Country Snapshots")
    rows = [df_ov.iloc[i:i+3] for i in range(0, len(df_ov), 3)]

    for row_group in rows:
        cols = st.columns(3)
        for col, (_, row) in zip(cols, row_group.iterrows()):
            country    = row.get("country", "—")
            patients   = row.get("dialysis_patients", 0)
            mkt        = row.get("market_size_usd_m", 0)
            cagr       = row.get("cagr_pct", 0)
            share      = row.get("amecath_share_pct", 0)
            confidence = row.get("confidence_score", 0)
            trend      = str(row.get("trend", "stable")).lower()
            updated    = row.get("last_updated", "—")
            top_comp   = row.get("top_competitor", "—")
            c_theme    = COUNTRY_THEMES.get(country, COUNTRY_THEMES["Saudi Arabia"])
            flag       = c_theme["flag"]
            t_icon     = TREND_ICONS.get(trend, "◆")
            t_color    = TREND_COLORS.get(trend, "#FFD600")

            col.markdown(f"""
            <div class="country-mini-card" style="border-left-color:{c_theme['primary']};">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:20px;font-weight:bold;">{flag} {country}</div>
                <div style="color:{t_color};font-size:20px;">{t_icon}</div>
              </div>
              <hr style="border-color:{c_theme['primary']}33;margin:8px 0;">
              <table style="width:100%;font-size:13px;border-collapse:collapse;">
                <tr>
                  <td style="opacity:.7;">Dialysis Patients</td>
                  <td style="text-align:right;font-weight:bold;">{patients:,.0f}</td>
                </tr>
                <tr>
                  <td style="opacity:.7;">Market Size</td>
                  <td style="text-align:right;font-weight:bold;">${mkt:,.1f}M</td>
                </tr>
                <tr>
                  <td style="opacity:.7;">CAGR</td>
                  <td style="text-align:right;font-weight:bold;color:{t_color};">{cagr:.1f}%</td>
                </tr>
                <tr>
                  <td style="opacity:.7;">AMECATH Share</td>
                  <td style="text-align:right;font-weight:bold;">{share:.1f}%</td>
                </tr>
                <tr>
                  <td style="opacity:.7;">Top Competitor</td>
                  <td style="text-align:right;font-style:italic;">{top_comp}</td>
                </tr>
                <tr>
                  <td style="opacity:.7;">Confidence</td>
                  <td style="text-align:right;">
                    <div style="background:#ffffff22;border-radius:4px;height:8px;width:80px;display:inline-block;vertical-align:middle;">
                      <div style="background:{c_theme['accent']};height:8px;border-radius:4px;width:{min(confidence,100)}%;"></div>
                    </div>
                    <span style="margin-left:6px;">{confidence:.0f}%</span>
                  </td>
                </tr>
              </table>
              <div style="font-size:10px;opacity:.5;margin-top:8px;">Updated: {updated}</div>
            </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 7. FORECAST TAB
# ─────────────────────────────────────────────

def render_forecast(data: dict, selected_country: str, theme: dict) -> None:
    """
    Forecast tab: reads Forecast_Data sheet filtered by country.
    Expected columns: country, year, metric, value, scenario (Base/Bull/Bear).
    """
    st.subheader(f"📈 Market Forecast — {selected_country}")

    df_fc = get_sheet(data, "forecast")
    if df_fc is None:
        st.info(
            "Forecast data not available. Add a sheet named "
            f"'{REQUIRED_SHEETS['forecast']}' with columns: "
            "country, year, metric, value, scenario."
        )
        return

    # Filter to selected country
    df_c = df_fc[df_fc["country"].str.strip() == selected_country].copy()
    if df_c.empty:
        st.warning(f"No forecast data found for {selected_country}.")
        return

    metrics = df_c["metric"].unique().tolist() if "metric" in df_c.columns else []
    scenarios = df_c["scenario"].unique().tolist() if "scenario" in df_c.columns else []

    col_m, col_s = st.columns([2, 1])
    selected_metric   = col_m.selectbox("📊 Metric", metrics, key="fc_metric")
    selected_scenario = col_s.selectbox("🎯 Scenario", scenarios, key="fc_scenario")

    df_plot = df_c[
        (df_c["metric"] == selected_metric) &
        (df_c["scenario"] == selected_scenario)
    ].sort_values("year")

    if df_plot.empty:
        st.info("No data for this metric / scenario combination.")
        return

    # Render chart using Streamlit native (no extra deps)
    st.markdown(f'<div class="forecast-frame">', unsafe_allow_html=True)
    st.line_chart(df_plot.set_index("year")["value"], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Insight cards below chart
    st.markdown("#### 🔍 Key Forecast Insights")
    last_val  = df_plot["value"].iloc[-1]
    first_val = df_plot["value"].iloc[0]
    growth    = ((last_val - first_val) / first_val * 100) if first_val else 0
    peak_year = df_plot.loc[df_plot["value"].idxmax(), "year"]

    i1, i2, i3 = st.columns(3)
    card = lambda label, val: (
        f'<div class="metric-card"><div style="font-size:11px;opacity:.7">{label}</div>'
        f'<div style="font-size:20px;font-weight:bold;color:{theme["accent"]}">{val}</div></div>'
    )
    i1.markdown(card("Projected Growth", f"{growth:+.1f}%"), unsafe_allow_html=True)
    i2.markdown(card("Peak Year",  str(peak_year)), unsafe_allow_html=True)
    i3.markdown(card("Final Value", f"{last_val:,.0f}"), unsafe_allow_html=True)

    with st.expander("📋 Raw Forecast Data"):
        st.dataframe(df_plot, use_container_width=True)


# ─────────────────────────────────────────────
# 8. ORIGINAL SECTION RENDERERS
# ─────────────────────────────────────────────

def render_macro(data: dict, country: str) -> None:
    st.subheader(f"📊 Macro & Executive Summary — {country}")
    df = get_sheet(data, "macro")
    if df is not None:
        # Filter to country if column exists
        if "country" in df.columns:
            df = df[df["country"].str.strip() == country]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Macro summary data not available.")


def render_questions(data: dict, country: str) -> None:
    st.subheader(f"📋 Strategic 7 Questions Summary — {country}")
    df = get_sheet(data, "questions")
    if df is not None:
        if "country" in df.columns:
            df = df[df["country"].str.strip() == country]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("7 Questions data not available.")


def render_hospitals(data: dict, country: str) -> None:
    st.subheader(f"🏥 Hospitals & Renal Infrastructure — {country}")
    df = get_sheet(data, "hospitals")
    if df is not None:
        if "country" in df.columns:
            df = df[df["country"].str.strip() == country]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Infrastructure data not available.")


def render_competitors(data: dict, country: str, theme: dict) -> None:
    st.subheader(f"⚔️ Competitor Matrix — {country}")
    df = get_sheet(data, "competitors")

    competitors_list = [
        "BD / Bard", "Teleflex / Arrow", "Medtronic / Covidien",
        "AngioDynamics", "Merit Medical",
    ]
    if "selected_competitor" not in st.session_state:
        st.session_state.selected_competitor = competitors_list[0]

    cols = st.columns(len(competitors_list))
    for idx, comp_name in enumerate(competitors_list):
        if cols[idx].button(comp_name, key=f"btn_{idx}", use_container_width=True):
            st.session_state.selected_competitor = comp_name

    st.markdown("---")
    st.markdown(f"### 🔍 Deep-Dive: **{st.session_state.selected_competitor}**")
    c1, c2 = st.columns(2)
    _comp_card = lambda title, body: (
        f'<div class="competitor-card"><h4>{title}</h4>{body}</div>'
    )
    c1.markdown(_comp_card(
        "📌 Strategic Profile",
        f"<p><b>Focus:</b> Vascular Access & Dialysis Catheters</p>"
        f"<p><b>Market Standing:</b> Key incumbent in {country}.</p>"
        f"<p><b>Pricing:</b> Premium tier with long-term tender history.</p>"
    ), unsafe_allow_html=True)
    c2.markdown(_comp_card(
        "⚡ Strengths & Gaps",
        "<p><b>Strengths:</b> High brand recognition among nephrologists.</p>"
        "<p><b>Gaps:</b> Rigid bundle pricing; slow tender renewal cycles.</p>"
        "<p><b>AMECATH Opportunity:</b> Carbothane biocompatibility + agile supply terms.</p>"
    ), unsafe_allow_html=True)

    if df is not None:
        st.markdown("---")
        st.markdown("### Full Competitor Matrix")
        if "country" in df.columns:
            df = df[df["country"].str.strip() == country]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Competitor matrix data not available.")


def render_financials(data: dict, country: str, theme: dict) -> None:
    st.subheader(f"📈 Financial Projections & Tenders — {country}")
    st.markdown(f"""
    <div class="metric-card">
        <h3>2025 Addressable Market & Tender Outlook</h3>
        <p>Market sizing, catheter consumption forecasts, and pricing benchmarks for <b>{country}</b>.</p>
    </div>""", unsafe_allow_html=True)
    df = get_sheet(data, "financials")
    if df is not None:
        if "country" in df.columns:
            df = df[df["country"].str.strip() == country]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Financial / tenders data not available.")


# ─────────────────────────────────────────────
# 9. SIDEBAR
# ─────────────────────────────────────────────

st.sidebar.markdown("## 🩺 AMECATH Executive Intelligence")
st.sidebar.markdown("---")

selected_country = st.sidebar.selectbox(
    "🌍 Select Target Country / Market",
    list(COUNTRY_THEMES.keys())
)
theme = COUNTRY_THEMES[selected_country]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Navigation")
nav_mode = st.sidebar.radio("Go to Section", [
    "🌐 Overview",
    "📊 Macro & Exec Summary",
    "📋 7 Questions Summary",
    "🏥 Hospitals & Infrastructure",
    "⚔️ Competitors & Pricing",
    "📈 Financials & Tenders",
    "🔮 Forecast",
])

st.sidebar.markdown("---")
st.sidebar.caption(
    f"Data source: `{MASTER_FILE}`  \n"
    f"Cache TTL: 5 min  \n"
    f"Version: 2.0"
)


# ─────────────────────────────────────────────
# 10. APPLY THEMING & LOAD DATA
# ─────────────────────────────────────────────

bg_b64 = find_landscape_b64(selected_country)
inject_css(theme, bg_b64)
render_hero(selected_country, theme)

# Load data with error boundary
try:
    data_sheets = load_master_data(MASTER_FILE)
except FileNotFoundError as exc:
    st.error(str(exc))
    st.info(
        "**Quick fix:** Place `AMECATH_Master_Data.xlsx` in the same directory "
        "as `dash_v2.py`, then refresh the page."
    )
    st.stop()


# ─────────────────────────────────────────────
# 11. SECTION ROUTING
# ─────────────────────────────────────────────

if nav_mode == "🌐 Overview":
    render_overview(data_sheets, theme)

elif nav_mode == "📊 Macro & Exec Summary":
    render_macro(data_sheets, selected_country)

elif nav_mode == "📋 7 Questions Summary":
    render_questions(data_sheets, selected_country)

elif nav_mode == "🏥 Hospitals & Infrastructure":
    render_hospitals(data_sheets, selected_country)

elif nav_mode == "⚔️ Competitors & Pricing":
    render_competitors(data_sheets, selected_country, theme)

elif nav_mode == "📈 Financials & Tenders":
    render_financials(data_sheets, selected_country, theme)

elif nav_mode == "🔮 Forecast":
    render_forecast(data_sheets, selected_country, theme)
