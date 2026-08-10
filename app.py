import streamlit as st
import pandas as pd
from pathlib import Path
import base64

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
        "country_csv": "18_SAU_Country.csv"
    },
    "United Arab Emirates": {
        "code": "ARE",
        "flag": "uae_flag.jpeg",
        "landscape": "uae_landscape.jpeg",
        "country_csv": "19_ARE_Country.csv"
    },
    "Qatar": {
        "code": "QAT",
        "flag": "qatar_flag.jpeg",
        "landscape": "qatar_landscape.jpeg",
        "country_csv": "20_QAT_Country.csv"
    },
    "Kuwait": {
        "code": "KWT",
        "flag": "kuwait_flag.jpeg",
        "landscape": "kuwait_landscape.jpeg",
        "country_csv": "21_KWT_Country.csv"
    },
    "Oman": {
        "code": "OMN",
        "flag": "oman_flag.jpeg",
        "landscape": "oman_landscape.jpeg",
        "country_csv": "22_OMN_Country.csv"
    },
    "Bahrain": {
        "code": "BHR",
        "flag": "bahraien_flag.jpeg",
        "landscape": "bahrain_landscape.jpg",
        "country_csv": "23_BHR_Country.csv"
    },
    "Jordan": {
        "code": "JOR",
        "flag": "jordon_flag.jpeg",
        "landscape": "jordon_landscape.jpeg",
        "country_csv": "24_JOR_Country.csv"
    },
    "Lebanon": {
        "code": "LBN",
        "flag": "lebanon_flag.jpeg",
        "landscape": "lebanon_landscape.jpeg",
        "country_csv": "25_LBN_Country.csv"
    },
    "Iraq": {
        "code": "IRQ",
        "flag": "iraq_flag.jpeg",
        "landscape": "iraq_landscape.jpeg",
        "country_csv": "26_IRQ_Country.csv"
    }
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def file_exists(filename):
    return Path(filename).exists()


def image_to_base64(filename):
    """
    Convert local image to base64 so it can be used
    inside CSS/HTML without external hosting.
    """
    path = Path(filename)

    if not path.exists():
        return None

    try:
        data = path.read_bytes()
        encoded = base64.b64encode(data).decode()

        suffix = path.suffix.lower()

        if suffix in [".jpg", ".jpeg"]:
            mime = "image/jpeg"
        elif suffix == ".png":
            mime = "image/png"
        elif suffix == ".webp":
            mime = "image/webp"
        else:
            mime = "image/jpeg"

        return f"data:{mime};base64,{encoded}"

    except Exception:
        return None


@st.cache_data
def load_csv(filename):
    path = Path(filename)

    if not path.exists():
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
                encoding="latin1",
                low_memory=False
            )
        except Exception:
            return pd.DataFrame()


def clean_number(value):
    if pd.isna(value):
        return None

    try:
        return float(str(value).replace(",", "").replace(" ", ""))
    except Exception:
        return None


def find_column(df, possible_names):
    """
    Find a column even if the CSV has slightly different
    capitalization/spacing.
    """

    if df.empty:
        return None

    normalized = {
        str(c).strip().lower().replace(" ", "_"): c
        for c in df.columns
    }

    for name in possible_names:
        key = name.lower().replace(" ", "_")

        if key in normalized:
            return normalized[key]

    return None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

    /* Main application */
    .stApp {
        background: #f5f7fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0b1220;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Main title */
    .main-title {
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .main-subtitle {
        color: #667085;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* KPI cards */
    .kpi {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 5px 20px rgba(15, 23, 42, 0.08);
        border: 1px solid #e7eaf0;
        min-height: 120px;
    }

    .kpi-label {
        color: #667085;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .5px;
    }

    .kpi-value {
        font-size: 29px;
        font-weight: 800;
        color: #101828;
        margin-top: 8px;
    }

    .kpi-note {
        font-size: 12px;
        color: #98a2b3;
        margin-top: 4px;
    }

    /* Section */
    .section-title {
        font-size: 23px;
        font-weight: 800;
        color: #101828;
        margin-top: 25px;
        margin-bottom: 12px;
    }

</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:24px;
        font-weight:800;
        margin-bottom:5px;
    ">
    🩺 MEA HD Intelligence
    </div>

    <div style="
        color:#98A2B3;
        font-size:12px;
        margin-bottom:25px;
    ">
    Hemodialysis Catheter Market Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
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

st.sidebar.markdown("---")

selected_country = st.sidebar.selectbox(
    "🌍 Country",
    list(COUNTRIES.keys())
)

country = COUNTRIES[selected_country]

# ============================================================
# EXECUTIVE HERO
# ============================================================

landscape_b64 = image_to_base64(country["landscape"])
flag_b64 = image_to_base64(country["flag"])

if landscape_b64:

    flag_html = ""

    if flag_b64:
        flag_html = f"""
        <img src="{flag_b64}"
             style="
                width:70px;
                height:45px;
                object-fit:cover;
                border-radius:5px;
                border:1px solid rgba(255,255,255,.6);
                margin-bottom:15px;
             ">
        """

    hero_html = f"""
    <div style="
        position:relative;
        height:330px;
        border-radius:24px;
        overflow:hidden;
        margin-bottom:30px;
        background-image:
            linear-gradient(
                90deg,
                rgba(5,10,20,.92) 0%,
                rgba(5,10,20,.72) 45%,
                rgba(5,10,20,.35) 100%
            ),
            url('{landscape_b64}');
        background-size:cover;
        background-position:center;
        box-shadow:0 12px 40px rgba(0,0,0,.18);
    ">

        <div style="
            position:absolute;
            left:45px;
            top:50%;
            transform:translateY(-50%);
            color:white;
        ">

            {flag_html}

            <div style="
                font-size:40px;
                font-weight:800;
                line-height:1.1;
                max-width:650px;
            ">
                MEA Hemodialysis<br>
                Catheter Market Intelligence
            </div>

            <div style="
                font-size:18px;
                margin-top:14px;
                opacity:.9;
            ">
                {selected_country} ({country["code"]})
            </div>

            <div style="
                font-size:13px;
                margin-top:7px;
                opacity:.7;
            ">
                2026 Medical Device Commercial Intelligence
            </div>

        </div>
    </div>
    """

    # IMPORTANT:
    # Use st.html so HTML is rendered rather than displayed as text.
    st.html(hero_html)

else:

    st.warning(
        f"Landscape image not found: {country['landscape']}"
    )

    st.title(
        f"MEA Hemodialysis Catheter Market Intelligence — {selected_country}"
    )

# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.markdown(
        '<div class="section-title">Executive Dashboard</div>',
        unsafe_allow_html=True
    )

    executive = load_csv("01_Executive_Summary.csv")

    country_master = load_csv("02_Country_Master.csv")

    country_data = load_csv(country["country_csv"])

    # --------------------------------------------------------
    # Find country row
    # --------------------------------------------------------

    selected_row = pd.DataFrame()

    if not executive.empty:

        country_col = find_column(
            executive,
            ["Country"]
        )

        if country_col:
            selected_row = executive[
                executive[country_col].astype(str).str.strip()
                == selected_country
            ]

            if selected_row.empty:

                selected_row = executive[
                    executive[country_col]
                    .astype(str)
                    .str.contains(
                        selected_country,
                        case=False,
                        na=False
                    )
                ]

    # --------------------------------------------------------
    # Extract KPI values
    # --------------------------------------------------------

    def get_value(column_names):

        if selected_row.empty:
            return None

        col = find_column(
            selected_row,
            column_names
        )

        if col is None:
            return None

        return selected_row.iloc[0][col]

    hd_patients = get_value([
        "2026 HD Patients",
        "2026_HD_Patients",
        "HD Patients"
    ])

    dialysis = get_value([
        "2026 Total Dialysis",
        "2026_Total_Dialysis",
        "Total Dialysis"
    ])

    catheter = get_value([
        "Base Catheter Demand",
        "2026 Base Catheter Demand",
        "Base_Catheter_Demand"
    ])

    investment = get_value([
        "Investment Score",
        "Investment_Score"
    ])

    # --------------------------------------------------------
    # KPI Cards
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    def display_kpi(container, label, value, note=""):

        if value is None or pd.isna(value):
            value_text = "—"
        else:
            try:
                num = float(
                    str(value)
                    .replace(",", "")
                    .replace("%", "")
                )

                if num.is_integer():
                    value_text = f"{int(num):,}"
                else:
                    value_text = f"{num:,.1f}"

            except Exception:
                value_text = str(value)

        with container:

            st.markdown(
                f"""
                <div class="kpi">

                    <div class="kpi-label">
                        {label}
                    </div>

                    <div class="kpi-value">
                        {value_text}
                    </div>

                    <div class="kpi-note">
                        {note}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    display_kpi(
        col1,
        "2026 HD Patients",
        hd_patients,
        "Verified / modeled"
    )

    display_kpi(
        col2,
        "Total Dialysis",
        dialysis,
        "Dialysis population"
    )

    display_kpi(
        col3,
        "Base Catheter Demand",
        catheter,
        "Base scenario"
    )

    display_kpi(
        col4,
        "Investment Score",
        investment,
        "Country attractiveness"
    )

    # --------------------------------------------------------
    # Country overview table
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Country Intelligence</div>',
        unsafe_allow_html=True
    )

    if not selected_row.empty:

        st.dataframe(
            selected_row,
            use_container_width=True,
            hide_index=True
        )

    elif not country_data.empty:

        st.dataframe(
            country_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            f"No data found for {selected_country}."
        )

# ============================================================
# COUNTRY INTELLIGENCE
# ============================================================

elif page == "Country Intelligence":

    st.header(f"🌍 {selected_country}")

    df = load_csv(country["country_csv"])

    if df.empty:
        st.warning(
            f"{country['country_csv']} was not found or is empty."
        )
    else:

        st.success(
            f"{len(df):,} records loaded for {selected_country}"
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

# ============================================================
# HD FACILITY INTELLIGENCE
# ============================================================

elif page == "HD Facility Intelligence":

    st.header("🏥 HD Facility Intelligence")

    df = load_csv("06_Major_Hospitals.csv")

    if df.empty:

        st.warning(
            "06_Major_Hospitals.csv was not found."
        )

    else:

        country_col = find_column(
            df,
            ["Country"]
        )

        if country_col:

            filtered = df[
                df[country_col]
                .astype(str)
                .str.contains(
                    selected_country,
                    case=False,
                    na=False
                )
            ]

        else:

            filtered = df

        st.metric(
            "Facilities in database",
            len(filtered)
        )

        st.dataframe(
            filtered,
            use_container_width=True,
            height=650
        )

# ============================================================
# MARKET SIZING
# ============================================================

elif page == "Market Sizing":

    st.header("💰 Market Sizing")

    df = load_csv("03_Market_Sizing.csv")

    if df.empty:

        st.warning(
            "03_Market_Sizing.csv was not found."
        )

    else:

        country_col = find_column(
            df,
            ["Country"]
        )

        if country_col:

            df = df[
                df[country_col]
                .astype(str)
                .str.contains(
                    selected_country,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

# ============================================================
# DEMAND MODEL
# ============================================================

elif page == "Demand Model":

    st.header("📊 Catheter Demand Model")

    df = load_csv("04_Demand_Model.csv")

    if df.empty:

        st.warning(
            "04_Demand_Model.csv was not found."
        )

    else:

        country_col = find_column(
            df,
            ["Country"]
        )

        if country_col:

            df = df[
                df[country_col]
                .astype(str)
                .str.contains(
                    selected_country,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

# ============================================================
# KOL INTELLIGENCE
# ============================================================

elif page == "KOL Intelligence":

    st.header("👨‍⚕️ KOL Intelligence")

    df = load_csv("05_KOL_Master.csv")

    if df.empty:

        st.warning(
            "05_KOL_Master.csv was not found."
        )

    else:

        country_col = find_column(
            df,
            ["Country"]
        )

        if country_col:

            df = df[
                df[country_col]
                .astype(str)
                .str.contains(
                    selected_country,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

# ============================================================
# HOSPITAL INTELLIGENCE
# ============================================================

elif page == "Hospital Intelligence":

    st.header("🏥 Hospital Intelligence")

    df = load_csv("06_Major_Hospitals.csv")

    if df.empty:

        st.warning(
            "06_Major_Hospitals.csv was not found."
        )

    else:

        country_col = find_column(
            df,
            ["Country"]
        )

        if country_col:

            df = df[
                df[country_col]
                .astype(str)
                .str.contains(
                    selected_country,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

# ============================================================
# HOT AREAS
# ============================================================

elif page == "Hot Areas":

    st.header("🔥 HD Market Hot Areas")

    df = load_csv("07_Hot_Areas.csv")

    if df.empty:

        st.warning(
            "07_Hot_Areas.csv was not found."
        )

    else:

        country_col = find_column(
            df,
            ["Country"]
        )

        if country_col:

            df = df[
                df[country_col]
                .astype(str)
                .str.contains(
                    selected_country,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

# ============================================================
# DISTRIBUTORS
# ============================================================

elif page == "Distributor Intelligence":

    st.header("🚚 Distributor Intelligence")

    df = load_csv("08_Top_Distributors.csv")

    if df.empty:

        st.warning(
            "08_Top_Distributors.csv was not found."
        )

    else:

        country_col = find_column(
            df,
            ["Country"]
        )

        if country_col:

            df = df[
                df[country_col]
                .astype(str)
                .str.contains(
                    selected_country,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

# ============================================================
# COMPETITORS
# ============================================================

elif page == "Competitor Intelligence":

    st.header("🏭 Competitor Intelligence")

    df = load_csv("09_Competitor_Master.csv")

    if df.empty:

        st.warning(
            "09_Competitor_Master.csv was not found."
        )

    else:

        country_col = find_column(
            df,
            ["Country"]
        )

        if country_col:

            df = df[
                df[country_col]
                .astype(str)
                .str.contains(
                    selected_country,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

# ============================================================
# TENDERS
# ============================================================

elif page == "Tender Intelligence":

    st.header("📑 Tender Intelligence")

    df = load_csv("12_Tender_Master.csv")

    if df.empty:

        st.warning(
            "12_Tender_Master.csv was not found."
        )

    else:

        country_col = find_column(
            df,
            ["Country"]
        )

        if country_col:

            df = df[
                df[country_col]
                .astype(str)
                .str.contains(
                    selected_country,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

# ============================================================
# DATA QUALITY
# ============================================================

elif page == "Data Quality":

    st.header("🔎 Data Quality & Verification")

    qa = load_csv("15_QA_Summary.csv")
    gaps = load_csv("13_Data_Gaps.csv")

    if not qa.empty:

        st.subheader("QA Summary")

        st.dataframe(
            qa,
            use_container_width=True
        )

    if not gaps.empty:

        st.subheader("Data Gaps")

        st.dataframe(
            gaps,
            use_container_width=True,
            height=500
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        margin-top:50px;
        padding:20px 0;
        border-top:1px solid #e5e7eb;
        color:#98a2b3;
        font-size:12px;
        text-align:center;
    ">
        MEA Hemodialysis Catheter Market Intelligence
        • 2026
        • Research Integrity First
    </div>
    """,
    unsafe_allow_html=True
)
