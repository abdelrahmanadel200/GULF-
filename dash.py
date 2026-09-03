import os
import pandas as pd
import streamlit as st
from typing import Dict, Optional

# ==============================================================================
# 1. CONFIGURATION & CONSTANTS
# ==============================================================================

DATA_SOURCE = "AMECATH_Master_Data.xlsx"

# ثيمات دول الخليج (GCC)
COUNTRY_THEMES = {
    "Saudi Arabia": {
        "flag": "🇸🇦",
        "primary": "#006C35",
        "accent": "#D4AF37",
        "bg": "#0B1D12",
        "card_bg": "rgba(15, 40, 25, 0.88)",
        "text": "#FFFFFF",
        "landmark": "Kingdom of Saudi Arabia",
    },
    "UAE": {
        "flag": "🇦🇪",
        "primary": "#007A3D",
        "accent": "#FFD700",
        "bg": "#0D1F17",
        "card_bg": "rgba(13, 31, 23, 0.88)",
        "text": "#FFFFFF",
        "landmark": "United Arab Emirates",
    },
    "Kuwait": {
        "flag": "🇰🇼",
        "primary": "#007A3D",
        "accent": "#CE1126",
        "bg": "#0A1A14",
        "card_bg": "rgba(10, 26, 20, 0.88)",
        "text": "#FFFFFF",
        "landmark": "State of Kuwait",
    },
    "Qatar": {
        "flag": "🇶🇦",
        "primary": "#8A1538",
        "accent": "#FFFFFF",
        "bg": "#1A080C",
        "card_bg": "rgba(35, 12, 20, 0.88)",
        "text": "#FFFFFF",
        "landmark": "State of Qatar",
    },
    "Oman": {
        "flag": "🇴🇲",
        "primary": "#DB162F",
        "accent": "#008000",
        "bg": "#1C0A0C",
        "card_bg": "rgba(35, 15, 18, 0.88)",
        "text": "#FFFFFF",
        "landmark": "Sultanate of Oman",
    },
    "Bahrain": {
        "flag": "🇧🇭",
        "primary": "#CE1126",
        "accent": "#FFFFFF",
        "bg": "#1C080A",
        "card_bg": "rgba(35, 10, 14, 0.88)",
        "text": "#FFFFFF",
        "landmark": "Kingdom of Bahrain",
    },
}


# ==============================================================================
# 2. DATA LOADING & CACHING
# ==============================================================================

@st.cache_data(ttl=3600)
def load_master_data(source_path: str = DATA_SOURCE) -> Dict[str, pd.DataFrame]:
    """
    قراءة ملف الإكسيل المرفق تلقائياً وترتيب جميع الشيتات داخل Dictionary.
    """
    try:
        xls = pd.ExcelFile(source_path)
        data_sheets = {}
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            data_sheets[sheet_name.strip()] = df.dropna(how="all").reset_index(drop=True)
        return data_sheets
    except Exception as e:
        st.error(f"⚠️ تعذر تحميل ملف البيانات تلقائياً: {e}")
        return {}


# ==============================================================================
# 3. EXECUTIVE OVERVIEW PAGE RENDERER
# ==============================================================================

def render_executive_overview(data_sheets: Optional[Dict] = None) -> None:
    """
    عرض الصفحة الرئيسية (Executive Overview) وتحويل الكروت الـ 10 إلى أزرار تفاعلية.
    """
    # ── CSS Styling ────────────────────────────────────────────────────────────
    st.markdown("""
        <style>
        .top-banner {
            background: linear-gradient(180deg, #02457A 0%, #001B3A 100%);
            border: 1px solid #00A8E8;
            border-radius: 14px;
            padding: 22px 15px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            margin-bottom: 30px;
        }
        .banner-title {
            color: #FFFFFF;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 1.5px;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }
        .banner-subtitle {
            color: #79C7FF;
            font-size: 13px;
            font-weight: 600;
            margin-top: 8px;
            margin-bottom: 0;
        }
        .section-header {
            color: #FFFFFF;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        div[data-testid="stColumn"] div.stButton > button {
            width: 100% !important;
            min-height: 140px !important;
            background: linear-gradient(145deg, #0A192F 0%, #06101E 100%) !important;
            border: 1px solid #1E3A8A !important;
            border-radius: 12px !important;
            color: #FFFFFF !important;
            padding: 12px 8px !important;
            transition: all 0.3s ease-in-out !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            white-space: pre-wrap !important;
            line-height: 1.4 !important;
        }
        div[data-testid="stColumn"] div.stButton > button:hover {
            border-color: #00B4D8 !important;
            transform: translateY(-5px) !important;
            box-shadow: 0 8px 22px rgba(0, 180, 216, 0.35) !important;
            background: linear-gradient(145deg, #0F2A4A 0%, #0A192F 100%) !important;
        }
        div[data-testid="stColumn"] div.stButton > button:active {
            transform: scale(0.97) !important;
            border-color: #00D4FF !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── Top Hero Banner ────────────────────────────────────────────────────────
    st.markdown("""
        <div class="top-banner">
            <h1 class="banner-title">🌐 REGIONAL EXECUTIVE OVERVIEW</h1>
            <p class="banner-subtitle">📍 Scope: Middle East & GCC Markets Performance</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🌐 Gulf Region — Executive Overview</div>', unsafe_allow_html=True)

    # ── Cards Data ─────────────────────────────────────────────────────────────
    cards = [
        {"id": "countries", "icon": "🌍", "label": "COUNTRIES COVERED", "value": "6", "sub": "Gulf Region"},
        {"id": "population", "icon": "👥", "label": "TOTAL POPULATION 2026", "value": "127.68M", "sub": "127,681,500"},
        {"id": "hd_patients", "icon": "🩺", "label": "TOTAL HD PATIENTS", "value": "65,254", "sub": "Hemodialysis"},
        {"id": "pd_est", "icon": "🧪", "label": "EST. 2026 PD", "value": "4,114", "sub": "Peritoneal Dialysis"},
        {"id": "facilities", "icon": "🏥", "label": "DIALYSIS FACILITIES", "value": "762", "sub": "Centers"},
        {"id": "machines", "icon": "⚡", "label": "HD MACHINES", "value": "44,050", "sub": "Units"},
        {"id": "demand", "icon": "💉", "label": "ANNUAL CATHETER DEMAND", "value": "167.87K", "sub": "167,867 units"},
        {"id": "market_val", "icon": "💰", "label": "MARKET VALUE", "value": "$18.90M", "sub": "USD"},
        {"id": "distributors", "icon": "🏢", "label": "DISTRIBUTORS", "value": "90", "sub": "Active Partners"},
        {"id": "kols", "icon": "👨‍⚕️", "label": "KOLS", "value": "90", "sub": "Opinion Leaders"}
    ]

    if "active_kpi" not in st.session_state:
        st.session_state["active_kpi"] = None

    # ── Grid Rendering ─────────────────────────────────────────────────────────
    # Row 1
    cols_row1 = st.columns(5)
    for i in range(5):
        c = cards[i]
        button_text = f"{c['icon']}\n\n{c['label']}\n\n{c['value']}\n\n{c['sub']}"
        with cols_row1[i]:
            if st.button(button_text, key=f"btn_{c['id']}"):
                st.session_state["active_kpi"] = c["id"]

    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    # Row 2
    cols_row2 = st.columns(5)
    for i in range(5, 10):
        c = cards[i]
        button_text = f"{c['icon']}\n\n{c['label']}\n\n{c['value']}\n\n{c['sub']}"
        with cols_row2[i - 5]:
            if st.button(button_text, key=f"btn_{c['id']}"):
                st.session_state["active_kpi"] = c["id"]

    # ── Selection Feedback ──────────────────────────────────────────────────────
    if st.session_state["active_kpi"]:
        selected_card = next((c for c in cards if c["id"] == st.session_state["active_kpi"]), None)
        if selected_card:
            st.info(f"🎯 تم الضغط على كارت: **{selected_card['label']}** ({selected_card['value']})")


# ==============================================================================
# 4. COUNTRIES PAGE RENDERER
# ==============================================================================

def render_countries_page(data_sheets: Dict[str, pd.DataFrame], country_themes: Dict[str, dict]) -> None:
    """
    عرض صفحة الدول بتصميم ديناميكي يتغير حسب علم وخلفية كل دولة.
    """
    if "selected_country_view" not in st.session_state:
        st.session_state["selected_country_view"] = None

    # ── View 1: Default Selection Grid ─────────────────────────────────────────
    if st.session_state["selected_country_view"] is None:
        default_theme = {
            "primary": "#00D4FF", "accent": "#FFB703",
            "bg": "#051329", "card_bg": "rgba(8, 28, 54, 0.88)", "text": "#FFFFFF"
        }
        inject_css(default_theme, bg_b64="")

        st.subheader("🌍 Select a Country Market / اختر الدولة")
        st.caption("اضغط على علم الدولة لمشاهدة كافة التقارير والمعلومات المخصصة لها.")

        st.markdown("""
            <style>
            div[data-testid="stColumn"] div.stButton > button {
                width: 100% !important;
                height: 150px !important;
                background: linear-gradient(145deg, #0D1F2D 0%, #08121C 100%) !important;
                border: 2px solid #1E3A8A !important;
                border-radius: 16px !important;
                color: #FFFFFF !important;
                font-size: 20px !important;
                font-weight: 700 !important;
                transition: all 0.3s ease-in-out !important;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4) !important;
            }
            div[data-testid="stColumn"] div.stButton > button:hover {
                border-color: #00D4FF !important;
                transform: translateY(-5px) !important;
                box-shadow: 0 10px 25px rgba(0, 212, 255, 0.35) !important;
            }
            </style>
        """, unsafe_allow_html=True)

        countries_list = list(country_themes.keys())
        cols_per_row = 3

        for i in range(0, len(countries_list), cols_per_row):
            cols = st.columns(cols_per_row)
            row_countries = countries_list[i : i + cols_per_row]

            for j, c_name in enumerate(row_countries):
                theme = country_themes[c_name]
                flag = theme.get("flag", "🏳️")
                card_label = f"{flag}\n\n{c_name}"

                with cols[j]:
                    if st.button(card_label, key=f"country_card_{c_name}", use_container_width=True):
                        st.session_state["selected_country_view"] = c_name
                        st.rerun()

    # ── View 2: Detailed Country Dashboard ──────────────────────────────────────
    else:
        c_name = st.session_state["selected_country_view"]
        theme = country_themes.get(c_name, {
            "flag": "🏳️", "primary": "#00B4D8", "accent": "#FFB703",
            "bg": "#0B1D12", "card_bg": "rgba(15, 40, 25, 0.88)", "text": "#FFFFFF"
        })

        landscape_b64 = find_landscape_b64(c_name)
        inject_css(theme, bg_b64=landscape_b64)

        st.markdown(f"""
            <style>
            button[data-baseweb="tab"] {{
                background-color: {theme['card_bg']} !important;
                color: #FFFFFF !important;
                border-radius: 8px 8px 0px 0px !important;
                padding: 10px 18px !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
                font-weight: 600 !important;
            }}
            button[data-baseweb="tab"][aria-selected="true"] {{
                background-color: {theme['primary']} !important;
                color: #FFFFFF !important;
                border-bottom: 3px solid {theme['accent']} !important;
                font-weight: 800 !important;
                box-shadow: 0 -4px 12px rgba(0,0,0,0.3) !important;
            }}
            div.stButton > button[key="btn_back_to_countries"] {{
                background-color: {theme['primary']} !important;
                border: 1px solid {theme['accent']} !important;
                color: #FFFFFF !important;
                font-weight: bold !important;
            }}
            </style>
        """, unsafe_allow_html=True)

        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("⬅️ Back to Countries", key="btn_back_to_countries"):
                st.session_state["selected_country_view"] = None
                st.rerun()

        render_hero(c_name, theme, bg_b64=landscape_b64)

        tabs = st.tabs([
            "📊 Macro Environment",
            "📈 Financials & Tenders",
            "🔥 Hot Market Areas",
            "🤝 Local Distributors",
            "⚔️ Competitor Matrix",
            "🏷️ Competitor ASP",
            "👨‍⚕️ Key Opinion Leaders",
            "🔮 Growth Forecast"
        ])

        with tabs[0]:
            render_generic_table(data_sheets, "macro", "📊 Macro Environment", c_name)
        with tabs[1]:
            render_generic_table(data_sheets, "tenders", "📈 Financials & Tenders", c_name)
        with tabs[2]:
            render_hot_areas(data_sheets, c_name, theme)
        with tabs[3]:
            render_distributors(data_sheets, c_name, theme)
        with tabs[4]:
            render_generic_table(data_sheets, "competitors", "⚔️ Competitor Matrix", c_name)
        with tabs[5]:
            render_generic_table(data_sheets, "competitors_asp", "🏷️ Competitor ASP", c_name)
        with tabs[6]:
            render_generic_table(data_sheets, "kol", "👨‍⚕️ Key Opinion Leaders", c_name)
        with tabs[7]:
            render_forecast(data_sheets, c_name, theme)
