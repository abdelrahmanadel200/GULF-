import pandas as pd
import streamlit as st
from typing import Dict

# اسم الملف الموجود في نفس مجلد المشروع (على GitHub/Server)
# أو يمكنك وضع رابط مباشر لملف أونلاين بدلاً من اسم الملف
DATA_SOURCE = "AMECATH_Master_Data.xlsx" 

@st.cache_data(ttl=3600)  # تخزين البيانات مؤقتاً لمدة ساعة لسرعة استجابة الموقع
def load_master_data(source_path: str = DATA_SOURCE) -> Dict[str, pd.DataFrame]:
    """
    دالة تقوم بقراءة ملف الإكسيل المرفق بالمشروع تلقائياً 
    وترجع جميع الشيتات داخل Dictionary لتسهيل الوصول إليها.
    """
    try:
        # قراءة ملف الإكسيل
        xls = pd.ExcelFile(source_path)
        data_sheets = {}

        # قراءة كل شيت وتنظيف الصفوف الفارغة
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            data_sheets[sheet_name.strip()] = df.dropna(how="all").reset_index(drop=True)

        return data_sheets

    except Exception as e:
        st.error(f"⚠️ تعذر تحميل ملف البيانات تلقائياً: {e}")
        return {}
        import streamlit as st
from typing import Dict, Optional

def render_executive_overview(data_sheets: Optional[Dict] = None) -> None:
    """
    دالة تعرض الصفحة الرئيسية (Executive Overview) بنفس التصميم المعروض
    وتقوم بتحويل الكروت الـ 10 إلى أزرار تفاعلية (Active Buttons).
    """
    
    # ── 1. تنسيقات CSS لتحسين شكل البانر والكروت التفاعلية ──────────────────
    st.markdown("""
        <style>
        /* تنسيق البانر العلوي */
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

        /* عنوان القسم */
        .section-header {
            color: #FFFFFF;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* تحويل أزرار Streamlit لتبدو ككروت تفاعلية مطابقة للصورة */
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

        /* تأثير التمرير للزر التفاعلي (Hover) */
        div[data-testid="stColumn"] div.stButton > button:hover {
            border-color: #00B4D8 !important;
            transform: translateY(-5px) !important;
            box-shadow: 0 8px 22px rgba(0, 180, 216, 0.35) !important;
            background: linear-gradient(145deg, #0F2A4A 0%, #0A192F 100%) !important;
        }

        /* تأثير الضغط على الزر (Active/Clicked) */
        div[data-testid="stColumn"] div.stButton > button:active {
            transform: scale(0.97) !important;
            border-color: #00D4FF !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── 2. البانر العلوي (Top Hero Banner) ──────────────────────────────────
    st.markdown("""
        <div class="top-banner">
            <h1 class="banner-title">🌐 REGIONAL EXECUTIVE OVERVIEW</h1>
            <p class="banner-subtitle">📍 Scope: Middle East & GCC Markets Performance</p>
        </div>
    """, unsafe_allow_html=True)

    # ── 3. عنوان المنطقة ───────────────────────────────────────────────────
    st.markdown('<div class="section-header">🌐 Gulf Region — Executive Overview</div>', unsafe_allow_html=True)

    # ── 4. بيانات الكروت التفاعلية الـ 10 ──────────────────────────────────
    cards = [
        {"id": "countries", "icon": "🌍", "label": "COUNTRIES COVERED", "value": "9", "sub": "Gulf Region"},
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

    # Initialize Active State Variable
    if "active_kpi" not in st.session_state:
        st.session_state["active_kpi"] = None

    # ── 5. رسم الصف الأول من الكروت (5 كروت) ──────────────────────────────
    cols_row1 = st.columns(5)
    for i in range(5):
        c = cards[i]
        button_text = f"{c['icon']}\n\n{c['label']}\n\n{c['value']}\n\n{c['sub']}"
        with cols_row1[i]:
            if st.button(button_text, key=f"btn_{c['id']}"):
                st.session_state["active_kpi"] = c["id"]

    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    # ── 6. رسم الصف الثاني من الكروت (5 كروت) ─────────────────────────────
    cols_row2 = st.columns(5)
    for i in range(5, 10):
        c = cards[i]
        button_text = f"{c['icon']}\n\n{c['label']}\n\n{c['value']}\n\n{c['sub']}"
        with cols_row2[i-5]:
            if st.button(button_text, key=f"btn_{c['id']}"):
                st.session_state["active_kpi"] = c["id"]

    # ── 7. إجراء عند الضغط على أي زر تفاعلي ───────────────────────────────
    if st.session_state["active_kpi"]:
        selected_card = next(c for c in cards if c["id"] == st.session_state["active_kpi"])
        st.info(f"🎯 تم الضغط على كارت: **{selected_card['label']}** ({selected_card['value']})")
        
