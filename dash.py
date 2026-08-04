import base64
import glob
import os
import pandas as pd
import streamlit as st

# Set page config
st.set_page_config(
    page_title="AMECATH Executive Intelligence Hub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 1. COUNTRY THEMES & COLOR PALETTES CONFIGURATION ---
COUNTRY_THEMES = {
    "Saudi Arabia": {
        "flag": "🇸🇦",
        "primary": "#006C35",
        "accent": "#C5A059",
        "bg": "#0D1B1E",
        "card_bg": "rgba(19, 42, 47, 0.85)",
        "text": "#E6F1FF",
        "landmark": "Kingdom Centre & Riyadh Skyline",
        "file": "AMECATH_Saudi_Arabia_Executive_Dashboard.xlsx",
    },
    "UAE": {
        "flag": "🇦🇪",
        "primary": "#CE1126",
        "accent": "#00732F",
        "bg": "#1A0F10",
        "card_bg": "rgba(42, 22, 24, 0.85)",
        "text": "#FFFFFF",
        "landmark": "Burj Khalifa & Dubai Skyline",
        "file": "AMECATH_UAE_Executive_Dashboard.xlsx",
    },
    "Qatar": {
        "flag": "🇶🇦",
        "primary": "#8A1538",
        "accent": "#E0A96D",
        "bg": "#1C0D12",
        "card_bg": "rgba(46, 21, 30, 0.85)",
        "text": "#FFF5F5",
        "landmark": "Doha Corniche & Museum of Islamic Art",
        "file": "AMECATH_Qatar_Executive_Dashboard.xlsx",
    },
    "Kuwait": {
        "flag": "🇰🇼",
        "primary": "#007A3D",
        "accent": "#CE1126",
        "bg": "#0A1816",
        "card_bg": "rgba(17, 41, 37, 0.85)",
        "text": "#E6FFFA",
        "landmark": "Kuwait Towers",
        "file": "AMECATH_Kuwait_Executive_Dashboard.xlsx",
    },
    "Oman": {
        "flag": "🇴🇲",
        "primary": "#DB162F",
        "accent": "#008000",
        "bg": "#1C0D10",
        "card_bg": "rgba(46, 22, 26, 0.85)",
        "text": "#FFF0F0",
        "landmark": "Al Alam Palace & Muscat Forts",
        "file": "AMECATH_Oman_Executive_Dashboard.xlsx",
    },
    "Bahrain": {
        "flag": "🇧🇭",
        "primary": "#CE1126",
        "accent": "#FFFFFF",
        "bg": "#1A0F10",
        "card_bg": "rgba(42, 22, 24, 0.85)",
        "text": "#FFFFFF",
        "landmark": "Bahrain World Trade Center",
        "file": "AMECATH_Bahrain_Executive_Dashboard.xlsx",
    },
    "Jordan": {
        "flag": "🇯🇴",
        "primary": "#000000",
        "accent": "#CE1126",
        "bg": "#121212",
        "card_bg": "rgba(31, 31, 31, 0.85)",
        "text": "#F5F5F5",
        "landmark": "Petra & Amman Citadel",
        "file": "AMECATH_Jordan_Executive_Dashboard.xlsx",
    },
    "Lebanon": {
        "flag": "🇱🇧",
        "primary": "#CE1126",
        "accent": "#007A3D",
        "bg": "#1A0D0D",
        "card_bg": "rgba(43, 22, 22, 0.85)",
        "text": "#FFF0F0",
        "landmark": "Jeita Grotto & Beirut Skyline",
        "file": "AMECATH_Lebanon_Executive_Dashboard.xlsx",
    },
}

# --- 2. SIDEBAR NAVIGATION & COUNTRY SELECTION ---
st.sidebar.markdown(
    "## 🩺 AMECATH Executive Intelligence", unsafe_allow_html=True
)
st.sidebar.markdown("---")

selected_country = st.sidebar.selectbox(
    "🌍 Select Target Country / Market", list(COUNTRY_THEMES.keys())
)
theme = COUNTRY_THEMES[selected_country]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Navigation Menu")
nav_mode = st.sidebar.radio(
    "Go to Section",
    [
        "📊 Macro & Exec Summary",
        "📋 7 Questions Summary",
        "🏥 Hospitals & Infrastructure",
        "⚔️ Competitors & Pricing",
        "📈 Financials & Tenders",
    ],
)


# --- دالة مرنة للبحث عن الملف وتحويله إلى Base64 بغض النظر عن امتداد الصورة ---
def find_and_get_base64(prefix):
  # تدعم البحث عن .jpeg, .jpg, .png وبأشكال الحروف المختلفة
  patterns = [
      f"{prefix}*.jpeg",
      f"{prefix}*.jpg",
      f"{prefix}*.png",
      f"{prefix.lower()}*.jpeg",
      f"{prefix.lower()}*.jpg",
  ]
  for pattern in patterns:
    matches = glob.glob(pattern)
    if matches:
      with open(matches[0], "rb") as f:
        return base64.b64encode(f.read()).decode()
  return ""


bg_base64 = find_and_get_base64(f"{selected_country} landscape")
flag_base64 = find_and_get_base64(f"{selected_country} flag")

# إجبار Streamlit على إظهار الصورة كخلفية للتطبيق بالكامل
if bg_base64:
  bg_css = f"""
    .stApp {{
        background: linear-gradient(rgba(10, 15, 20, 0.75), rgba(10, 15, 20, 0.88)), 
                    url("data:image/jpeg;base64,{bg_base64}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}
    """
else:
  bg_css = f"""
    .stApp {{
        background-color: {theme['bg']} !important;
    }}
    """

# Inject Dynamic CSS
st.markdown(
    f"""
    <style>
    {bg_css}
    
    body, .stApp {{
        color: {theme['text']};
    }}
    
    .metric-card {{
        background-color: {theme['card_bg']};
        border: 1px solid {theme['primary']};
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        text-align: center;
        backdrop-filter: blur(6px);
    }}
    
    .hero-banner {{
        background: linear-gradient(135deg, {theme['primary']}CC, {theme['card_bg']});
        padding: 20px 25px;
        border-radius: 15px;
        border-left: 6px solid {theme['accent']};
        margin-bottom: 25px;
        backdrop-filter: blur(8px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.4);
    }}
    
    .header-container {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}
    
    .header-flag {{
        width: 60px;
        height: 40px;
        object-fit: cover;
        border-radius: 6px;
        border: 2px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.6);
    }}
    
    .header-title {{
        color: white;
        margin: 0;
        font-size: 26px;
        font-weight: bold;
    }}
    
    .competitor-card {{
        background-color: {theme['card_bg']};
        border-left: 4px solid {theme['accent']};
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        backdrop-filter: blur(6px);
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# هيدر التطبيق الرئيسي: العلم بجانب اسم الدولة في سطر واحد
flag_html = (
    f'<img src="data:image/jpeg;base64,{flag_base64}" class="header-flag">'
    if flag_base64
    else f'<span style="font-size:32px;">{theme["flag"]}</span>'
)

st.markdown(
    f"""
    <div class="hero-banner">
        <div class="header-container">
            {flag_html}
            <h1 class="header-title">{selected_country.upper()} — EXECUTIVE MARKET DOSSIER</h1>
        </div>
        <p style="color: {theme['accent']}; font-size: 15px; margin-top: 10px; margin-bottom: 0;">
            Strategic Landmark Focus: <b>{theme['landmark']}</b> | Active Theme Accent: <b>{theme['primary']}</b>
        </p>
    </div>
""",
    unsafe_allow_html=True,
)


# --- 3. DATA LOADING FUNCTION ---
@st.cache_data
def load_country_data(file_name):
  if os.path.exists(file_name):
    xls = pd.ExcelFile(file_name)
    sheets = {}
    for sh in xls.sheet_names:
      sheets[sh] = pd.read_excel(file_name, sheet_name=sh)
    return sheets
  return None


data_sheets = load_country_data(theme["file"])

if not data_sheets:
  st.error(
      f"⚠️ File `{theme['file']}` not found in the directory. Please make sure"
      " all country Excel files are uploaded."
  )
  st.stop()


# --- 4. SECTION ROUTING ---

if nav_mode == "📊 Macro & Exec Summary":
  st.subheader(f"📊 Macro & Executive Summary — {selected_country}")
  macro_sheet_name = [
      s for s in data_sheets.keys() if "Macro" in s or "Summary" in s
  ]
  if macro_sheet_name:
    df_macro = data_sheets[macro_sheet_name[0]]
    st.dataframe(df_macro.dropna(how="all"), use_container_width=True)
  else:
    st.info("Macro summary sheet not available for this country.")

elif nav_mode == "📋 7 Questions Summary":
  st.subheader(f"📋 Strategic 7 Questions Summary — {selected_country}")
  q7_sheet = [s for s in data_sheets.keys() if "7_Questions" in s]
  if q7_sheet:
    df_q7 = data_sheets[q7_sheet[0]]
    st.dataframe(df_q7.dropna(how="all"), use_container_width=True)
  else:
    st.info("7 Questions summary sheet not available.")

elif nav_mode == "🏥 Hospitals & Infrastructure":
  st.subheader(f"🏥 Hospitals & Renal Infrastructure — {selected_country}")
  inf_sheet = [s for s in data_sheets.keys() if "Hospitals" in s or "Infra" in s]
  if inf_sheet:
    df_inf = data_sheets[inf_sheet[0]]
    st.dataframe(df_inf.dropna(how="all"), use_container_width=True)
  else:
    st.info("Infrastructure data sheet not available.")

elif nav_mode == "⚔️ Competitors & Pricing":
  st.subheader(
      f"⚔️ Competitor Matrix & Deep-Dive Hub — {selected_country}"
  )
  comp_sheet = [s for s in data_sheets.keys() if "Competitor" in s]

  if comp_sheet:
    df_comp = data_sheets[comp_sheet[0]]
    st.markdown(
        "### 🏢 Market Competitors (Click a card or select for Deep-Dive)"
    )

    competitors_list = [
        "BD / Bard",
        "Teleflex / Arrow",
        "Medtronic / Covidien",
        "AngioDynamics",
        "Merit Medical",
    ]

    if "selected_competitor" not in st.session_state:
      st.session_state.selected_competitor = competitors_list[0]

    cols = st.columns(len(competitors_list))
    for idx, comp_name in enumerate(competitors_list):
      with cols[idx]:
        if st.button(
            comp_name, key=f"btn_{idx}", use_container_width=True
        ):
          st.session_state.selected_competitor = comp_name

    st.markdown("---")
    st.markdown(
        f"### 🔍 Deep-Dive Analysis:"
        f" **{st.session_state.selected_competitor}**"
    )

    col1, col2 = st.columns(2)
    with col1:
      st.markdown(
          f"""
            <div class="competitor-card">
                <h4>📌 Strategic Profile & Positioning</h4>
                <p><b>Primary Focus:</b> Vascular Access & Dialysis Catheters</p>
                <p><b>Market Standing:</b> Key incumbent with established hospital contracting across {selected_country}.</p>
                <p><b>Pricing Approach:</b> Premium tier pricing backed by established brand reputation and long-term tender history.</p>
            </div>
            """,
          unsafe_allow_html=True,
      )
    with col2:
      st.markdown(
          f"""
            <div class="competitor-card">
                <h4>⚡ Strengths & Vulnerabilities</h4>
                <p><b>Key Strengths:</b> High brand recognition among nephrologists and vascular surgeons.</p>
                <p><b>Identified Gaps:</b> Rigid bundle pricing and longer local switching cycles in tender renewals.</p>
                <p><b>AMECATH Opportunity:</b> Position high-biocompatibility (Carbothane) alternatives with agile supply terms.</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

    st.markdown("---")
    st.markdown("### Full Competitor Matrix Table")
    st.dataframe(df_comp.dropna(how="all"), use_container_width=True)
  else:
    st.info("Competitor matrix sheet not available.")

elif nav_mode == "📈 Financials & Tenders":
  st.subheader(f"📈 Financial Projections & Tenders — {selected_country}")
  st.markdown(
      f"""
    <div class="metric-card">
        <h3>2025 Addressable Market & Tender Outlook</h3>
        <p>Comprehensive market sizing, catheter consumption forecasts, and pricing benchmarks for <b>{selected_country}</b>.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )
  if "7_Questions_Summary" in data_sheets:
    st.dataframe(
        data_sheets["7_Questions_Summary"].dropna(how="all"),
        use_container_width=True,
    )
