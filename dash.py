"""
AMECATH Executive Intelligence Hub — v2.1
========================================
Single-file Streamlit dashboard with updated structured navigation & key mapping.
Data source: Amecath Dash_5.xlsx
"""

import base64
import os
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────
# 0. CONFIGURATION & MAPPING
# ─────────────────────────────────────────────

MASTER_FILE = "Amecath Dash_5.xlsx"

ASSETS_DIR = Path("assets")
LANDSCAPE_DIR = ASSETS_DIR / "landscapes"
LOGO_DIR = ASSETS_DIR / "logos"

# Ordered Required Sheets Mapping
REQUIRED_SHEETS = {
    "overview": "Overview_KPIs",
    "macro": "Macro_Summary",
    "tenders": "Financials_Tenders",
    "hot_areas": "Hot_Areas",
    "competitors": "Competitor_Matrix",
    "competitors_asp": "Competitor_Aspiration",
    "kol": "KOL_Catalog",
    "forecast": "Forecast_Data",
    "sources": "Sources",
}

# Sidebar Navigation Order & Icon Mapping
NAV_MAP = {
    "🌐 Executive Overview": "overview",
    "📊 Macro Environment": "macro",
    "📈 Financials & Tenders": "tenders",
    "🔥 Hot Market Areas": "hot_areas",
    "⚔️ Competitor Matrix": "competitors",
    "🏷️ Competitor ASP & Pricing": "competitors_asp",
    "👨‍⚕️ Key Opinion Leaders": "kol",
    "🔮 Market Forecast": "forecast",
    "📚 Data Sources & Audit": "sources",
}

OVERVIEW_SCHEMA = {
    "country":           str,
    "dialysis_patients": (int, float),
    "market_size_usd_m": (int, float),
    "cagr_pct":          (int, float),
    "top_competitor":    str,
    "amecath_share_pct": (int, float),
    "confidence_score":  (int, float),
    "trend":             str,
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
# 1. STREAMLIT CONFIG & HELPERS
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AMECATH Executive Intelligence Hub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

def _image_to_b64(path: Path) -> str:
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return ""

def find_landscape_b64(country: str) -> str:
    for ext in ("jpeg", "jpg", "png"):
        p = LANDSCAPE_DIR / f"{country} landscape.{ext}"
        b64 = _image_to_b64(p)
        if b64:
            return b64
    matches = list(LANDSCAPE_DIR.glob(f"{country}*landscape*"))
    if matches:
        return _image_to_b64(matches[0])
    return ""

def logo_b64() -> str:
    for ext in ("png", "jpeg", "jpg"):
        b64 = _image_to_b64(LOGO_DIR / f"amecath_logo.{ext}")
        if b64:
            return b64
    return ""

@st.cache_data(ttl=300)
def load_master_data(filepath: str) -> dict[str, pd.DataFrame]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Master data file '{filepath}' not found. "
            f"Place {MASTER_FILE} in the project root."
        )

    xls = pd.ExcelFile(filepath)
    sheets: dict[str, pd.DataFrame] = {}
    for name in xls.sheet_names:
        df = pd.read_excel(filepath, sheet_name=name)
        sheets[name] = df.dropna(how="all").reset_index(drop=True)

    missing = [v for v in REQUIRED_SHEETS.values() if v not in sheets]
    if missing:
        st.warning(
            f"⚠️ Missing sheet(s) in master file: {missing}. "
            "Some sections may display placeholder data or empty views."
        )
    return sheets

def get_sheet(data: dict, key: str) -> Optional[pd.DataFrame]:
    sheet_name = REQUIRED_SHEETS.get(key)
    return data.get(sheet_name)

def inject_css(theme: dict, bg_b64: str = "") -> None:
    bg_css = f"""
    .stApp {{
        background: linear-gradient(rgba(10,15,20,0.78), rgba(10,15,20,0.90)),
                    url("data:image/jpeg;base64,{bg_b64}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}""" if bg_b64 else f".stApp {{ background-color: {theme['bg']} !important; }}"

    st.markdown(f"""
    <style>
    {bg_css}
    body, .stApp {{ color: {theme['text']}; }}
    .country-mini-card {{
        background: {theme['card_bg']};
        border-left: 5px solid {theme['primary']}; border-radius: 10px;
        padding: 16px 18px; margin-bottom: 14px; backdrop-filter: blur(6px);
        box-shadow: 0 3px 10px rgba(0,0,0,0.35);
    }}
    .hero-banner {{
        background: linear-gradient(135deg, {theme['primary']}CC, {theme['card_bg']});
        padding: 20px 25px; border-radius: 15px; border-left: 6px solid {theme['accent']};
        margin-bottom: 25px; backdrop-filter: blur(8px); box-shadow: 0 6px 18px rgba(0,0,0,0.4);
    }}
    .header-container {{ display: flex; align-items: center; gap: 15px; }}
    .header-title {{ color: white; margin: 0; font-size: 26px; font-weight: bold; }}
    .forecast-frame {{
        background: {theme['card_bg']}; border: 1px solid {theme['accent']};
        border-radius: 12px; padding: 18px; backdrop-filter: blur(6px);
    }}
    </style>
    """, unsafe_allow_html=True)

def render_hero(country: str, theme: dict) -> None:
    flag_html = f'<span style="font-size:36px;">{theme["flag"]}</span>'
    logo = logo_b64()
    logo_html = (
        f'<img src="data:image/png;base64,{logo}" style="height:48px;margin-left:auto;" alt="AMECATH logo">'
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
# 2. SECTION RENDERERS
# ─────────────────────────────────────────────

def render_generic_table(data: dict, key: str, title: str, country: str) -> None:
    st.subheader(f"{title} — {country}")
    df = get_sheet(data, key)
    if df is not None and not df.empty:
        if "country" in df.columns:
            df = df[df["country"].str.strip().str.lower() == country.lower()]
        st.dataframe(df, use_container_width=True)
    else:
        st.info(f"No data available in sheet '{REQUIRED_SHEETS.get(key)}' for {country}.")

def render_overview(data: dict, theme: dict) -> None:
    st.subheader("🌐 Regional Overview — All Markets at a Glance")
    df_ov = get_sheet(data, "overview")
    if df_ov is None or df_ov.empty:
        st.info("Overview data not available.")
        return

    total_patients = df_ov["dialysis_patients"].sum() if "dialysis_patients" in df_ov.columns else 0
    total_market = df_ov["market_size_usd_m"].sum() if "market_size_usd_m" in df_ov.columns else 0
    avg_cagr = df_ov["cagr_pct"].mean() if "cagr_pct" in df_ov.columns else 0
    avg_share = df_ov["amecath_share_pct"].mean() if "amecath_share_pct" in df_ov.columns else 0

    k1, k2, k3, k4, k5 = st.columns(5)
    kpi_style = f"background:{theme['card_bg']};border:1px solid {theme['primary']}; border-radius:10px;padding:14px;text-align:center;"
    for col, label, value in [
        (k1, "Markets Covered", f"{len(df_ov)}"),
        (k2, "Total Dialysis Patients", f"{total_patients:,.0f}"),
        (k3, "Total Addressable Market", f"${total_market:,.1f}M"),
        (k4, "Avg. Market CAGR", f"{avg_cagr:.1f}%"),
        (k5, "Avg. AMECATH Share", f"{avg_share:.1f}%"),
    ]:
        col.markdown(
            f'<div style="{kpi_style}">'
            f'<div style="font-size:11px;opacity:.7;margin-bottom:4px;">{label}</div>'
            f'<div style="font-size:22px;font-weight:bold;color:{theme["accent"]}">{value}</div>'
            f'</div>', unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Country Snapshots")
    rows = [df_ov.iloc[i:i+3] for i in range(0, len(df_ov), 3)]

    for row_group in rows:
        cols = st.columns(3)
        for col, (_, row) in zip(cols, row_group.iterrows()):
            country = row.get("country", "—")
            patients = row.get("dialysis_patients", 0)
            mkt = row.get("market_size_usd_m", 0)
            cagr = row.get("cagr_pct", 0)
            share = row.get("amecath_share_pct", 0)
            trend = str(row.get("trend", "stable")).lower()
            top_comp = row.get("top_competitor", "—")
            
            c_theme = COUNTRY_THEMES.get(country, COUNTRY_THEMES["Saudi Arabia"])
            flag = c_theme["flag"]
            t_icon = TREND_ICONS.get(trend, "◆")
            t_color = TREND_COLORS.get(trend, "#FFD600")

            col.markdown(f"""
            <div class="country-mini-card" style="border-left-color:{c_theme['primary']};">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:20px;font-weight:bold;">{flag} {country}</div>
                <div style="color:{t_color};font-size:20px;">{t_icon}</div>
              </div>
              <hr style="border-color:{c_theme['primary']}33;margin:8px 0;">
              <table style="width:100%;font-size:13px;border-collapse:collapse;">
                <tr><td style="opacity:.7;">Dialysis Patients</td><td style="text-align:right;font-weight:bold;">{patients:,.0f}</td></tr>
                <tr><td style="opacity:.7;">Market Size</td><td style="text-align:right;font-weight:bold;">${mkt:,.1f}M</td></tr>
                <tr><td style="opacity:.7;">CAGR</td><td style="text-align:right;font-weight:bold;color:{t_color};">{cagr:.1f}%</td></tr>
                <tr><td style="opacity:.7;">AMECATH Share</td><td style="text-align:right;font-weight:bold;">{share:.1f}%</td></tr>
                <tr><td style="opacity:.7;">Top Competitor</td><td style="text-align:right;font-style:italic;">{top_comp}</td></tr>
              </table>
            </div>""", unsafe_allow_html=True)

def render_forecast(data: dict, selected_country: str, theme: dict) -> None:
    st.subheader(f"🔮 Market Forecast — {selected_country}")
    df_fc = get_sheet(data, "forecast")
    if df_fc is None or df_fc.empty:
        st.info("Forecast data sheet not available.")
        return

    df_c = df_fc[df_fc["country"].str.strip().str.lower() == selected_country.lower()].copy()
    if df_c.empty:
        st.warning(f"No forecast records found for {selected_country}.")
        return

    metrics = df_c["metric"].unique().tolist() if "metric" in df_c.columns else []
    scenarios = df_c["scenario"].unique().tolist() if "scenario" in df_c.columns else []

    col_m, col_s = st.columns([2, 1])
    selected_metric = col_m.selectbox("📊 Metric", metrics, key="fc_metric") if metrics else None
    selected_scenario = col_s.selectbox("🎯 Scenario", scenarios, key="fc_scenario") if scenarios else None

    df_plot = df_c
    if selected_metric:
        df_plot = df_plot[df_plot["metric"] == selected_metric]
    if selected_scenario:
        df_plot = df_plot[df_plot["scenario"] == selected_scenario]

    if df_plot.empty:
        st.info("No forecast values available for selected parameters.")
        return

    df_plot = df_plot.sort_values("year")
    st.markdown('<div class="forecast-frame">', unsafe_allow_html=True)
    st.line_chart(df_plot.set_index("year")["value"], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. SIDEBAR NAVIGATION & ROUTING
# ─────────────────────────────────────────────

st.sidebar.markdown("## 🩺 AMECATH Intelligence")
st.sidebar.markdown("---")

selected_country = st.sidebar.selectbox("🌍 Select Target Country / Market", list(COUNTRY_THEMES.keys()))
theme = COUNTRY_THEMES[selected_country]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Navigation")
selected_nav_label = st.sidebar.radio("Go to Section", list(NAV_MAP.keys()))
nav_mode = NAV_MAP[selected_nav_label]

st.sidebar.markdown("---")
st.sidebar.caption(
    f"Data File: `{MASTER_FILE}`  \n"
    f"Active Mode: `{nav_mode}`  \n"
    f"Version: 2.1"
)

# ─────────────────────────────────────────────
# 4. APP ENTRY & ROUTING
# ─────────────────────────────────────────────

bg_b64 = find_landscape_b64(selected_country)
inject_css(theme, bg_b64)
render_hero(selected_country, theme)

try:
    data_sheets = load_master_data(MASTER_FILE)
except FileNotFoundError as exc:
    st.error(str(exc))
    st.stop()

# Execution Routing Map
if nav_mode == "overview":
    render_overview(data_sheets, theme)
elif nav_mode == "macro":
    render_generic_table(data_sheets, "macro", "📊 Macro Environment", selected_country)
elif nav_mode == "tenders":
    render_generic_table(data_sheets, "tenders", "📈 Financials & Tenders", selected_country)
elif nav_mode == "hot_areas":
    render_generic_table(data_sheets, "hot_areas", "🔥 Hot Market Areas", selected_country)
elif nav_mode == "competitors":
    render_generic_table(data_sheets, "competitors", "⚔️ Competitor Matrix", selected_country)
elif nav_mode == "competitors_asp":
    render_generic_table(data_sheets, "competitors_asp", "🏷️ Competitor ASP & Pricing", selected_country)
elif nav_mode == "kol":
    render_generic_table(data_sheets, "kol", "👨‍⚕️ Key Opinion Leaders", selected_country)
elif nav_mode == "forecast":
    render_forecast(data_sheets, selected_country, theme)
elif nav_mode == "sources":
    render_generic_table(data_sheets, "sources", "📚 Data Sources & Audit", selected_country)
