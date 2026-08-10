import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import html
import re

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MEA HD Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# COUNTRY CONFIGURATION
# ============================================================

COUNTRIES = {
    "Saudi Arabia": {
        "code": "SAU",
        "flag": "saudi_arabia_flag.jpeg",
        "landscape": "saudi_landscape.jpeg",
        "color": "#16A34A",
        "light": "#22C55E",
        "dark": "#064E3B",
        "emoji": "🇸🇦"
    },
    "UAE": {
        "code": "ARE",
        "flag": "uae_flag.jpeg",
        "landscape": "uae_landscape.jpeg",
        "color": "#EF4444",
        "light": "#F87171",
        "dark": "#7F1D1D",
        "emoji": "🇦🇪"
    },
    "Qatar": {
        "code": "QAT",
        "flag": "qatar_flag.jpeg",
        "landscape": "qatar_landscape.jpeg",
        "color": "#8A1538",
        "light": "#B8325C",
        "dark": "#4A0B20",
        "emoji": "🇶🇦"
    },
    "Kuwait": {
        "code": "KWT",
        "flag": "kuwait_flag.jpeg",
        "landscape": "kuwait_landscape.jpeg",
        "color": "#60A5FA",
        "light": "#93C5FD",
        "dark": "#1E3A8A",
        "emoji": "🇰🇼"
    },
    "Oman": {
        "code": "OMN",
        "flag": "oman_flag.jpeg",
        "landscape": "oman_landscape.jpeg",
        "color": "#DC2626",
        "light": "#F87171",
        "dark": "#7F1D1D",
        "emoji": "🇴🇲"
    },
    "Bahrain": {
        "code": "BHR",
        "flag": "bahraien_flag.jpeg",
        "landscape": "bahrain_landscape.jpg",
        "color": "#D91E36",
        "light": "#F05267",
        "dark": "#7F1020",
        "emoji": "🇧🇭"
    },
    "Jordan": {
        "code": "JOR",
        "flag": "jordon_flag.jpeg",
        "landscape": "jordon_landscape.jpeg",
        "color": "#38BDF8",
        "light": "#7DD3FC",
        "dark": "#075985",
        "emoji": "🇯🇴"
    },
    "Lebanon": {
        "code": "LBN",
        "flag": "lebanon_flag.jpeg",
        "landscape": "lebanon_landscape.jpeg",
        "color": "#F97316",
        "light": "#FB923C",
        "dark": "#7C2D12",
        "emoji": "🇱🇧"
    },
    "Iraq": {
        "code": "IRQ",
        "flag": None,
        "landscape": None,
        "color": "#DC2626",
        "light": "#F87171",
        "dark": "#7F1D1D",
        "emoji": "🇮🇶"
    }
}


# ============================================================
# FILE HELPERS
# ============================================================

def find_file(filename):
    """
    Find a file in the GitHub/Streamlit repository.
    """
    path = BASE_DIR / filename

    if path.exists():
        return path

    return None


def load_csv(filename):
    """
    Load CSV safely.
    """
    path = find_file(filename)

    if path is None:
        return pd.DataFrame()

    try:
        return pd.read_csv(
            path,
            encoding="utf-8-sig",
            low_memory=False
        )
    except Exception:
        try:
            return pd.read_csv(
                path,
                encoding="utf-8",
                low_memory=False
            )
        except Exception:
            return pd.DataFrame()


def get_country_csv(country):
    code = COUNTRIES[country]["code"]

    filename_map = {
        "SAU": "18_SAU_Country.csv",
        "ARE": "19_ARE_Country.csv",
        "QAT": "20_QAT_Country.csv",
        "KWT": "21_KWT_Country.csv",
        "OMN": "22_OMN_Country.csv",
        "BHR": "23_BHR_Country.csv",
        "JOR": "24_JOR_Country.csv",
        "LBN": "25_LBN_Country.csv",
        "IRQ": "26_IRQ_Country.csv",
    }

    return load_csv(filename_map.get(code, ""))


# ============================================================
# IMAGE HELPERS
# ============================================================

def image_to_base64(filename):
    """
    Convert local image into a base64 data URI.
    This makes GitHub/Streamlit deployment easier.
    """
    if not filename:
        return None

    path = find_file(filename)

    if path is None:
        return None

    try:
        data = path.read_bytes()
        encoded = base64.b64encode(data).decode()

        extension = path.suffix.lower()

        mime = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp"
        }.get(extension, "image/jpeg")

        return f"data:{mime};base64,{encoded}"

    except Exception:
        return None


# ============================================================
# GLOBAL DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(30, 64, 175, 0.18),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #020617 0%,
                #07111F 45%,
                #0B1627 100%
            );

        color: #F8FAFC;
    }

    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #020617 0%,
                #07111F 100%
            );

        border-right: 1px solid #1E293B;
    }

    section[data-testid="stSidebar"] * {
        color: #E2E8F0;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ======================================================
       TEXT
       ====================================================== */

    h1, h2, h3, h4, h5 {
        color: #F8FAFC !important;
    }

    p, label {
        color: #CBD5E1 !important;
    }

    /* ======================================================
       SIDEBAR BRAND
       ====================================================== */

    .brand-box {
        padding: 8px 4px 20px 4px;
    }

    .brand-title {
        font-size: 21px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        font-size: 11px;
        color: #64748B;
        margin-top: 3px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ======================================================
       COUNTRY TAB AREA
       ====================================================== */

    .country-strip {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0 0 18px 0;
        padding: 10px 12px;
        border-radius: 14px;
        background: rgba(15, 23, 42, 0.80);
        border: 1px solid #1E293B;
        overflow-x: auto;
    }

    .country-pill {
        padding: 8px 14px;
        border-radius: 10px;
        white-space: nowrap;
        font-size: 12px;
        font-weight: 700;
        color: #CBD5E1;
        background: #0F172A;
        border: 1px solid #1E293B;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        position: relative;
        min-height: 310px;
        border-radius: 24px;
        overflow: hidden;
        margin-bottom: 25px;

        background-color: #0F172A;
        background-size: cover;
        background-position: center;

        border: 1px solid rgba(255,255,255,0.08);

        box-shadow:
            0 25px 70px rgba(0,0,0,0.40);
    }

    .hero-overlay {
        position: absolute;
        inset: 0;

        background:
            linear-gradient(
                90deg,
                rgba(2,6,23,0.98) 0%,
                rgba(2,6,23,0.86) 38%,
                rgba(2,6,23,0.38) 100%
            );
    }

    .hero-content {
        position: relative;
        z-index: 2;
        padding: 45px;
        max-width: 850px;
    }

    .flag {
        width: 72px;
        height: 45px;
        object-fit: cover;
        border-radius: 7px;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow: 0 6px 20px rgba(0,0,0,0.35);
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 38px;
        line-height: 1.1;
        font-weight: 850;
        color: white;
        letter-spacing: -1.3px;
        margin-bottom: 10px;
    }

    .hero-country {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .hero-description {
        font-size: 13px;
        color: #CBD5E1;
    }

    /* ======================================================
       KPI CARDS
       ====================================================== */

    .kpi-card {
        background:
            linear-gradient(
                145deg,
                rgba(15,23,42,0.95),
                rgba(15,23,42,0.70)
            );

        border: 1px solid #1E293B;
        border-radius: 18px;

        padding: 22px;
        min-height: 135px;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.20);

        transition: all 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #334155;
    }

    .kpi-label {
        color: #94A3B8;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .kpi-value {
        color: #F8FAFC;
        font-size: 27px;
        font-weight: 850;
        margin-top: 9px;
    }

    .kpi-note {
        color: #64748B;
        font-size: 11px;
        margin-top: 5px;
    }

    /* ======================================================
       SECTION HEADERS
       ====================================================== */

    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .section-line {
        width: 5px;
        height: 28px;
        border-radius: 5px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: #F8FAFC;
    }

    /* ======================================================
       INFO CARDS
       ====================================================== */

    .info-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 20px;
        min-height: 120px;
    }

    .info-title {
        color: #94A3B8;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 700;
    }

    .info-value {
        color: #F8FAFC;
        font-size: 21px;
        font-weight: 800;
        margin-top: 8px;
    }

    /* ======================================================
       TABLES
       ====================================================== */

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #334155;
        background: #0F172A;
        color: #E2E8F0;
    }

    .stButton > button:hover {
        border-color: #64748B;
        color: white;
    }

    /* ======================================================
       SELECT BOX
       ====================================================== */

    div[data-baseweb="select"] > div {
        background: #0F172A;
        border-color: #334155;
        color: #F8FAFC;
    }

    /* ======================================================
       ALERTS
       ====================================================== */

    div[data-testid="stAlert"] {
        background: #0F172A;
        border: 1px solid #334155;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

EXECUTIVE = load_csv("01_Executive_Summary.csv")
COUNTRY_MASTER = load_csv("02_Country_Master.csv")
MARKET_SIZING = load_csv("03_Market_Sizing.csv")
DEMAND_MODEL = load_csv("04_Demand_Model.csv")
KOLS = load_csv("05_KOL_Master.csv")
HOSPITALS = load_csv("06_Major_Hospitals.csv")
HOT_AREAS = load_csv("07_Hot_Areas.csv")
DISTRIBUTORS = load_csv("08_Top_Distributors.csv")
COMPETITORS = load_csv("09_Competitor_Master.csv")
TENDER_SKU = load_csv("10_Tender_SKU_Detail.csv")
NUPCO = load_csv("11_NUPCO_Tenders.csv")
TENDERS = load_csv("12_Tender_Master.csv")
DATA_GAPS = load_csv("13_Data_Gaps.csv")
AUDIT = load_csv("14_Audit_Checks.csv")
QA = load_csv("15_QA_Summary.csv")
DATA_DICTIONARY = load_csv("16_Data_Dictionary.csv")
SOURCES = load_csv("17_Source_Register.csv")

FACILITIES = pd.DataFrame()

# ============================================================
# LOAD FACILITY DATABASE
# ============================================================

facility_candidates = [
    "07_HD_Facility_Master.csv",
    "HD_Facility_Master.csv",
]

for f in facility_candidates:
    temp = load_csv(f)

    if not temp.empty:
        FACILITIES = temp
        break


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_value(df, columns, country=None, default=None):
    """
    Find first matching value from several possible column names.
    """

    if df is None or df.empty:
        return default

    work = df.copy()

    if country:
        country_cols = [
            "Country",
            "country",
            "Country_Name"
        ]

        for col in country_cols:
            if col in work.columns:
                mask = (
                    work[col]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    == country.lower()
                )

                filtered = work[mask]

                if not filtered.empty:
                    work = filtered
                    break

    for col in columns:
        if col in work.columns:
            values = work[col].dropna()

            if len(values):
                return values.iloc[0]

    return default


def format_number(value):
    if value is None:
        return "—"

    if pd.isna(value):
        return "—"

    try:
        number = float(value)

        if number.is_integer():
            return f"{int(number):,}"

        return f"{number:,.2f}"

    except Exception:
        return str(value)


def filter_country(df, country):
    if df is None or df.empty:
        return pd.DataFrame()

    country_columns = [
        "Country",
        "Country_Name",
        "Market",
        "Country Name"
    ]

    for col in country_columns:
        if col in df.columns:

            result = df[
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                == country.lower()
            ]

            if not result.empty:
                return result

    return df.iloc[0:0]


def render_table(df, max_rows=100):
    if df is None or df.empty:
        st.info("No verified data available in this table.")
        return

    display_df = df.head(max_rows).copy()

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# HERO
# ============================================================

def render_hero(country):

    info = COUNTRIES[country]

    flag = image_to_base64(info["flag"])
    landscape = image_to_base64(info["landscape"])

    if landscape:
        background = f"background-image: url('{landscape}');"
    else:
        background = (
            f"background: linear-gradient("
            f"135deg, {info['dark']}, #020617);"
        )

    flag_html = ""

    if flag:
        flag_html = (
            f'<img class="flag" src="{flag}" '
            f'alt="{html.escape(country)} flag">'
        )
    else:
        flag_html = (
            f'<div style="font-size:42px;margin-bottom:14px;">'
            f'{info["emoji"]}</div>'
        )

    st.markdown(
        f"""
        <div class="hero" style="{background}">
            <div class="hero-overlay"></div>

            <div class="hero-content">

                {flag_html}

                <div class="hero-title">
                    MEA Hemodialysis<br>
                    Catheter Market Intelligence
                </div>

                <div
                    class="hero-country"
                    style="color:{info['light']};"
                >
                    {info['emoji']} {html.escape(country)}
                    ({info['code']})
                </div>

                <div class="hero-description">
                    2026 Medical Device Commercial Intelligence
                    • Hemodialysis • Vascular Access • Catheter Market
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# KPI
# ============================================================

def kpi(label, value, note, color):
    st.markdown(
        f"""
        <div class="kpi-card"
             style="border-top:3px solid {color};">

            <div class="kpi-label">
                {html.escape(label)}
            </div>

            <div class="kpi-value">
                {html.escape(str(value))}
            </div>

            <div class="kpi-note">
                {html.escape(str(note))}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SECTION
# ============================================================

def section(title, color):
    st.markdown(
        f"""
        <div class="section-header">
            <div
                class="section-line"
                style="background:{color};"
            ></div>

            <div class="section-title">
                {html.escape(title)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# COUNTRY DATA
# ============================================================

def get_country_metrics(country):

    executive = filter_country(EXECUTIVE, country)
    master = filter_country(COUNTRY_MASTER, country)
    market = filter_country(MARKET_SIZING, country)
    demand = filter_country(DEMAND_MODEL, country)

    # Facility count
    facility_country = filter_country(FACILITIES, country)

    facility_count = len(facility_country)

    # Try executive first, then country master
    hd_patients = safe_value(
        executive,
        [
            "2026 HD Patients",
            "2026_HD_Patients",
            "HD Patients",
            "2026 HD Patients "
        ],
        default=None
    )

    if hd_patients is None:
        hd_patients = safe_value(
            master,
            [
                "2026 HD Patients",
                "HD Patients",
                "Chronic HD Population"
            ],
            default=None
        )

    dialysis_base = safe_value(
        executive,
        [
            "2026 Total Dialysis",
            "2026 Total Dialysis Base",
            "Total Dialysis Base"
        ],
        default=None
    )

    if dialysis_base is None:
        dialysis_base = safe_value(
            master,
            [
                "Dialysis Centers",
                "Total Dialysis Base"
            ],
            default=None
        )

    catheter_demand = safe_value(
        executive,
        [
            "Base Catheter Demand",
            "2026 Base Catheter Demand",
            "Catheter Demand"
        ],
        default=None
    )

    if catheter_demand is None:
        catheter_demand = safe_value(
            demand,
            [
                "Base Catheter Demand",
                "Total Catheter Demand"
            ],
            default=None
        )

    investment_score = safe_value(
        executive,
        [
            "Investment Score",
            "Attractiveness Score"
        ],
        default=None
    )

    asp = safe_value(
        executive,
        ["ASP", "Average Selling Price"],
        default=None
    )

    tam = safe_value(
        executive,
        ["TAM", "Total Addressable Market"],
        default=None
    )

    return {
        "hd_patients": format_number(hd_patients),
        "dialysis_base": format_number(dialysis_base),
        "catheter_demand": format_number(catheter_demand),
        "investment_score": format_number(investment_score),
        "asp": format_number(asp),
        "tam": format_number(tam),
        "facilities": format_number(facility_count)
    }


# ============================================================
# COUNTRY NAVIGATION
# ============================================================

st.sidebar.markdown(
    """
    <div class="brand-box">
        <div class="brand-title">🩺 MEA HD Intelligence</div>
        <div class="brand-subtitle">
            Hemodialysis Catheter Market Intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Country Intelligence",
        "HD Facility Intelligence",
        "Market Sizing",
        "Demand Model",
        "KOL Intelligence",
        "Hospital Intelligence",
        "Hot Areas",
        "Distributor Intelligence",
        "Competitor Intelligence",
        "Tender Intelligence",
        "Data Quality"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🌍 Country")

selected_country = st.sidebar.selectbox(
    "Select Country",
    list(COUNTRIES.keys()),
    label_visibility="collapsed"
)

country_info = COUNTRIES[selected_country]


# ============================================================
# COUNTRY TABS
# ============================================================

st.markdown(
    """
    <div style="
        font-size:12px;
        color:#64748B;
        text-transform:uppercase;
        letter-spacing:1.2px;
        margin-bottom:8px;
        font-weight:700;
    ">
        COUNTRY MARKET TABS
    </div>
    """,
    unsafe_allow_html=True
)

country_tabs = st.tabs(
    [
        f"{COUNTRIES[c]['emoji']} {c}"
        for c in COUNTRIES
    ]
)

tab_country_list = list(COUNTRIES.keys())

# The tabs act as a country overview navigation.
# The sidebar selector controls the detailed page.


# ============================================================
# MAIN HERO
# ============================================================

render_hero(selected_country)


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.markdown(
        f"""
        <h2 style="margin-bottom:4px;">
            Executive Dashboard
        </h2>

        <div style="
            color:#64748B;
            font-size:13px;
            margin-bottom:20px;
        ">
            {country_info["emoji"]} {selected_country}
            • Regional medical-device commercial intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    metrics = get_country_metrics(selected_country)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi(
            "2026 HD Patients",
            metrics["hd_patients"],
            "Verified / sourced value",
            country_info["color"]
        )

    with c2:
        kpi(
            "Total Dialysis Base",
            metrics["dialysis_base"],
            "Country dialysis infrastructure",
            country_info["color"]
        )

    with c3:
        kpi(
            "Base Catheter Demand",
            metrics["catheter_demand"],
            "Demand model",
            country_info["color"]
        )

    with c4:
        kpi(
            "Investment Score",
            metrics["investment_score"],
            "Commercial attractiveness",
            country_info["color"]
        )

    section(
        "Market Intelligence",
        country_info["color"]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi(
            "HD Facilities",
            metrics["facilities"],
            "Verified facility records",
            country_info["color"]
        )

    with c2:
        kpi(
            "ASP",
            metrics["asp"],
            "Blank where not verified",
            country_info["color"]
        )

    with c3:
        kpi(
            "TAM",
            metrics["tam"],
            "Only where supported",
            country_info["color"]
        )

    with c4:
        kpi(
            "Data Confidence",
            "Traceable",
            "Source-level evidence",
            country_info["color"]
        )

    section(
        "Country Executive Data",
        country_info["color"]
    )

    country_exec = filter_country(
        EXECUTIVE,
        selected_country
    )

    render_table(country_exec)


# ============================================================
# COUNTRY INTELLIGENCE
# ============================================================

elif page == "Country Intelligence":

    section(
        f"{selected_country} — Country Intelligence",
        country_info["color"]
    )

    country_data = get_country_csv(selected_country)

    render_table(country_data, 200)


# ============================================================
# HD FACILITIES
# ============================================================

elif page == "HD Facility Intelligence":

    section(
        f"{selected_country} — HD Facility Intelligence",
        country_info["color"]
    )

    facility_data = filter_country(
        FACILITIES,
        selected_country
    )

    if facility_data.empty:
        st.warning(
            "No HD facility records were found for this country "
            "in the uploaded facility database."
        )
    else:

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi(
                "Verified Facilities",
                format_number(len(facility_data)),
                "Facility-level records",
                country_info["color"]
            )

        with c2:
            station_count = 0

            if "HD_Stations" in facility_data.columns:
                station_count = pd.to_numeric(
                    facility_data["HD_Stations"],
                    errors="coerce"
                ).sum()

            kpi(
                "Known HD Stations",
                format_number(station_count),
                "Only populated station values",
                country_info["color"]
            )

        with c3:
            tier1 = 0

            if "Commercial_Priority" in facility_data.columns:
                tier1 = (
                    facility_data["Commercial_Priority"]
                    .astype(str)
                    .str.contains(
                        "Tier_1",
                        case=False,
                        na=False
                    )
                    .sum()
                )

            kpi(
                "Tier 1 Accounts",
                format_number(tier1),
                "Commercial priority",
                country_info["color"]
            )

        section(
            "Facility Database",
            country_info["color"]
        )

        render_table(facility_data, 500)


# ============================================================
# MARKET SIZING
# ============================================================

elif page == "Market Sizing":

    section(
        f"{selected_country} — Market Sizing",
        country_info["color"]
    )

    data = filter_country(
        MARKET_SIZING,
        selected_country
    )

    render_table(data, 300)


# ============================================================
# DEMAND MODEL
# ============================================================

elif page == "Demand Model":

    section(
        f"{selected_country} — Catheter Demand Model",
        country_info["color"]
    )

    data = filter_country(
        DEMAND_MODEL,
        selected_country
    )

    render_table(data, 300)


# ============================================================
# KOL
# ============================================================

elif page == "KOL Intelligence":

    section(
        f"{selected_country} — KOL Intelligence",
        country_info["color"]
    )

    data = filter_country(
        KOLS,
        selected_country
    )

    render_table(data, 300)


# ============================================================
# HOSPITALS
# ============================================================

elif page == "Hospital Intelligence":

    section(
        f"{selected_country} — Major Hospitals",
        country_info["color"]
    )

    data = filter_country(
        HOSPITALS,
        selected_country
    )

    render_table(data, 300)


# ============================================================
# HOT AREAS
# ============================================================

elif page == "Hot Areas":

    section(
        f"{selected_country} — HD Commercial Hot Areas",
        country_info["color"]
    )

    data = filter_country(
        HOT_AREAS,
        selected_country
    )

    render_table(data, 300)


# ============================================================
# DISTRIBUTORS
# ============================================================

elif page == "Distributor Intelligence":

    section(
        f"{selected_country} — Distributor Intelligence",
        country_info["color"]
    )

    data = filter_country(
        DISTRIBUTORS,
        selected_country
    )

    render_table(data, 300)


# ============================================================
# COMPETITORS
# ============================================================

elif page == "Competitor Intelligence":

    section(
        f"{selected_country} — Competitor Intelligence",
        country_info["color"]
    )

    data = filter_country(
        COMPETITORS,
        selected_country
    )

    render_table(data, 300)


# ============================================================
# TENDERS
# ============================================================

elif page == "Tender Intelligence":

    section(
        f"{selected_country} — Tender Intelligence",
        country_info["color"]
    )

    tender_data = filter_country(
        TENDERS,
        selected_country
    )

    sku_data = filter_country(
        TENDER_SKU,
        selected_country
    )

    nupco_data = filter_country(
        NUPCO,
        selected_country
    )

    st.markdown("#### Tender Master")

    render_table(tender_data, 300)

    st.markdown("#### Tender SKU Detail")

    render_table(sku_data, 300)

    if selected_country == "Saudi Arabia":

        st.markdown("#### NUPCO Tenders")

        render_table(nupco_data, 300)


# ============================================================
# DATA QUALITY
# ============================================================

elif page == "Data Quality":

    section(
        "Data Quality & Research Coverage",
        country_info["color"]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi(
            "Sources",
            format_number(len(SOURCES)),
            "Source register",
            country_info["color"]
        )

    with c2:
        kpi(
            "Data Gaps",
            format_number(len(DATA_GAPS)),
            "Open research gaps",
            country_info["color"]
        )

    with c3:
        kpi(
            "Audit Checks",
            format_number(len(AUDIT)),
            "QA controls",
            country_info["color"]
        )

    with c4:
        kpi(
            "Facility Records",
            format_number(len(FACILITIES)),
            "HD facility database",
            country_info["color"]
        )

    section(
        "QA Summary",
        country_info["color"]
    )

    render_table(QA, 300)

    section(
        "Data Gaps",
        country_info["color"]
    )

    render_table(DATA_GAPS, 500)

    section(
        "Audit Checks",
        country_info["color"]
    )

    render_table(AUDIT, 500)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        margin-top:50px;
        padding:20px 0;
        border-top:1px solid #1E293B;
        color:#475569;
        font-size:11px;
        text-align:center;
    ">
        MEA Hemodialysis Catheter Market Intelligence • 2026
        <br>
        Research evidence should be interpreted according to
        Evidence_Level, Confidence and Source_ID.
    </div>
    """,
    unsafe_allow_html=True
)
