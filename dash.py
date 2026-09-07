import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIGURATION & DARK THEME TOKENS
# ==========================================
st.set_page_config(
    page_title="Executive Decision Engine & Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design Tokens CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #0b1628;
            color: #f1f5f9;
        }
        [data-testid="stSidebar"] {
            background-color: #070e1a;
            border-right: 1px solid #1e293b;
        }
        div[data-testid="metric-container"] {
            background-color: #13274c;
            border: 1px solid #1e3a8a;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        label[data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-weight: 600;
        }
        div[data-testid="stMetricValue"] {
            color: #f59e0b !important;
            font-size: 1.8rem !important;
            font-weight: 700;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #070e1a;
            padding: 6px;
            border-radius: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            background-color: #13274c;
            border-radius: 6px;
            color: #cbd5e1;
        }
        .stTabs [aria-selected="true"] {
            background-color: #f59e0b !important;
            color: #0b1628 !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LOADERS & CACHING
# ==========================================
@st.cache_data
def load_market_intelligence():
    macro_data = pd.DataFrame({
        "Country": ["Saudi Arabia", "UAE", "Qatar", "Kuwait", "Oman", "Jordan", "Lebanon", "Iraq", "Bahrain"],
        "Code": ["SAU", "ARE", "QAT", "KWT", "OMN", "JOR", "LBN", "IRQ", "BHR"],
        "HD_Patients": [18500, 4200, 1100, 2400, 1800, 3100, 1500, 8900, 750],
        "PD_Patients": [1200, 310, 95, 180, 210, 120, 80, 340, 60],
        "Public_Coverage_Pct": [92, 88, 95, 90, 85, 75, 55, 65, 90],
        "Market_Value_USD_M": [45.2, 18.6, 6.8, 9.4, 7.1, 5.8, 3.2, 14.5, 2.9]
    })
    
    tenders_data = pd.DataFrame({
        "Tender_ID": [f"TND-2026-00{i}" for i in range(1, 10)],
        "Authority": ["NUPCO", "DAHC", "HMC", "MOH Kuwait", "MOH Oman", "RMS Jordan", "MOH Lebanon", "Kimadia", "MOH Bahrain"],
        "Country": ["Saudi Arabia", "UAE", "Qatar", "Kuwait", "Oman", "Jordan", "Lebanon", "Iraq", "Bahrain"],
        "Value_USD_M": [12.5, 4.8, 2.1, 3.5, 2.0, 1.8, 0.9, 6.2, 1.1],
        "Status": ["Open", "Under Evaluation", "Awarded", "Open", "Drafting", "Open", "On Hold", "Under Evaluation", "Awarded"],
        "Priority": ["High", "High", "Medium", "High", "Low", "Medium", "Low", "Critical", "Low"]
    })

    competitor_data = pd.DataFrame({
        "Competitor": ["Fresenius", "B. Braun", "Medtronic", "BD", "Baxter", "Teleflex"],
        "Market_Share_Pct": [34, 22, 15, 12, 10, 7],
        "Avg_Catheter_ASP": [85, 78, 92, 70, 88, 95],
        "Primary_Edge": ["Dialyser Bundles", "Pricing", "Brand/ICU Tech", "Distribution", "PD Focus", "Vascular Access"]
    })
    return macro_data, tenders_data, competitor_data

macro_df, tenders_df, competitor_df = load_market_intelligence()

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/analytics.png", width=64)
st.sidebar.title("Decision Engine")
st.sidebar.markdown("---")

selected_countries = st.sidebar.multiselect(
    "Select Target Markets",
    options=macro_df["Country"].unique(),
    default=macro_df["Country"].unique()
)

st.sidebar.markdown("### Strategic ASP Margin Rules")
min_margin, max_margin = st.sidebar.slider(
    "Target Margin Threshold (%)",
    min_value=10,
    max_value=80,
    value=(20, 60),
    step=5
)

st.sidebar.caption(f"Configured Operating Range: **{min_margin}%** to **{max_margin}%**")

# Filtering Data
filtered_macro = macro_df[macro_df["Country"].isin(selected_countries)]
filtered_tenders = tenders_df[tenders_df["Country"].isin(selected_countries)]

# ==========================================
# 4. EXECUTIVE DASHBOARD HEADER & KPIS
# ==========================================
st.title("AMECATH Executive Decision Engine")
st.markdown("Regional Dialysis Market Intelligence & Pricing Strategy Dashboard")

col1, col2, col3, col4 = st.columns(4)

total_market_val = filtered_macro["Market_Value_USD_M"].sum()
total_hd_patients = filtered_macro["HD_Patients"].sum()
active_tenders_val = filtered_tenders[filtered_tenders["Status"].isin(["Open", "Under Evaluation"])]["Value_USD_M"].sum()
avg_coverage = filtered_macro["Public_Coverage_Pct"].mean()

col1.metric("Total Market Addressable", f"${total_market_val:.1f} M")
col2.metric("Total HD Patient Base", f"{total_hd_patients:,}")
col3.metric("Active Tender Pipeline", f"${active_tenders_val:.1f} M")
col4.metric("Avg Public Coverage", f"{avg_coverage:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5. TABULAR MODULE ROUTING
# ==========================================
tab_macro, tab_tenders, tab_competitors, tab_pricing = st.tabs([
    "📍 Regional Macro Overview", 
    "📑 Tender Pipeline", 
    "⚔️ Competitor Intelligence", 
    "💲 ASP & Margin Simulator"
])

# ---------------- TAB 1: MACRO OVERVIEW ----------------
with tab_macro:
    col_map, col_chart = st.columns([1.2, 1])
    
    with col_map:
        st.subheader("Regional Patient Concentration")
        fig_map = px.choropleth(
            filtered_macro,
            locations="Code",
            color="HD_Patients",
            hover_name="Country",
            hover_data=["PD_Patients", "Market_Value_USD_M"],
            color_continuous_scale="YlOrBr",
            template="plotly_dark"
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=10)
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
    with col_chart:
        st.subheader("Market Value vs Patient Volume")
        fig_bar = px.bar(
            filtered_macro,
            x="Country",
            y="Market_Value_USD_M",
            color="Public_Coverage_Pct",
            color_continuous_scale="Teal",
            text_auto=".1f",
            template="plotly_dark"
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Market Value ($ Millions)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ---------------- TAB 2: TENDER PIPELINE ----------------
with tab_tenders:
    st.subheader("Regional Tender Procurement Opportunities")
    
    status_filter = st.multiselect(
        "Filter Status",
        options=tenders_df["Status"].unique(),
        default=tenders_df["Status"].unique()
    )
    
    tender_display = filtered_tenders[filtered_tenders["Status"].isin(status_filter)]
    
    st.dataframe(
        tender_display,
        column_config={
            "Value_USD_M": st.column_config.NumberColumn("Value ($M)", format="$%.2f M"),
            "Priority": st.column_config.SelectboxColumn("Priority Level", options=["Low", "Medium", "High", "Critical"])
        },
        use_container_width=True,
        hide_index=True
    )

# ---------------- TAB 3: COMPETITOR INTELLIGENCE ----------------
with tab_competitors:
    col_comp_share, col_comp_asp = st.columns(2)
    
    with col_comp_share:
        st.subheader("Market Share Distribution")
        fig_pie = px.pie(
            competitor_df,
            names="Competitor",
            values="Market_Share_Pct",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Dark24,
            template="plotly_dark"
        )
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_comp_asp:
        st.subheader("Competitor ASP Benchmark ($)")
        fig_asp = px.bar(
            competitor_df,
            x="Competitor",
            y="Avg_Catheter_ASP",
            color="Avg_Catheter_ASP",
            color_continuous_scale="Gold",
            template="plotly_dark"
        )
        fig_asp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_asp, use_container_width=True)

# ---------------- TAB 4: PRICING & MARGIN CALCULATOR ----------------
with tab_pricing:
    st.subheader("Dynamic Average Selling Price (ASP) Model")
    
    col_calc1, col_calc2 = st.columns(2)
    
    with col_calc1:
        unit_cogs = st.number_input("Unit COGS ($)", min_value=1.0, max_value=200.0, value=35.0, step=2.5)
        distributor_margin = st.slider("Distributor Margin (%)", 5, 40, 15)
        
    with col_calc2:
        target_margin = st.slider("Target Internal Margin (%)", min_value=min_margin, max_value=max_margin, value=int((min_margin + max_margin) / 2))
        
        # Financial Calculations
        floor_price = unit_cogs / (1 - (min_margin / 100))
        target_asp = unit_cogs / (1 - (target_margin / 100))
        tender_list_price = target_asp / (1 - (distributor_margin / 100))
        
        st.markdown(f"""
        <div style="background-color: #13274c; padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b;">
            <p style="margin:0; color:#94a3b8;">Floor ASP (Min {min_margin}% Margin): <b>${floor_price:.2f}</b></p>
            <h3 style="margin:5px 0; color:#f59e0b;">Target ASP: ${target_asp:.2f}</h3>
            <p style="margin:0; color:#cbd5e1;">Suggested Tender List Price: <b>${tender_list_price:.2f}</b></p>
        </div>
        """, unsafe_allow_html=True)
