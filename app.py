import pathlib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AMECATH GCC & Levant Dashboard", layout="wide")

BASE_DIR = pathlib.Path(__file__).parent
EXCEL_PATH = BASE_DIR / "Amecath Dash.xlsx"


@st.cache_data
def load_data():
    kpis = pd.read_excel(EXCEL_PATH, sheet_name="Overview_KPIs")
    hot_areas = pd.read_excel(EXCEL_PATH, sheet_name="Hot_Areas")
    competitors = pd.read_excel(EXCEL_PATH, sheet_name="Competitor_Matrix")
    tenders = pd.read_excel(EXCEL_PATH, sheet_name="Financials_Tenders")
    asp = pd.read_excel(EXCEL_PATH, sheet_name="our ASP")
    return kpis, hot_areas, competitors, tenders, asp


# ⚠️ السطر الأساسي: استدعاء البيانات في النطاق العام قبل أي تبويب
kpis_df, hot_areas_df, competitors_df, tenders_df, asp_df = load_data()

# القائمة الجانبية
st.sidebar.title("AMECATH Analytics")
page = st.sidebar.radio(
    "الانتقال إلى:",
    [
        "1. Overview (9 Countries)",
        "2. Country Deep-Dive",
        "3. Revenue Forecast",
        "4. Sources & Methodology",
    ],
)

# 1. Overview Page
if page == "1. Overview (9 Countries)":
    st.title("🌐 Market Overview - GCC & Levant")

    cols = st.columns(3)
    # الآن kpis_df معرف وجاهز للاستخدام بدون خطأ
    for index, row in kpis_df.iterrows():
        col_idx = index % 3
        with cols[col_idx]:
            with st.container(border=True):
                st.subheader(f"{row['Country']}")
                st.metric("HD Patients (2026)", f"{row['Est. 2026 HD']:,}")
                st.metric(
                    "Annual Catheter Demand",
                    f"{row['Annual Catheter Demand']:,}",
                )
                st.write(f"**Market Value:** {row['Market Value']}")
                st.write(
                    f"**Distributors:** {row['Distributors']} | **KOLs:** {row['KOLs']}"
                )

# القائمة الجانبية للتبويب
st.sidebar.title("AMECATH Analytics")
page = st.sidebar.radio("الانتقال إلى:", [
    "1. Overview (9 Countries)", 
    "2. Country Deep-Dive", 
    "3. Revenue Forecast", 
    "4. Sources & Methodology"
])

# ---------------------------------------------------------
# الصفحة الأولى: Flashcards لـ 9 دول
# ---------------------------------------------------------
if page == "1. Overview (9 Countries)":
    st.title("🌐 Market Overview - GCC & Levant")
    st.write("ملخص عام لأداء وإحصائيات الـ 9 دول المستهدفة")
    
    cols = st.columns(3)
    for index, row in kpis_df.iterrows():
        col_idx = index % 3
        with cols[col_idx]:
            with st.container(border=True):
                st.subheader(f"{row['Country']}")
                st.metric("HD Patients (2026)", f"{row['Est. 2026 HD']:,}")
                st.metric("Annual Catheter Demand", f"{row['Annual Catheter Demand']:,}")
                st.write(f"**Market Value:** {row['Market Value']}")
                st.write(f"**Distributors:** {row['Distributors']} | **KOLs:** {row['KOLs']}")

# ---------------------------------------------------------
# الصفحة الثانية: التفاصيل والدراسة لكل دولة
# ---------------------------------------------------------
elif page == "2. Country Deep-Dive":
    st.title("🔍 Country Interactive Analysis")
    
    # فلتر اختيار الدولة
    selected_country = st.selectbox("اختر الدولة:", kpis_df['Country'].unique())
    
    # عرض معلومات سريعة أعلى الصفحة
    country_info = kpis_df[kpis_df['Country'] == selected_country].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("السكان", f"{country_info['Population 2026']:,}")
    c2.metric("مرضى HD", f"{country_info['Est. 2026 HD']:,}")
    c3.metric("معدل النمو السنوي", f"{country_info['Annual Growth']*100:.1f}%")
    c4.metric("أجهزة الغسيل", f"{country_info['HD Machines']}")

    st.markdown("---")
    
    # التبويبات الداخلية للدولة
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Hot Areas (Heatmap)", "⚔️ Competitors", "📜 Tenders & Procurement", "💰 Our ASP Pricing"])
    
    with tab1:
        st.subheader(f"المناطق الأكثر تركيزاً - {selected_country}")
        # عرض الـ Heatmap أو التوزيع الجغرافي للمراكز
        if selected_country in hot_areas_df.columns:
            country_hot = hot_areas_df[['Rank', selected_country]].dropna()
            st.dataframe(country_hot, use_container_width=True)
            
            # chart تفاعلي يبين الأهمية النسبية للمراكز
            fig = px.bar(country_hot, x='Rank', y='Rank', title=f"Top Priority Hubs in {selected_country}", text=selected_country)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("المنافسون المميزون (Flashcards)")
        # عرض المنافسين على شكل كروت تفاعلية
        for idx, comp in competitors_df.iterrows():
            if pd.notna(comp.iloc[0]) and comp.iloc[0] != 'Competitor':
                with st.expander(f"📌 {comp.iloc[0]} (Market Share: {comp.iloc[1]})"):
                    st.write(f"**التغطية:** {comp.iloc[2]}")
                    st.write(f"**الميزة الرئيسية:** {comp.iloc[4]}")
                    st.write(f"**نقاط الضعف:** {comp.iloc[3]}")
                    st.info(f"💡 **ميزة AMECATH التنافسية:** {comp.iloc[6]}")

    with tab3:
        st.subheader("المناقصات والجهات الحكومية")
        country_tenders = tenders_df[tenders_df['Country'].str.contains(selected_country, na=False)]
        st.dataframe(country_tenders[['Tender Title (Short)', 'Issuing Entity', 'Closing Date', 'Link']], use_container_width=True)

    with tab4:
        st.subheader("أسعار AMECATH المستهدفة (ASP)")
        country_asp = asp_df[asp_df['Country'].str.contains(selected_country, na=False)]
        st.table(country_asp)

# ---------------------------------------------------------
# الصفحة الثالثة: التوقعات المالية (Forecast)
# ---------------------------------------------------------
elif page == "3. Revenue Forecast":
    st.title("📈 Revenue & Volume Forecasts (2026 - 2028)")
    scenario = st.radio("اختر السيناريو:", ["Base Case", "Conservative", "Upside"], horizontal=True)
    st.info(f"تم اختيار سيناريو: {scenario}")
    
    # يمكن ربطها مباشرة بشيت Forecast_Data لإظهار Charts الإيرادات والوحدات
    st.write("عرض تفاعلي لإجمالي الإيرادات المتوقعة والوحدات المطلوبة لكل دولة.")

# ---------------------------------------------------------
# الصفحة الرابعة: المصادر وطرق الحساب
# ---------------------------------------------------------
elif page == "4. Sources & Methodology":
    st.title("📚 Data Sources & References")
    st.write("جميع المصادر المعتمدة في البيانات المرفقة:")
    # عرض شيت Sources
    sources_df = pd.read_excel('Amecath Dash.xlsx', sheet_name='Sources')
    st.dataframe(sources_df, use_container_width=True)
