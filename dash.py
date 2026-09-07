"""AMECATH Executive Decision Engine — modular Streamlit foundation."""

from pathlib import Path

import streamlit as st

from pathlib import Path
import streamlit as st

# Fix imports
from config import APP_TITLE  
from loader import get_default_data
import executive_overview
import pricing


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme_css()

st.markdown('<div class="amecath-brand">AMECATH</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="amecath-page-title">Executive Decision Engine</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="amecath-subtitle">Market intelligence → decision → action → revenue</div>',
    unsafe_allow_html=True,
)

data = get_default_data()

with st.sidebar:
    st.markdown("### Decision Engine")
    page = st.radio(
        "Navigate",
        ["Executive Overview", "Normalized Pricing"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Foundation build")
    st.caption("Data source: centralized seed DataFrames")
    st.caption("Next modules: country scoring, competitor attack, revenue forecast")

if page == "Executive Overview":
    executive_overview.render(data)
else:
    pricing.render(data)
