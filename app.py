import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MEA Hemodialysis Catheter Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# ROOT
# =========================================================

ROOT = Path(__file__).resolve().parent


# =========================================================
# COUNTRY CONFIG
# EXACT FILENAMES FROM YOUR GITHUB REPOSITORY
# =========================================================

COUNTRIES = {

    "Saudi Arabia": {
        "code": "SAU",
        "flag": "saudi_arabia_flag.jpeg",
        "landscape": "saudi_landscape.jpeg",
        "csv": "18_SAU_Country.csv"
    },

    "UAE": {
        "code": "ARE",
        "flag": "uae_flag.jpeg",
        "landscape": "uae_landscape.jpeg",
        "csv": "19_ARE_Country.csv"
    },

    "Qatar": {
        "code": "QAT",
        "flag": "qatar_flag.jpeg",
        "landscape": "qatar_landscape.jpeg",
        "csv": "20_QAT_Country.csv"
    },

    "Kuwait": {
        "code": "KWT",
        "flag": "kuwait_flag.jpeg",
        "landscape": "kuwait_landscape.jpeg",
        "csv": "21_KWT_Country.csv"
    },

    "Oman": {
        "code": "OMN",
        "flag": "oman_flag.jpeg",
        "landscape": "oman_landscape.jpeg",
        "csv": "22_OMN_Country.csv"
    },

    "Bahrain": {
        "code": "BHR",
        "flag": "bahraien_flag.jpeg",
        "landscape": "bahrain_landscape.jpg",
        "csv": "23_BHR_Country.csv"
    },

    "Jordan": {
        "code": "JOR",
        "flag": "jordon_flag.jpeg",
        "landscape": "jordon_landscape.jpeg",
        "csv": "24_JOR_Country.csv"
    },

    "Lebanon": {
        "code": "LBN",
        "flag": "lebanon_flag.jpeg",
        "landscape": "lebanon_landscape.jpeg",
        "csv": "25_LBN_Country.csv"
    },

    "Iraq": {
        "code": "IRQ",
        "flag": None,
        "landscape": None,
        "csv": "26_IRQ_Country.csv"
    }
}


# =========================================================
# DATA FILES
# =========================================================

DATASETS = {

    "Executive Summary": "01_Executive_Summary.csv",
    "Country Master": "02_Country_Master.csv",
    "Market Sizing": "03_Market_Sizing.csv",
    "Demand Model": "04_Demand_Model.csv",
    "KOL Master": "05_KOL_Master.csv",
    "Major Hospitals": "06_Major_Hospitals.csv",
    "Hot Areas": "07_Hot_Areas.csv",
    "Top Distributors": "08_Top_Distributors.csv",
    "Competitors": "09_Competitor_Master.csv",
    "Tender SKU Detail": "10_Tender_SKU_Detail.csv",
    "NUPCO Tenders": "11_NUPCO_Tenders.csv",
    "Tender Master": "12_Tender_Master.csv",
    "Data Gaps": "13_Data_Gaps.csv",
    "Audit Checks": "14_Audit_Checks.csv",
    "QA Summary": "15_QA_Summary.csv",
    "Data Dictionary": "16_Data_Dictionary.csv",
    "Source Register": "17_Source_Register.csv"
}


# =========================================================
# HELPERS
# =========================================================

def read_csv(filename):

    path = ROOT / filename

    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(
            path,
            encoding="utf-8-sig"
        )

    except Exception:

        try:
            return pd.read_csv(
                path,
                encoding="utf-8"
            )

        except Exception:
            return pd.DataFrame()


def image_base64(filename):

    if not filename:
        return None

    path = ROOT / filename

    if not path.exists():
        return None

    try:

        encoded = base64.b64encode(
            path.read_bytes()
        ).decode()

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


def country_filter(df, country):

    if df.empty:
        return df

    possible = [
        "Country",
        "country",
        "Country_Name"
    ]

    column = None

    for c in possible:

        if c in df.columns:
            column = c
            break

    if column is None:
        return df

    return df[
        df[column]
        .astype(str)
        .str.strip()
        .str.lower()
        == country.lower()
    ]


def find_column(df, names):

    for name in names:

        for column in df.columns:

            if str(column).strip().lower() == name.lower():
                return column

    return None


def get_value(row, names):

    if row is None:
        return "—"

    for name in names:

        if name in row.index:

            value = row[name]

            if pd.notna(value) and str(value).strip() != "":
                return value

    return "—"


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #f4f7fb;
}

[data-testid="stSidebar"] {
    background-color: #0b1220;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {

    height: 340px;

    border-radius: 25px;

    background-size: cover;

    background-position: center;

    overflow: hidden;

    margin-bottom: 25px;

    box-shadow:
        0 15px 45px rgba(0,0,0,.20);
}

.hero-overlay {

    height: 100%;

    padding: 50px;

    display: flex;

    flex-direction: column;

    justify-content: flex-end;

    background:
        linear-gradient(
            90deg,
            rgba(0,0,0,.82),
            rgba(0,0,0,.42),
            rgba(0,0,0,.10)
        );
}

.hero-title {

    color: white;

    font-size: 40px;

    font-weight: 800;

    line-height: 1.1;

}

.hero-subtitle {

    color: #e5e7eb;

    font-size: 18px;

    margin-top: 8px;

}

.flag {

    width: 85px;

    height: 55px;

    object-fit: cover;

    border-radius: 8px;

    margin-bottom: 15px;

    box-shadow:
        0 5px 18px rgba(0,0,0,.35);
}

.card {

    background: white;

    border-radius: 18px;

    padding: 22px;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 5px 20px rgba(0,0,0,.05);

    min-height: 125px;

}

.card-title {

    font-size: 13px;

    font-weight: 700;

    color: #64748b;

    text-transform: uppercase;

}

.card-value {

    font-size: 30px;

    font-weight: 800;

    color: #0f172a;

    margin-top: 8px;

}

.section {

    font-size: 26px;

    font-weight: 800;

    color: #0f172a;

    margin-top: 30px;

    margin-bottom: 15px;

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:24px;
            font-weight:800;
            margin-bottom:25px;">
            🩺 MEA HD Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "Dashboard",
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
        ]
    )

    st.markdown("---")

    country_name = st.selectbox(
        "🌍 Country",
        list(COUNTRIES.keys())
    )


country = COUNTRIES[country_name]


# =========================================================
# HERO IMAGE
# =========================================================

landscape = image_base64(
    country["landscape"]
)


flag = image_base64(
    country["flag"]
)


if landscape:

    background = (
        f"background-image:url('{landscape}');"
    )

else:

    background = (
        "background:linear-gradient("
        "135deg,#0f172a,#1d4ed8);"
    )


flag_html = ""

if flag:

    flag_html = (
        f"<img class='flag' src='{flag}'>"
    )


st.markdown(
    f"""
    <div class="hero" style="{background}">

        <div class="hero-overlay">

            {flag_html}

            <div class="hero-title">
                MEA Hemodialysis Catheter
                Market Intelligence
            </div>

            <div class="hero-subtitle">
                {country_name}
                ({country["code"]})
                • 2026 Market Intelligence Dashboard
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# EXECUTIVE DASHBOARD
# =========================================================

if page == "Executive Dashboard":

    st.markdown(
        '<div class="section">Executive Dashboard</div>',
        unsafe_allow_html=True
    )

    df = read_csv(
        DATASETS["Executive Summary"]
    )

    filtered = country_filter(
        df,
        country_name
    )

    if filtered.empty:

        st.warning(
            "No country-specific Executive Summary record found."
        )

    else:

        row = filtered.iloc[0]

        c1, c2, c3, c4 = st.columns(4)

        cards = [

            (
                "2026 HD Patients",
                [
                    "2026 HD Patients",
                    "HD Patients 2026",
                    "HD_Patients_2026"
                ]
            ),

            (
                "Total Dialysis",
                [
                    "2026 Total Dialysis",
                    "Total Dialysis",
                    "Total_Dialysis"
                ]
            ),

            (
                "Base Catheter Demand",
                [
                    "Base Catheter Demand",
                    "Catheter Demand",
                    "Base_Catheter_Demand"
                ]
            ),

            (
                "Investment Grade",
                [
                    "Investment Grade",
                    "Investment_Grade"
                ]
            )

        ]

        for col, (title, candidates) in zip(
            [c1,c2,c3,c4],
            cards
        ):

            value = get_value(
                row,
                candidates
            )

            with col:

                st.markdown(
                    f"""
                    <div class="card">

                        <div class="card-title">
                            {title}
                        </div>

                        <div class="card-value">
                            {html.escape(str(value))}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            '<div class="section">Country Executive Data</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# COUNTRY INTELLIGENCE
# =========================================================

elif page == "Country Intelligence":

    st.markdown(
        '<div class="section">Country Intelligence</div>',
        unsafe_allow_html=True
    )

    df = read_csv(
        country["csv"]
    )

    if df.empty:

        st.error(
            f"Could not load {country['csv']}"
        )

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# HD FACILITY INTELLIGENCE
# =========================================================

elif page == "HD Facility Intelligence":

    st.markdown(
        '<div class="section">HD Facility Intelligence</div>',
        unsafe_allow_html=True
    )

    df = read_csv(
        "06_Major_Hospitals.csv"
    )

    filtered = country_filter(
        df,
        country_name
    )

    st.metric(
        "Verified Facility / Hospital Records",
        len(filtered)
    )

    if filtered.empty:

        st.info(
            "No facility records were found for this country "
            "in the current dataset."
        )

    else:

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# OTHER DATA PAGES
# =========================================================

PAGE_MAP = {

    "Market Sizing":
        "Market Sizing",

    "Demand Model":
        "Demand Model",

    "KOL Intelligence":
        "KOL Master",

    "Hospital Intelligence":
        "Major Hospitals",

    "Hot Areas":
        "Hot Areas",

    "Distributor Intelligence":
        "Top Distributors",

    "Competitor Intelligence":
        "Competitors",

    "Tender Intelligence":
        "Tender Master",

    "Data Quality":
        "QA Summary"
}


if page in PAGE_MAP:

    dataset_name = PAGE_MAP[page]

    filename = DATASETS[dataset_name]

    df = read_csv(filename)

    st.markdown(
        f'<div class="section">{page}</div>',
        unsafe_allow_html=True
    )

    filtered = country_filter(
        df,
        country_name
    )

    if not filtered.empty:

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

    elif not df.empty:

        st.info(
            "This table does not contain a Country column "
            "or no country-specific record was found. "
            "Showing available data."
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.error(
            f"Could not load {filename}"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <br>

    <div style="
        text-align:center;
        color:#64748b;
        padding:25px;
        font-size:12px;">

        MEA Hemodialysis Catheter Market Intelligence
        • 2026

    </div>
    """,
    unsafe_allow_html=True
)
