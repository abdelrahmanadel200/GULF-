import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
from PIL import Image


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MEA Hemodialysis Catheter Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
FLAGS_DIR = BASE_DIR / "assets" / "flags"
LANDSCAPE_DIR = BASE_DIR / "assets" / "landscapes"


# ============================================================
# COUNTRY CONFIGURATION
# ============================================================

COUNTRIES = {
    "Saudi Arabia": {
        "code": "SAU",
        "flag": "SAU.png",
        "landscape": "SAU.jpg",
        "currency": "SAR"
    },
    "United Arab Emirates": {
        "code": "ARE",
        "flag": "ARE.png",
        "landscape": "ARE.jpg",
        "currency": "AED"
    },
    "Qatar": {
        "code": "QAT",
        "flag": "QAT.png",
        "landscape": "QAT.jpg",
        "currency": "QAR"
    },
    "Kuwait": {
        "code": "KWT",
        "flag": "KWT.png",
        "landscape": "KWT.jpg",
        "currency": "KWD"
    },
    "Oman": {
        "code": "OMN",
        "flag": "OMN.png",
        "landscape": "OMN.jpg",
        "currency": "OMR"
    },
    "Bahrain": {
        "code": "BHR",
        "flag": "BHR.png",
        "landscape": "BHR.jpg",
        "currency": "BHD"
    },
    "Jordan": {
        "code": "JOR",
        "flag": "JOR.png",
        "landscape": "JOR.jpg",
        "currency": "JOD"
    },
    "Lebanon": {
        "code": "LBN",
        "flag": "LBN.png",
        "landscape": "LBN.jpg",
        "currency": "LBP"
    },
    "Iraq": {
        "code": "IRQ",
        "flag": "IRQ.png",
        "landscape": "IRQ.jpg",
        "currency": "IQD"
    }
}


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #f4f7fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        min-height: 120px;
    }

    .kpi-title {
        font-size: 13px;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 800;
        color: #111827;
        margin-top: 5px;
    }

    .hero {
        border-radius: 20px;
        padding: 35px;
        min-height: 260px;
        background-size: cover;
        background-position: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 25px;
    }

    .hero-overlay {
        background: rgba(0,0,0,0.48);
        position: absolute;
        inset: 0;
    }

    .hero-content {
        position: relative;
        z-index: 2;
        color: white;
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 17px;
        opacity: 0.9;
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        background: rgba(255,255,255,0.18);
        margin-top: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_csv(filename):

    path = DATA_DIR / filename

    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


executive = load_csv("01_Executive_Summary.csv")
country_master = load_csv("02_Country_Master.csv")
market_sizing = load_csv("03_Market_Sizing.csv")
demand_model = load_csv("04_Demand_Model.csv")
kol_master = load_csv("05_KOL_Master.csv")
hospitals = load_csv("06_Major_Hospitals.csv")
facilities = load_csv("07_HD_Facility_Master.csv")
facility_summary = load_csv("08_HD_Facility_Summary.csv")
hot_areas = load_csv("09_Hot_Areas.csv")
distributors = load_csv("10_Top_Distributors.csv")
competitors = load_csv("11_Competitor_Master.csv")
tenders = load_csv("12_Tender_Master.csv")
tender_sku = load_csv("13_Tender_SKU_Detail.csv")
nupco = load_csv("14_NUPCO_Tenders.csv")
data_gaps = load_csv("15_Data_Gaps.csv")
facility_gaps = load_csv("16_HD_Facility_Data_Gaps.csv")
audit = load_csv("17_Audit_Checks.csv")
qa = load_csv("18_QA_Summary.csv")
dictionary = load_csv("19_Data_Dictionary.csv")
sources = load_csv("20_Source_Register.csv")
facility_sources = load_csv("21_HD_Facility_Source_Register.csv")


# ============================================================
# HELPERS
# ============================================================

def find_column(df, names):

    if df.empty:
        return None

    normalized = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in names:
        if name.lower() in normalized:
            return normalized[name.lower()]

    return None


def country_filter(df, country, code):

    if df.empty:
        return df

    country_col = find_column(df, ["Country"])

    if country_col:
        result = df[
            df[country_col].astype(str).str.strip().str.lower()
            == country.lower()
        ]

        if not result.empty:
            return result

    code_col = find_column(df, ["Country_Code"])

    if code_col:
        return df[
            df[code_col].astype(str).str.strip().str.upper()
            == code.upper()
        ]

    return pd.DataFrame()


def safe_number(df, column_names):

    col = find_column(df, column_names)

    if col is None:
        return None

    values = pd.to_numeric(df[col], errors="coerce")

    if values.notna().any():
        return values.sum()

    return None


def display_kpi(title, value):

    if value is None or pd.isna(value):
        value = "N/A"

    elif isinstance(value, (int, float, np.integer, np.floating)):
        if float(value).is_integer():
            value = f"{int(value):,}"
        else:
            value = f"{float(value):,.1f}"

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_image(path):

    if path.exists():
        return str(path)

    return None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <h2 style="color:white;">
    🩺 MEA HD Intelligence
    </h2>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Dashboard",
    [
        "Executive Overview",
        "Country Intelligence",
        "HD Facilities",
        "Market Sizing",
        "Demand Model",
        "KOL Intelligence",
        "Hospitals",
        "Hot Areas",
        "Distributors",
        "Competitors",
        "Tenders",
        "Data Quality"
    ]
)


selected_country = st.sidebar.selectbox(
    "Select Country",
    list(COUNTRIES.keys())
)

country_info = COUNTRIES[selected_country]
country_code = country_info["code"]


# ============================================================
# COUNTRY HERO
# ============================================================

def country_hero(country):

    info = COUNTRIES[country]

    landscape = LANDSCAPE_DIR / info["landscape"]
    flag = FLAGS_DIR / info["flag"]

    if landscape.exists():

        background = landscape.as_posix()

        flag_html = ""

        if flag.exists():
            flag_html = f"""
            <img
                src="data:image/png;base64,{__import__('base64').b64encode(flag.read_bytes()).decode()}"
                width="80"
                style="border-radius:8px;margin-bottom:15px;"
            >
            """

        st.markdown(
            f"""
            <div class="hero"
                 style="background-image:url('data:image/jpeg;base64,{__import__('base64').b64encode(landscape.read_bytes()).decode()}');">

                <div class="hero-overlay"></div>

                <div class="hero-content">

                    {flag_html}

                    <div class="hero-title">
                        {country}
                    </div>

                    <div class="hero-subtitle">
                        Hemodialysis Catheter Market Intelligence
                    </div>

                    <div class="badge">
                        Country Code: {info['code']}
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.title("MEA Hemodialysis Catheter Market Intelligence")

    st.markdown(
        """
        ### Regional Commercial Intelligence Dashboard

        **9-country Middle East & Africa hemodialysis catheter market**
        """
    )

    if not executive.empty:

        st.dataframe(
            executive,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Executive_Summary.csv was not found or contains no data."
        )


# ============================================================
# COUNTRY INTELLIGENCE
# ============================================================

elif page == "Country Intelligence":

    country_hero(selected_country)

    st.markdown(
        '<div class="section-title">Country Snapshot</div>',
        unsafe_allow_html=True
    )

    c_country = country_filter(
        country_master,
        selected_country,
        country_code
    )

    c_exec = country_filter(
        executive,
        selected_country,
        country_code
    )

    c_facilities = country_filter(
        facilities,
        selected_country,
        country_code
    )

    c_hot = country_filter(
        hot_areas,
        selected_country,
        country_code
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        display_kpi(
            "HD Facilities",
            len(c_facilities) if not c_facilities.empty else None
        )

    with col2:
        display_kpi(
            "HD Patients",
            safe_number(
                c_exec,
                ["2026 HD Patients", "HD Patients"]
            )
        )

    with col3:
        display_kpi(
            "Dialysis Centers",
            safe_number(
                c_country,
                ["Dialysis centers", "Dialysis Centers"]
            )
        )

    with col4:
        display_kpi(
            "KRT Population",
            safe_number(
                c_country,
                ["KRT / ESRD population", "KRT"]
            )
        )

    st.markdown(
        '<div class="section-title">Country Data</div>',
        unsafe_allow_html=True
    )

    if not c_country.empty:
        st.dataframe(
            c_country,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# HD FACILITIES
# ============================================================

elif page == "HD Facilities":

    country_hero(selected_country)

    st.title("Verified HD Facility Intelligence")

    c_facilities = country_filter(
        facilities,
        selected_country,
        country_code
    )

    if c_facilities.empty:

        st.warning(
            "No facility records were found for this country."
        )

    else:

        col1, col2, col3 = st.columns(3)

        with col1:
            display_kpi(
                "Verified Facilities",
                len(c_facilities)
            )

        station_col = find_column(
            c_facilities,
            ["HD_Stations", "HD Stations"]
        )

        with col2:
            if station_col:
                stations = pd.to_numeric(
                    c_facilities[station_col],
                    errors="coerce"
                ).sum()
            else:
                stations = None

            display_kpi(
                "Known HD Stations",
                stations
            )

        type_col = find_column(
            c_facilities,
            ["Facility_Type", "Facility Type"]
        )

        with col3:

            if type_col:
                hospital_count = (
                    c_facilities[type_col]
                    .astype(str)
                    .str.contains(
                        "hospital",
                        case=False,
                        na=False
                    )
                    .sum()
                )
            else:
                hospital_count = None

            display_kpi(
                "Hospitals / Hospital Units",
                hospital_count
            )

        st.markdown(
            '<div class="section-title">Facility Database</div>',
            unsafe_allow_html=True
        )

        search = st.text_input(
            "Search facility, city, region or hospital"
        )

        filtered = c_facilities.copy()

        if search:

            mask = filtered.astype(str).apply(
                lambda row: row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )

            filtered = filtered[mask]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        csv = filtered.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "Download Country Facility Data",
            csv,
            file_name=f"{country_code}_HD_Facilities.csv",
            mime="text/csv"
        )


# ============================================================
# MARKET SIZING
# ============================================================

elif page == "Market Sizing":

    country_hero(selected_country)

    st.title("Market Sizing")

    c_market = country_filter(
        market_sizing,
        selected_country,
        country_code
    )

    if c_market.empty:

        st.warning(
            "No market sizing data available."
        )

    else:

        st.dataframe(
            c_market,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Blank TAM/SAM/SOM values are intentionally preserved "
            "when ASP or addressable-unit evidence is unavailable."
        )


# ============================================================
# DEMAND MODEL
# ============================================================

elif page == "Demand Model":

    country_hero(selected_country)

    st.title("Hemodialysis Catheter Demand Model")

    c_demand = country_filter(
        demand_model,
        selected_country,
        country_code
    )

    if c_demand.empty:

        st.warning(
            "No demand-model data available."
        )

    else:

        st.dataframe(
            c_demand,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# KOL INTELLIGENCE
# ============================================================

elif page == "KOL Intelligence":

    country_hero(selected_country)

    st.title("Key Opinion Leader Intelligence")

    c_kol = country_filter(
        kol_master,
        selected_country,
        country_code
    )

    if c_kol.empty:

        st.warning(
            "No verified KOL records available."
        )

    else:

        st.dataframe(
            c_kol,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# HOSPITALS
# ============================================================

elif page == "Hospitals":

    country_hero(selected_country)

    st.title("Major Hospitals")

    c_hospitals = country_filter(
        hospitals,
        selected_country,
        country_code
    )

    if c_hospitals.empty:

        st.warning(
            "No hospital records available."
        )

    else:

        st.dataframe(
            c_hospitals,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# HOT AREAS
# ============================================================

elif page == "Hot Areas":

    country_hero(selected_country)

    st.title("HD Commercial Hot Areas")

    c_hot = country_filter(
        hot_areas,
        selected_country,
        country_code
    )

    if c_hot.empty:

        st.warning(
            "No hot-area data available."
        )

    else:

        st.dataframe(
            c_hot,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# DISTRIBUTORS
# ============================================================

elif page == "Distributors":

    country_hero(selected_country)

    st.title("Distributor Intelligence")

    c_dist = country_filter(
        distributors,
        selected_country,
        country_code
    )

    if c_dist.empty:

        st.warning(
            "No verified distributor records available."
        )

    else:

        st.dataframe(
            c_dist,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# COMPETITORS
# ============================================================

elif page == "Competitors":

    country_hero(selected_country)

    st.title("Competitor & Manufacturer Intelligence")

    c_comp = country_filter(
        competitors,
        selected_country,
        country_code
    )

    if c_comp.empty:

        st.warning(
            "No competitor data available."
        )

    else:

        st.dataframe(
            c_comp,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# TENDERS
# ============================================================

elif page == "Tenders":

    country_hero(selected_country)

    st.title("Tender Intelligence")

    c_tenders = country_filter(
        tenders,
        selected_country,
        country_code
    )

    if c_tenders.empty:

        st.warning(
            "No tender records available."
        )

    else:

        st.dataframe(
            c_tenders,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# DATA QUALITY
# ============================================================

elif page == "Data Quality":

    st.title("Research Integrity & QA")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        display_kpi(
            "Countries",
            9
        )

    with col2:
        display_kpi(
            "Facility Records",
            len(facilities)
        )

    with col3:
        display_kpi(
            "Sources",
            len(sources)
        )

    with col4:
        display_kpi(
            "Data Gaps",
            len(data_gaps)
        )

    st.markdown(
        '<div class="section-title">QA Summary</div>',
        unsafe_allow_html=True
    )

    if not qa.empty:

        st.dataframe(
            qa,
            use_container_width=True,
            hide_index=True
        )

    st.markdown(
        '<div class="section-title">Audit Checks</div>',
        unsafe_allow_html=True
    )

    if not audit.empty:

        st.dataframe(
            audit,
            use_container_width=True,
            hide_index=True
        )
