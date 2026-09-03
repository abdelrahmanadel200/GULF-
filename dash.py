"""
AMECATH Executive Intelligence Hub — v2.2 (Ultra-Resilient Edition)
===================================================================
Single-file Streamlit dashboard with dynamic file resolution, 
fuzzy sheet matching, resilient column detection, and rich UI cards.
"""

import base64
import os
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd
import streamlit as st

import re
import plotly.express as px

# ─────────────────────────────────────────────
# 0. CONFIGURATION & MAPPINGS
# ─────────────────────────────────────────────

PRIMARY_FILE = "Amecath Dash_5.xlsx"
FALLBACK_FILES = ["Amecath Dash.xlsx", "amecath_dash.xlsx", "data.xlsx"]

ASSETS_DIR = Path("assets")
LANDSCAPE_DIR = ASSETS_DIR / "landscapes"
LOGO_DIR = ASSETS_DIR / "logos"

# Flexible Sheet Alias Mapping (Maps internal keys to list of candidate tab names)
REQUIRED_SHEETS: Dict[str, List[str]] = {
    "overview": ["Overview_KPIs", "overview", "Overview", "kpi_overview"],
    "macro": ["Macro_Summary", "macro", "Macro", "macro_environment"],
    "tenders": ["Financials_Tenders", "tenders", "Tenders", "financials"],
    "hot_areas": ["Hot_Areas", "Hot Areas", "hot_areas", "HotMarkets"],
    "distributors": ["Local_Distributors", "Distributors", "distributors", "distributor_network"],
    "competitors": ["Competitor_Matrix", "COMPETITORS", "competitors", "Competitors"],
    "competitors_asp": ["Competitor_Aspiration", "comp asp", "competitors_asp", "ASP_Pricing"],
    "kol": ["KOL_Catalog", "KOLS", "kol", "KeyOpinionLeaders"],
    "forecast": ["Forecast_Data", "Revenue Forecast", "forecast", "Forecast"],
    "sources": ["Sources", "sources", "Audit_Sources"],
}

# Sidebar Navigation Map
NAV_MAP: Dict[str, str] = {
    "🌐 Executive Overview": "overview",
    "📊 Macro Environment": "macro",
    "📈 Financials & Tenders": "tenders",
    "🔥 Hot Market Areas": "hot_areas",
    "🤝 Local Distributors": "distributors",
    "⚔️ Competitor Matrix": "competitors",
    "🏷️ Competitor ASP & Pricing": "competitors_asp",
    "👨‍⚕️ Key Opinion Leaders": "kol",
    "🔮 Market Forecast": "forecast",
    "📚 Data Sources & Audit": "sources",
}

COUNTRY_THEMES = {
    "Saudi Arabia": {
        "flag": "🇸🇦", "primary": "#006C35", "accent": "#C5A059",
        "bg": "#0D1B1E", "card_bg": "rgba(19,42,47,0.85)", "text": "#E6F1FF",
        "landmark": "Kingdom Centre & Riyadh Skyline"
    },
    "UAE": {
        "flag": "🇦🇪", "primary": "#CE1126", "accent": "#00732F",
        "bg": "#1A0F10", "card_bg": "rgba(42,22,24,0.85)", "text": "#FFFFFF",
        "landmark": "Burj Khalifa & Dubai Skyline"
    },
    "Qatar": {
        "flag": "🇶🇦", "primary": "#8A1538", "accent": "#E0A96D",
        "bg": "#1C0D12", "card_bg": "rgba(46,21,30,0.85)", "text": "#FFF5F5",
        "landmark": "Doha Corniche & Museum of Islamic Art"
    },
    "Kuwait": {
        "flag": "🇰🇼", "primary": "#007A3D", "accent": "#CE1126",
        "bg": "#0A1816", "card_bg": "rgba(17,41,37,0.85)", "text": "#E6FFFA",
        "landmark": "Kuwait Towers"
    },
    "Oman": {
        "flag": "🇴🇲", "primary": "#DB162F", "accent": "#008000",
        "bg": "#1C0D10", "card_bg": "rgba(46,22,26,0.85)", "text": "#FFF0F0",
        "landmark": "Al Alam Palace & Muscat Forts"
    },
    "Bahrain": {
        "flag": "🇧🇭", "primary": "#CE1126", "accent": "#FFFFFF",
        "bg": "#1A0F10", "card_bg": "rgba(42,22,24,0.85)", "text": "#FFFFFF",
        "landmark": "Bahrain World Trade Center"
    },
    "Jordan": {
        "flag": "🇯🇴", "primary": "#000000", "accent": "#CE1126",
        "bg": "#121212", "card_bg": "rgba(31,31,31,0.85)", "text": "#F5F5F5",
        "landmark": "Petra & Amman Citadel"
    },
    "Lebanon": {
        "flag": "🇱🇧", "primary": "#CE1126", "accent": "#007A3D",
        "bg": "#1A0D0D", "card_bg": "rgba(43,22,22,0.85)", "text": "#FFF0F0",
        "landmark": "Jeita Grotto & Beirut Skyline"
    },
  "Iraq": {
        "flag": "🇮🇶", "primary": "#CE1126", "accent": "#007A3D",
        "bg": "#121212", "card_bg": "rgba(30,30,30,0.85)", "text": "#FFFFFF",
        "landmark": "Erbil Citadel & Baghdad Skyline"
    },
}

TREND_ICONS = {"up": "▲", "down": "▼", "stable": "◆"}
TREND_COLORS = {"up": "#00C853", "down": "#FF1744", "stable": "#FFD600"}

# ─────────────────────────────────────────────
# 1. HELPER FUNCTIONS & RESILIENT DATA RETRIEVAL
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
    if not LANDSCAPE_DIR.exists():
        return ""
    
    # استخراج الكلمة الأساسية من اسم الدولة (مثلاً saudi من Saudi Arabia)
    key = country.lower().split()[0]
    if key == "jordan":
        key = "jord"    # للتعامل مع تسمية jordon
    elif key == "bahrain":
        key = "bahra"   # للتعامل مع تسمية bahraien
        
    for p in LANDSCAPE_DIR.glob("*"):
        if p.is_file() and key in p.name.lower() and "landscape" in p.name.lower():
            return _image_to_b64(p)
            
    return ""

def find_flag_b64(country: str) -> str:
    key = country.lower().split()[0]
    if key == "jordan":
        key = "jord"
    elif key == "bahrain":
        key = "bahra"
        
    if ASSETS_DIR.exists():
        for p in ASSETS_DIR.glob("**/*"):
            if p.is_file() and key in p.name.lower() and "flag" in p.name.lower():
                return _image_to_b64(p)
    return ""

def logo_b64() -> str:
    if not LOGO_DIR.exists():
        return ""
    for ext in ("png", "jpeg", "jpg"):
        b64 = _image_to_b64(LOGO_DIR / f"amecath_logo.{ext}")
        if b64:
            return b64
    return ""

def find_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """Dynamically finds a column matching any candidate name (case & whitespace insensitive)."""
    normalized_cols = {str(c).strip().lower(): str(c) for c in df.columns}
    for cand in candidates:
        norm_cand = cand.strip().lower()
        if norm_cand in normalized_cols:
            return normalized_cols[norm_cand]
    return None

def resolve_master_filepath() -> Optional[str]:
    """Finds available Excel file in root directory."""
    if os.path.exists(PRIMARY_FILE):
        return PRIMARY_FILE
    for fname in FALLBACK_FILES:
        if os.path.exists(fname):
            return fname
    return None

@st.cache_data(ttl=300)
def load_master_data(filepath: str) -> Dict[str, pd.DataFrame]:
    """Loads and maps Excel sheets dynamically matching internal aliases."""
    xls = pd.ExcelFile(filepath)
    actual_sheets = {s.strip().lower(): s for s in xls.sheet_names}

    sheets: Dict[str, pd.DataFrame] = {}
    missing_keys = []

    for key, candidates in REQUIRED_SHEETS.items():
        matched_sheet = None
        for cand in candidates:
            norm_cand = cand.strip().lower()
            if norm_cand in actual_sheets:
                matched_sheet = actual_sheets[norm_cand]
                break

        if matched_sheet:
            df = pd.read_excel(filepath, sheet_name=matched_sheet)
            sheets[key] = df.dropna(how="all").reset_index(drop=True)
        else:
            missing_keys.append(candidates[0])

    if missing_keys:
        st.warning(f"⚠️ Could not automatically match sheet(s): `{missing_keys}`")

    return sheets

def get_sheet(data: Dict[str, pd.DataFrame], key: str) -> Optional[pd.DataFrame]:
    return data.get(key)

# ─────────────────────────────────────────────
# 2. STYLING & HERO COMPONENTS
# ─────────────────────────────────────────────

def inject_css(theme: dict, bg_b64: str = "") -> None:
    bg_css = f"""
    .stApp {{
        background: linear-gradient(rgba(10,15,20,0.82), rgba(10,15,20,0.92)),
                    url("data:image/jpeg;base64,{bg_b64}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}""" if bg_b64 else f".stApp {{ background-color: {theme['bg']} !important; }}"

    st.markdown(f"""
    <style>
    {bg_css}
    body, .stApp {{ color: {theme['text']}; font-family: 'Segoe UI', Roboto, sans-serif; }}
    .country-mini-card {{
        background: {theme['card_bg']};
        border-left: 5px solid {theme['primary']}; border-radius: 12px;
        padding: 16px 18px; margin-bottom: 14px; backdrop-filter: blur(8px);
        box-shadow: 0 4px 14px rgba(0,0,0,0.4);
        transition: transform 0.2s ease-in-out;
    }}
    .hero-banner {{
        background: linear-gradient(135deg, {theme['primary']}CC, {theme['card_bg']});
        padding: 22px 28px; border-radius: 16px; border-left: 6px solid {theme['accent']};
        margin-bottom: 25px; backdrop-filter: blur(10px); box-shadow: 0 6px 20px rgba(0,0,0,0.45);
    }}
    .header-container {{ display: flex; align-items: center; justify-content: space-between; gap: 15px; }}
    .header-title {{ color: #FFFFFF; margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 0.5px; }}
    .forecast-frame {{
        background: {theme['card_bg']}; border: 1px solid {theme['accent']}66;
        border-radius: 12px; padding: 20px; backdrop-filter: blur(6px);
    }}
    </style>
    """, unsafe_allow_html=True)


def render_hero(country: str, theme: dict, bg_b64: str = "") -> None:
    flag_b64 = find_flag_b64(country)
    if flag_b64:
        flag_html = f'<img src="data:image/png;base64,{flag_b64}" style="height:32px; border-radius:4px; margin-right:10px; vertical-align:middle; box-shadow:0 2px 6px rgba(0,0,0,0.3);">'
    else:
        flag_html = f'<span style="font-size:38px;margin-right:10px;">{theme["flag"]}</span>'

    logo = logo_b64()
    logo_html = (
        f'<img src="data:image/png;base64,{logo}" style="height:46px;position:absolute;right:25px;top:20px;" alt="AMECATH logo">'
        if logo else ""
    )
    
    bg_style = (
        f"background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url('data:image/jpeg;base64,{bg_b64}') center/cover no-repeat;"
        if bg_b64 else f"background: linear-gradient(135deg, {theme['primary']}CC, {theme['card_bg']});"
    )

    st.markdown(f"""
    <div class="hero-banner" style="{bg_style} position: relative; text-align: center; padding: 30px 20px;">
      {logo_html}
      <div style="display:flex; align-items:center; justify-content:center; gap:10px;">
        {flag_html}
        <h1 class="header-title" style="margin:0; font-size:34px; letter-spacing:1px;">{country.upper()}</h1>
      </div>
      <p style="color:{theme['accent']}; font-size:14px; margin-top:10px; margin-bottom:0; font-weight:600;">
        &#128205; Strategic Landmark: <span>{theme['landmark']}</span>
      </p>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. VIEWS & DASHBOARD SECTIONS
# ─────────────────────────────────────────────

def render_generic_table(data: Dict[str, pd.DataFrame], key: str, title: str, country: str) -> None:
    st.subheader(f"{title} — {country}")
    df = get_sheet(data, key)
    if df is not None and not df.empty:
        country_col = find_column(df, ["country", "الدولة", "Market", "Region"])
        if country_col:
            filtered_df = df[df[country_col].astype(str).str.strip().str.lower() == country.lower()]
            if not filtered_df.empty:
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            else:
                st.info(f"No records matching '{country}' in section data.")
                with st.expander("🔍 View Unfiltered Sheet Data"):
                    st.dataframe(df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning(f"No data available for key '{key}'.")

def render_hot_areas(data: Dict[str, pd.DataFrame], selected_country: str, theme: dict) -> None:
    st.subheader(f"🔥 Hot Market Areas — {selected_country}")
    df = get_sheet(data, "hot_areas")
    
    if df is None or df.empty:
        st.warning("No Hot Market Areas data available.")
        return

    # Find matching country column
    country_col = find_column(df, [selected_country])
    if not country_col:
        for col in df.columns:
            if selected_country.lower() in str(col).lower():
                country_col = col
                break

    if not country_col:
        st.warning(f"No specific hot market area data found for {selected_country}.")
        st.dataframe(df, use_container_width=True)
        return

    # Parse City Names, Centers count & Details
    rank_col = find_column(df, ["rank", "الترتيب", "no"])
    parsed_data = []

    for idx, row in df.iterrows():
        val = str(row[country_col]) if pd.notna(row[country_col]) else ""
        if not val or val.strip() in ["-", "nan", "None"]:
            continue
        
        rank = row[rank_col] if rank_col and pd.notna(row[rank_col]) else idx + 1
        
        # Extract City Name (text before parenthesis)
        city_match = re.split(r'[\(;\:]', val)[0].strip()
        city_name = city_match if city_match else f"Area {rank}"
        
        # Extract number of centers for Treemap sizing
        centers_match = re.search(r'(\d+)\s*center', val, re.IGNORECASE)
        centers = int(centers_match.group(1)) if centers_match else (10 - min(idx, 9))

        parsed_data.append({
            "Rank": rank,
            "City": city_name,
            "Centers": centers,
            "Details": val
        })

    if not parsed_data:
        st.info(f"No valid data points found for {selected_country}.")
        return

    parsed_df = pd.DataFrame(parsed_data)

    # 💥 قائمة ألوان Flame النارية المصممة يدويًا لضمان التوافق
    flame_colors = ['#2B0000', '#660000', '#990000', '#CC3300', '#FF6600', '#FF9900', '#FFCC00']

    # Render Interactive Plotly Treemap using Custom Flame Palette
    fig = px.treemap(
        parsed_df,
        path=['City'],
        values='Centers',
        color='Centers',
        color_continuous_scale=flame_colors,
        hover_data=['Rank', 'Details'],
        title=f"📍 Regional Market Concentration (Treemap) — {selected_country}"
    )
    
    fig.update_layout(
        margin=dict(t=40, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#FFFFFF", size=14),
        coloraxis_showscale=False
    )
    
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value} Centers",
        hovertemplate="<b>%{label}</b><br>Rank: %{customdata[0]}<br>Centers: %{value}<br><br>%{customdata[1]}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed Table View
    with st.expander("📋 View Detailed Market Breakdown Table", expanded=False):
        st.dataframe(parsed_df[['Rank', 'City', 'Centers', 'Details']], use_container_width=True, hide_index=True)

def render_forecast(data: Dict[str, pd.DataFrame], selected_country: str, theme: dict) -> None:
    st.subheader(f"🔮 Revenue & Growth Forecast — {selected_country}")
    df_fc = get_sheet(data, "forecast")
    if df_fc is None or df_fc.empty:
        st.info("Forecast data sheet is missing or empty.")
        return

    country_col = find_column(df_fc, ["country", "الدولة", "Market"])
    year_col = find_column(df_fc, ["year", "السنة", "Year"])
    val_col = find_column(df_fc, ["value", "revenue", "amount", "forecast_value"])
    metric_col = find_column(df_fc, ["metric", "indicator", "kpi"])
    scenario_col = find_column(df_fc, ["scenario", "case"])

    df_c = df_fc
    if country_col:
        df_c = df_fc[df_fc[country_col].astype(str).str.strip().str.lower() == selected_country.lower()].copy()

    if df_c.empty:
        st.warning(f"No specific forecast record found for {selected_country}. Displaying combined dataset:")
        st.dataframe(df_fc, use_container_width=True)
        return

    filters_col1, filters_col2 = st.columns(2)
    
    if metric_col and df_c[metric_col].nunique() > 1:
        metrics = df_c[metric_col].dropna().unique().tolist()
        sel_metric = filters_col1.selectbox("📊 Select Metric", metrics)
        df_c = df_c[df_c[metric_col] == sel_metric]

    if scenario_col and df_c[scenario_col].nunique() > 1:
        scenarios = df_c[scenario_col].dropna().unique().tolist()
        sel_scenario = filters_col2.selectbox("🎯 Scenario", scenarios)
        df_c = df_c[df_c[scenario_col] == sel_scenario]

    if year_col and val_col:
        df_plot = df_c.sort_values(year_col)
        st.markdown('<div class="forecast-frame">', unsafe_allow_html=True)
        st.line_chart(df_plot.set_index(year_col)[val_col], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("##### Detailed Forecast Data")
    st.dataframe(df_c, use_container_width=True, hide_index=True)

def render_hot_areas(data: Dict[str, pd.DataFrame], selected_country: str, theme: dict) -> None:
    st.subheader(f"🔥 Hot Market Areas — {selected_country}")
    df = get_sheet(data, "hot_areas")
    
    if df is None or df.empty:
        st.warning("No Hot Market Areas data available.")
        return

    # Find matching country column
    country_col = find_column(df, [selected_country])
    if not country_col:
        for col in df.columns:
            if selected_country.lower() in str(col).lower():
                country_col = col
                break

    if not country_col:
        st.warning(f"No specific hot market area data found for {selected_country}.")
        st.dataframe(df, use_container_width=True)
        return

    # Parse City Names, Centers count & Details
    rank_col = find_column(df, ["rank", "الترتيب", "no"])
    parsed_data = []

    for idx, row in df.iterrows():
        val = str(row[country_col]) if pd.notna(row[country_col]) else ""
        if not val or val.strip() in ["-", "nan", "None"]:
            continue
        
        rank = row[rank_col] if rank_col and pd.notna(row[rank_col]) else idx + 1
        
        # Extract City Name (text before parenthesis)
        city_match = re.split(r'[\(;\:]', val)[0].strip()
        city_name = city_match if city_match else f"Area {rank}"
        
        # Extract number of centers for Treemap sizing
        centers_match = re.search(r'(\d+)\s*center', val, re.IGNORECASE)
        centers = int(centers_match.group(1)) if centers_match else (10 - min(idx, 9))

        parsed_data.append({
            "Rank": rank,
            "City": city_name,
            "Centers": centers,
            "Details": val
        })

    if not parsed_data:
        st.info(f"No valid data points found for {selected_country}.")
        return

    parsed_df = pd.DataFrame(parsed_data)

    # Render Interactive Plotly Treemap using Flame Palette
    fig = px.treemap(
        parsed_df,
        path=['City'],
        values='Centers',
        color='Centers',
        color_continuous_scale=px.colors.sequential.Flame,  # بالتة ألوان Flame
        hover_data=['Rank', 'Details'],
        title=f"📍 Regional Market Concentration (Treemap) — {selected_country}"
    )
    
    fig.update_layout(
        margin=dict(t=40, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#FFFFFF", size=14),
        coloraxis_showscale=False
    )
    
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value} Centers",
        hovertemplate="<b>%{label}</b><br>Rank: %{customdata[0]}<br>Centers: %{value}<br><br>%{customdata[1]}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed Table View
    with st.expander("📋 View Detailed Market Breakdown Table", expanded=False):
        st.dataframe(parsed_df[['Rank', 'City', 'Centers', 'Details']], use_container_width=True, hide_index=True)
    
    if df is None or df.empty:
        st.warning("No Hot Market Areas data available.")
        return

    # Find matching country column
    country_col = find_column(df, [selected_country])
    if not country_col:
        for col in df.columns:
            if selected_country.lower() in str(col).lower():
                country_col = col
                break

    if not country_col:
        st.warning(f"No specific hot market area data found for {selected_country}.")
        st.dataframe(df, use_container_width=True)
        return

    # Parse City Names, Centers count & Details
    rank_col = find_column(df, ["rank", "الترتيب", "no"])
    parsed_data = []

    for idx, row in df.iterrows():
        val = str(row[country_col]) if pd.notna(row[country_col]) else ""
        if not val or val.strip() in ["-", "nan", "None"]:
            continue
        
        rank = row[rank_col] if rank_col and pd.notna(row[rank_col]) else idx + 1
        
        # Extract City Name (text before parenthesis)
        city_match = re.split(r'[\(;\:]', val)[0].strip()
        city_name = city_match if city_match else f"Area {rank}"
        
        # Extract number of centers for Treemap sizing (fallback to rank weight if not specified)
        centers_match = re.search(r'(\d+)\s*center', val, re.IGNORECASE)
        centers = int(centers_match.group(1)) if centers_match else (10 - min(idx, 9))

        parsed_data.append({
            "Rank": rank,
            "City": city_name,
            "Centers": centers,
            "Details": val
        })

    if not parsed_data:
        st.info(f"No valid data points found for {selected_country}.")
        return

    parsed_df = pd.DataFrame(parsed_data)

    # Render Interactive Plotly Treemap
    fig = px.treemap(
        parsed_df,
        path=['City'],
        values='Centers',
        color='Centers',
        color_continuous_scale=['#002B49', '#005A9C', '#00D4FF'],
        hover_data=['Rank', 'Details'],
        title=f"📍 Regional Market Concentration (Treemap) — {selected_country}"
    )
    
    fig.update_layout(
        margin=dict(t=40, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#FFFFFF", size=14),
        coloraxis_showscale=False
    )
    
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value} Centers",
        hovertemplate="<b>%{label}</b><br>Rank: %{customdata[0]}<br>Centers: %{value}<br><br>%{customdata[1]}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed Table View
    with st.expander("📋 View Detailed Market Breakdown Table", expanded=False):
        st.dataframe(parsed_df[['Rank', 'City', 'Centers', 'Details']], use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# 4. SIDEBAR CONTROLS & NAVIGATION ROUTING
# ─────────────────────────────────────────────

st.sidebar.markdown("## 🩺 AMECATH Hub")
st.sidebar.markdown("---")

selected_country = st.sidebar.selectbox("🌍 Target Country / Market", list(COUNTRY_THEMES.keys()))
theme = COUNTRY_THEMES[selected_country]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Section Navigation")
selected_nav_label = st.sidebar.radio("Go to Section", list(NAV_MAP.keys()))
nav_mode = NAV_MAP[selected_nav_label]

st.sidebar.markdown("---")

# ─────────────────────────────────────────────
# 1. HELPER FUNCTIONS & RESILIENT DATA RETRIEVAL
# ─────────────────────────────────────────────

def _image_to_b64(path: Path) -> str:
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return ""

def find_overview_bg_b64() -> str:
    """Finds overview background image matching 'overview' or 'background'."""
    if ASSETS_DIR.exists():
        for p in ASSETS_DIR.glob("**/*"):
            if p.is_file() and any(k in p.name.lower() for k in ["overview", "catheter", "background"]):
                return _image_to_b64(p)
    for p in Path(".").glob("*"):
        if p.is_file() and any(k in p.name.lower() for k in ["overview", "catheter", "background"]):
            return _image_to_b64(p)
    return ""

def find_landscape_b64(country: str) -> str:
    if not LANDSCAPE_DIR.exists():
        return ""
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
    """Flexible logo matching for any variation of amecath logo file name."""
    search_dirs = [LOGO_DIR, ASSETS_DIR, Path(".")]
    for d in search_dirs:
        if d.exists():
            for p in d.glob("**/*"):
                if p.is_file() and "logo" in p.name.lower():
                    return _image_to_b64(p)
    return ""

# ─────────────────────────────────────────────
# STYLING INJECTION WITH DARK OVERLAY FOR CLARITY
# ─────────────────────────────────────────────

def inject_css(theme: dict, bg_b64: str = "") -> None:
    # High-contrast overlay to make text crisp over white/bright backgrounds
    bg_css = f"""
    .stApp {{
        background: linear-gradient(rgba(5, 19, 41, 0.82), rgba(5, 19, 41, 0.92)),
                    url("data:image/png;base64,{bg_b64}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}""" if bg_b64 else f".stApp {{ background-color: {theme['bg']} !important; }}"

    st.markdown(f"""
    <style>
    {bg_css}
    body, .stApp {{ color: {theme['text']}; font-family: 'Segoe UI', Roboto, sans-serif; }}
    .country-mini-card {{
        background: {theme['card_bg']};
        border-left: 5px solid {theme['primary']}; border-radius: 12px;
        padding: 16px 18px; margin-bottom: 14px; backdrop-filter: blur(10px);
        box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    }}
    .hero-banner {{
        background: linear-gradient(135deg, {theme['primary']}CC, {theme['card_bg']});
        padding: 22px 28px; border-radius: 16px; border-left: 6px solid {theme['accent']};
        margin-bottom: 25px; backdrop-filter: blur(10px); box-shadow: 0 6px 20px rgba(0,0,0,0.45);
    }}
    .header-container {{ display: flex; align-items: center; justify-content: space-between; gap: 15px; }}
    .header-title {{ color: #FFFFFF; margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 0.5px; }}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 5. EXECUTION & APP INITIALIZATION
# ─────────────────────────────────────────────

active_filepath = resolve_master_filepath()

if not active_filepath:
    st.error("⚠️ Master dataset file not found.")
    uploaded_file = st.file_uploader("Upload Master Dataset (.xlsx)", type=["xlsx"])
    if uploaded_file:
        data_sheets = {}
        xls = pd.ExcelFile(uploaded_file)
        actual_sheets = {s.strip().lower(): s for s in xls.sheet_names}
        for key, candidates in REQUIRED_SHEETS.items():
            for cand in candidates:
                if cand.strip().lower() in actual_sheets:
                    data_sheets[key] = pd.read_excel(uploaded_file, sheet_name=actual_sheets[cand.strip().lower()])
                    break
        active_filepath = uploaded_file.name
    else:
        st.stop()
else:
    try:
        data_sheets = load_master_data(active_filepath)
    except Exception as e:
        st.error(f"Error loading Excel file `{active_filepath}`: {e}")
        st.stop()

st.sidebar.caption(
    f"📁 File: `{os.path.basename(str(active_filepath))}`  \n"
    f"📍 Section: `{nav_mode}`  \n"
    f"⚡ Version: 2.3"
)

# AMECATH Navy Theme Configuration
overview_theme = {
    "flag": "🌐", "primary": "#005A9C", "accent": "#00D4FF",
    "bg": "#051329", "card_bg": "rgba(8, 28, 54, 0.88)", "text": "#FFFFFF",
    "landmark": "Scope: Middle East & GCC Markets Performance"
}

active_theme = overview_theme if nav_mode == "overview" else theme

# Background image routing
if nav_mode == "overview":
    bg_b64 = find_overview_bg_b64()
else:
    bg_b64 = find_landscape_b64(selected_country)

inject_css(active_theme, bg_b64)

# Dashboard Routing Switcher
if nav_mode == "overview":
    logo = logo_b64()

    logo_html = (
        f'<img src="data:image/png;base64,{logo}" style="height:48px; background:white; padding:6px 12px; border-radius:8px; box-shadow:0 3px 10px rgba(0,0,0,0.4);" alt="AMECATH Logo">'
        if logo else ""
    )

    st.markdown(f"""
    <div class="hero-banner" style="position: relative; text-align: center; padding: 28px 20px; background: linear-gradient(135deg, rgba(0, 43, 73, 0.92), rgba(0, 90, 156, 0.92)); border-left: 6px solid #00D4FF; border-radius: 14px; box-shadow: 0 4px 18px rgba(0,0,0,0.5);">
      <div style="position: absolute; right: 20px; top: 18px;">
        {logo_html}
      </div>
      <h1 class="header-title" style="margin:0; font-size:30px; letter-spacing:1px; color: #FFFFFF;">🌐 REGIONAL EXECUTIVE OVERVIEW</h1>
      <p style="color: #D0E8FF; font-size:14px; margin-top:8px; margin-bottom:0; font-weight:600;">
        📍 Scope: Middle East & GCC Markets Performance
      </p>
    </div>""", unsafe_allow_html=True)
    
    render_overview(data_sheets, active_theme)
else:
    render_hero(selected_country, theme)
    if nav_mode == "macro":
        render_generic_table(data_sheets, "macro", "📊 Macro Environment", selected_country)
    elif nav_mode == "tenders":
        render_generic_table(data_sheets, "tenders", "📈 Financials & Tenders", selected_country)
    elif nav_mode == "hot_areas":
        render_hot_areas(data_sheets, selected_country, active_theme)
    elif nav_mode == "distributors":
        render_generic_table(data_sheets, "distributors", "🤝 Local Distributors Network", selected_country)
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
