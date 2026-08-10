import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import html

# ============================================================
# MEA HEMODIALYSIS CATHETER MARKET INTELLIGENCE
# Streamlit Dashboard
# ============================================================

st.set_page_config(
    page_title="MEA HD Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COUNTRY CONFIGURATION
# ============================================================

COUNTRIES = {
    "Saudi Arabia": {
        "code": "SAU",
        "flag": "saudi_arabia_flag.jpeg",
        "landscape": "saudi_landscape.jpeg",
        "accent": "#00A86B"
    },
    "UAE": {
        "code": "ARE",
        "flag": "uae_flag.jpeg",
        "landscape": "uae_landscape.jpeg",
        "accent": "#00A86B"
    },
    "Qatar": {
        "code": "QAT",
        "flag": "qatar_flag.jpeg",
        "landscape": "qatar_landscape.jpeg",
        "accent": "#8A1538"
    },
    "Kuwait": {
        "code": "KWT",
        "flag": "kuwait_flag.jpeg",
        "landscape": "kuwait_landscape.jpeg",
        "accent": "#007A3D"
    },
    "Oman": {
        "code": "OMN",
        "flag": "oman_flag.jpeg",
        "landscape": "oman_landscape.jpeg",
        "accent": "#D22630"
    },
    "Bahrain": {
        "code": "BHR",
        "flag": "bahraien_flag.jpeg",
        "landscape": "bahrain_landscape.jpg",
        "accent": "#CE1126"
    },
    "Jordan": {
        "code": "JOR",
        "flag": "jordon_flag.jpeg",
        "landscape": "jordon_landscape.jpeg",
        "accent": "#007A3D"
    },
    "Lebanon": {
        "code": "LBN",
        "flag": "lebanon_flag.jpeg",
        "landscape": "lebanon_landscape.jpeg",
        "accent": "#ED1C24"
    },
    "Iraq": {
        "code": "IRQ",
        "flag": "iraq_flag.jpeg",
        "landscape": None,
        "accent": "#CE1126"
    }
}

# ============================================================
# FILE HELPERS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


def find_file(filename):
    path = BASE_DIR / filename
    if path.exists():
        return path

    return None


def load_csv(filename):
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


def image_to_base64(filename):
    if not filename:
        return None

    path = find_file(filename)

    if path is None:
        return None

    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        extension = path.suffix.lower()

        if extension in [".jpg", ".jpeg"]:
            mime = "image/jpeg"
        elif extension == ".png":
            mime = "image/png"
        elif extension == ".webp":
            mime = "image/webp"
        else:
            mime = "image/jpeg"

        return f"data:{mime};base64,{encoded}"

    except Exception:
        return None


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(20, 80, 120, 0.16),
                transparent 35%
            ),
            #06101c;
        color: #F4F7FA;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07111f 0%,
                #091827 100%
            );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: #F4F7FA !important;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    .brand {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }

    .brand-subtitle {
        font-size: 11px;
        color: #8EA1B5 !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }

    /* ======================================================
       COUNTRY NAVIGATION
       ====================================================== */

    .country-nav-title {
        font-size: 12px;
        font-weight: 700;
        color: #8EA1B5;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        position: relative;
        min-height: 350px;
        border-radius: 24px;
        overflow: hidden;
        margin-bottom: 30px;

        background-size: cover;
        background-position: center;

        box-shadow:
            0 20px 60px rgba(0,0,0,0.40);

        border: 1px solid rgba(255,255,255,0.10);
    }

    .hero-overlay {
        position: absolute;
        inset: 0;

        background:
            linear-gradient(
                90deg,
                rgba(3,10,18,0.96) 0%,
                rgba(3,10,18,0.78) 48%,
                rgba(3,10,18,0.35) 100%
            );
    }

    .hero-content {
        position: relative;
        z-index: 2;
        padding: 48px;
        max-width: 850px;
    }

    .hero-flag {
        width: 72px;
        height: 48px;
        object-fit: cover;
        border-radius: 7px;
        border: 1px solid rgba(255,255,255,0.30);
        box-shadow: 0 5px 20px rgba(0,0,0,0.35);
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 43px;
        line-height: 1.05;
        font-weight: 850;
        color: white;
        margin-bottom: 14px;
        letter-spacing: -1.5px;
    }

    .hero-country {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .hero-description {
        font-size: 14px;
        color: #C8D2DC;
        line-height: 1.7;
    }

    /* ======================================================
       SECTION HEADERS
       ====================================================== */

    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #8295AA;
        font-size: 13px;
        margin-bottom: 20px;
    }

    /* ======================================================
       KPI CARDS
       ====================================================== */

    .kpi {
        background:
            linear-gradient(
                145deg,
                #101D2C,
                #0B1623
            );

        border-radius: 17px;
        padding: 22px;

        border: 1px solid rgba(255,255,255,0.07);

        box-shadow:
            0 10px 35px rgba(0,0,0,0.20);

        min-height: 145px;
    }

    .kpi-label {
        color: #8EA1B5;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 13px;
    }

    .kpi-value {
        color: #FFFFFF;
        font-size: 29px;
        font-weight: 850;
        margin-bottom: 7px;
    }

    .kpi-note {
        color: #71859A;
        font-size: 11px;
    }

    /* ======================================================
       COUNTRY TABS
       ====================================================== */

    button[data-baseweb="tab"] {
        background: #0D1A29 !important;
        border-radius: 9px 9px 0 0 !important;
        padding: 9px 14px !important;
        margin-right: 4px !important;
        color: #A8B8C8 !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: #14283B !important;
        color: white !important;
        font-weight: 800 !important;
    }

    /* ======================================================
       DATAFRAME
       ====================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ======================================================
       INFO BOX
       ====================================================== */

    .info-box {
        background: #0D1A29;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 15px;
        padding: 20px;
        color: #AFC0D0;
        font-size: 13px;
        line-height: 1.6;
    }

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

executive = load_csv("01_Executive_Summary.csv")
country_master = load_csv("02_Country_Master.csv")
market_sizing = load_csv("03_Market_Sizing.csv")
demand_model = load_csv("04_Demand_Model.csv")
kol_master = load_csv("05_KOL_Master.csv")
hospitals = load_csv("06_Major_Hospitals.csv")
hot_areas = load_csv("07_Hot_Areas.csv")
distributors = load_csv("08_Top_Distributors.csv")
competitors = load_csv("09_Competitor_Master.csv")
tender_sku = load_csv("10_Tender_SKU_Detail.csv")
nupco = load_csv("11_NUPCO_Tenders.csv")
tenders = load_csv("12_Tender_Master.csv")
data_gaps = load_csv("13_Data_Gaps.csv")
audit = load_csv("14_Audit_Checks.csv")
qa = load_csv("15_QA_Summary.csv")
sources = load_csv("17_Source_Register.csv")


# ============================================================
# SAFE VALUE FUNCTIONS
# ============================================================

def get_value(df, country, possible_columns):
    if df.empty:
        return None

    country_columns = [
        "Country",
        "country",
        "Country_Name",
        "Country Name"
    ]

    country_col = None

    for c in country_columns:
        if c in df.columns:
            country_col = c
            break

    if country_col is None:
        return None

    rows = df[
        df[country_col]
        .astype(str)
        .str.strip()
        .str.lower()
        == country.lower()
    ]

    if rows.empty:
        return None

    row = rows.iloc[0]

    for col in possible_columns:
        if col in row.index:
            value = row[col]

            if pd.isna(value):
                return None

            return value

    return None


def format_value(value):
    if value is None:
        return "—"

    if isinstance(value, float):
        if pd.isna(value):
            return "—"

        if value.is_integer():
            return f"{int(value):,}"

        return f"{value:,.2f}"

    try:
        numeric = float(value)

        if numeric.is_integer():
            return f"{int(numeric):,}"

        return f"{numeric:,.2f}"

    except Exception:
        return str(value)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">🩺 MEA HD Intelligence</div>
        <div class="brand-subtitle">
            Hemodialysis Catheter Market Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Dashboard")

    page = st.radio(
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

    st.markdown("---")

    st.markdown(
        '<div class="country-nav-title">Country</div>',
        unsafe_allow_html=True
    )

    selected_country = st.selectbox(
        "Country",
        list(COUNTRIES.keys()),
        label_visibility="collapsed"
    )


# ============================================================
# HERO
# ============================================================

country = COUNTRIES[selected_country]

landscape = image_to_base64(country["landscape"])
flag = image_to_base64(country["flag"])

if landscape:
    hero_style = (
        f"background-image:url('{landscape}');"
    )
else:
    hero_style = (
        "background:linear-gradient(135deg,#0C1C2D,#102A3D);"
    )

flag_html = ""

if flag:
    flag_html = (
        f'<img class="hero-flag" src="{flag}" '
        f'alt="{html.escape(selected_country)} flag">'
    )

st.markdown(
    f"""
    <div class="hero" style="{hero_style}">
        <div class="hero-overlay"></div>

        <div class="hero-content">

            {flag_html}

            <div class="hero-title">
                MEA Hemodialysis<br>
                Catheter Market Intelligence
            </div>

            <div class="hero-country"
                 style="color:{country["accent"]};">
                {html.escape(selected_country)}
                ({country["code"]})
            </div>

            <div class="hero-description">
                2026 Medical Device Commercial Intelligence
                <br>
                Hemodialysis • Vascular Access • Catheter Market
            </div>

        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.markdown(
        '<div class="section-title">Executive Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="section-subtitle">
            {html.escape(selected_country)} medical-device commercial intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    hd_patients = get_value(
        executive,
        selected_country,
        ["2026 HD Patients", "HD Patients", "2026_HD_Patients"]
    )

    dialysis = get_value(
        executive,
        selected_country,
        [
            "2026 Total Dialysis",
            "Total Dialysis",
            "2026 Total Dialysis Base"
        ]
    )

    catheter = get_value(
        executive,
        selected_country,
        [
            "Base Catheter Demand",
            "2026 Base Catheter Demand",
            "Total Catheter Demand"
        ]
    )

    investment = get_value(
        executive,
        selected_country,
        [
            "Investment Score",
            "Investment_Score"
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">2026 HD Patients</div>
                <div class="kpi-value">{format_value(hd_patients)}</div>
                <div class="kpi-note">Verified / sourced value</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">Total Dialysis Base</div>
                <div class="kpi-value">{format_value(dialysis)}</div>
                <div class="kpi-note">Country dialysis infrastructure</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">Base Catheter Demand</div>
                <div class="kpi-value">{format_value(catheter)}</div>
                <div class="kpi-note">Demand model</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">Investment Score</div>
                <div class="kpi-value">{format_value(investment)}</div>
                <div class="kpi-note">Commercial attractiveness</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
        <b>Research Integrity:</b>
        Blank or unavailable commercial metrics remain blank rather than
        being estimated. Historical observations are not automatically
        converted into 2026 observations.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# COUNTRY INTELLIGENCE
# ============================================================

elif page == "Country Intelligence":

    st.markdown(
        '<div class="section-title">Country Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Country-level market master data</div>',
        unsafe_allow_html=True
    )

    if not country_master.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in country_master.columns
            ),
            None
        )

        if country_col:

            country_data = country_master[
                country_master[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            if not country_data.empty:
                st.dataframe(
                    country_data,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No country-level record found.")

    else:
        st.warning("02_Country_Master.csv was not found or contains no data.")


# ============================================================
# GENERIC DATA PAGES
# ============================================================

elif page == "HD Facility Intelligence":

    st.markdown(
        '<div class="section-title">HD Facility Intelligence</div>',
        unsafe_allow_html=True
    )

    facility = load_csv("07_HD_Facility_Master.csv")

    if facility.empty:
        facility = load_csv("HD_Facility_Master.csv")

    if not facility.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in facility.columns
            ),
            None
        )

        if country_col:

            filtered = facility[
                facility[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            st.metric(
                "Verified Facilities",
                len(filtered)
            )

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.dataframe(
                facility,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning(
            "HD Facility Master CSV was not found. "
            "Add the facility database to the repository."
        )


elif page == "Market Sizing":

    st.markdown(
        '<div class="section-title">Market Sizing</div>',
        unsafe_allow_html=True
    )

    if not market_sizing.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in market_sizing.columns
            ),
            None
        )

        if country_col:
            filtered = market_sizing[
                market_sizing[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(
                market_sizing,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("Market sizing data unavailable.")


elif page == "Demand Model":

    st.markdown(
        '<div class="section-title">Demand Model</div>',
        unsafe_allow_html=True
    )

    if not demand_model.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in demand_model.columns
            ),
            None
        )

        if country_col:

            filtered = demand_model[
                demand_model[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.dataframe(
                demand_model,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("Demand model data unavailable.")


elif page == "KOL Intelligence":

    st.markdown(
        '<div class="section-title">KOL Intelligence</div>',
        unsafe_allow_html=True
    )

    if not kol_master.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in kol_master.columns
            ),
            None
        )

        if country_col:
            filtered = kol_master[
                kol_master[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(
                kol_master,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("KOL data unavailable.")


elif page == "Hospital Intelligence":

    st.markdown(
        '<div class="section-title">Hospital Intelligence</div>',
        unsafe_allow_html=True
    )

    if not hospitals.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in hospitals.columns
            ),
            None
        )

        if country_col:
            filtered = hospitals[
                hospitals[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(
                hospitals,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("Hospital data unavailable.")


elif page == "Hot Areas":

    st.markdown(
        '<div class="section-title">HD Hot Areas</div>',
        unsafe_allow_html=True
    )

    if not hot_areas.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in hot_areas.columns
            ),
            None
        )

        if country_col:
            filtered = hot_areas[
                hot_areas[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(
                hot_areas,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("Hot-area data unavailable.")


elif page == "Distributor Intelligence":

    st.markdown(
        '<div class="section-title">Distributor Intelligence</div>',
        unsafe_allow_html=True
    )

    if not distributors.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in distributors.columns
            ),
            None
        )

        if country_col:
            filtered = distributors[
                distributors[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(
                distributors,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("Distributor data unavailable.")


elif page == "Competitor Intelligence":

    st.markdown(
        '<div class="section-title">Competitor Intelligence</div>',
        unsafe_allow_html=True
    )

    if not competitors.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in competitors.columns
            ),
            None
        )

        if country_col:
            filtered = competitors[
                competitors[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(
                competitors,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("Competitor data unavailable.")


elif page == "Tender Intelligence":

    st.markdown(
        '<div class="section-title">Tender Intelligence</div>',
        unsafe_allow_html=True
    )

    data = tenders

    if data.empty:
        data = nupco

    if not data.empty:

        country_col = next(
            (
                c for c in
                ["Country", "country", "Country_Name"]
                if c in data.columns
            ),
            None
        )

        if country_col:
            filtered = data[
                data[country_col].astype(str).str.strip().str.lower()
                == selected_country.lower()
            ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(
                data,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("Tender data unavailable.")


elif page == "Data Quality":

    st.markdown(
        '<div class="section-title">Data Quality</div>',
        unsafe_allow_html=True
    )

    if not qa.empty:
        st.dataframe(
            qa,
            use_container_width=True,
            hide_index=True
        )

    if not audit.empty:
        st.markdown(
            '<div class="section-title">Audit Checks</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            audit,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br><br>
    <div style="
        text-align:center;
        color:#53677B;
        font-size:11px;
        padding:20px;
        border-top:1px solid rgba(255,255,255,0.06);
    ">
        MEA Hemodialysis Catheter Market Intelligence • 2026
        <br>
        Research integrity priority: sourced data is distinguished
        from derived and analyst-scenario information.
    </div>
    """,
    unsafe_allow_html=True
)
