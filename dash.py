import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="AMECATH Market Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* hide streamlit chrome */
  #MainMenu, header, footer, [data-testid="collapsedControl"] { display:none !important; }
  .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
  [data-testid="stAppViewContainer"] { background: #0b1628; }
  /* sidebar fixed */
  .sb-wrap {
    position:fixed; top:0; left:0; bottom:0; width:210px;
    background:#070f1f; border-right:1px solid #1e3d7a;
    display:flex; flex-direction:column; padding:18px 0;
    z-index:9999; font-family:'Segoe UI',system-ui,sans-serif;
    overflow-y:auto;
  }
  .sb-logo      { padding:0 16px 18px; border-bottom:1px solid #1e3d7a; margin-bottom:10px; }
  .sb-logo-text { font-size:15px; font-weight:700; color:#60a5fa; letter-spacing:1.5px; }
  .sb-logo-sub  { font-size:10px; color:#3a5278; margin-top:2px; }
  .sb-section   { font-size:9px; letter-spacing:1.5px; color:#2a4060; text-transform:uppercase;
                  padding:14px 16px 6px; font-weight:700; }
  .sb-item      { display:flex; align-items:center; gap:10px; padding:10px 16px;
                  font-size:12px; color:#6a85b0; border-left:3px solid transparent;
                  cursor:pointer; text-decoration:none !important; }
  .sb-item:hover  { background:#0f1f3d; color:#c8d8f0; }
  .sb-item.active { background:#0f1f3d; color:#60a5fa; border-left-color:#2563eb; font-weight:600; }
  .sb-icon { font-size:15px; width:18px; text-align:center; }
  /* main content wrapper */
  .main-wrap {
    margin-left:210px;
    padding:16px 20px 40px 20px;
    background:#0b1628;
    min-height:100vh;
    font-family:'Segoe UI',system-ui,sans-serif;
    color:#e8edf5;
    box-sizing:border-box;
  }
  /* top banner */
  .top-banner {
    background:linear-gradient(135deg,#0d2145 0%,#1a3a6e 50%,#0d2145 100%);
    border:1px solid #1e3d7a; border-radius:14px;
    padding:20px 32px; margin-bottom:18px; text-align:center; position:relative; overflow:hidden;
  }
  .top-banner::before {
    content:''; position:absolute; inset:0;
    background:radial-gradient(ellipse at 50% -20%,#2563eb22 0%,transparent 65%);
    pointer-events:none;
  }
  .banner-title { font-size:18px; font-weight:700; letter-spacing:2px; color:#e8edf5; }
  .banner-sub   { font-size:11px; color:#f59e0b; margin-top:5px; }
  /* section header */
  .section-hdr { font-size:15px; font-weight:600; color:#c8d8f0; margin:0 0 14px;
                 display:flex; align-items:center; gap:8px; }
  /* kpi grid */
  .kpi-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:14px; }
  .kpi-card { background:#0f1f3d; border:1px solid #1e3d7a; border-radius:12px;
              padding:16px 12px 12px; display:flex; flex-direction:column;
              align-items:center; text-align:center; gap:5px;
              transition:border-color .2s, transform .15s; }
  .kpi-card:hover { border-color:#2563eb; transform:translateY(-1px); }
  .kpi-icon  { font-size:22px; margin-bottom:2px; }
  .kpi-label { font-size:9px; letter-spacing:1px; color:#6a85b0; text-transform:uppercase; font-weight:600; }
  .kpi-value { font-size:22px; font-weight:700; color:#e8edf5; line-height:1.1; }
  .accent { color:#60a5fa !important; }
  .gold   { color:#f59e0b !important; }
  .kpi-sub       { font-size:10px; color:#3b82f6; font-weight:500; }
  .kpi-sub.muted { color:#6a85b0; }
  .kpi-sub.green { color:#34d399; }
  .kpi-sub.amber { color:#f59e0b; }
  .divider { height:1px; background:#1e3d7a; margin:6px 0 12px; }
  /* placeholder */
  .placeholder { background:#0f1f3d; border:1px dashed #1e3d7a; border-radius:14px;
                 padding:80px 32px; text-align:center; margin-top:8px; }
  .ph-icon  { font-size:44px; margin-bottom:14px; }
  .ph-title { font-size:18px; font-weight:600; color:#6a85b0; margin-bottom:8px; }
  .ph-sub   { font-size:13px; color:#3a5278; }
  /* map legend */
  .legend { display:flex; gap:20px; flex-wrap:wrap; margin-top:10px; font-size:12px; color:#c8d8f0; }
  /* plotly chart full-width */
  [data-testid="stPlotlyChart"] { width:100% !important; }
  /* country buttons row */
  .stButton>button {
    font-size:11px !important; padding:5px 8px !important;
    border-radius:20px !important; font-weight:600 !important;
    border:1px solid #1e3d7a !important;
    background:#0f1f3d !important; color:#6a85b0 !important;
  }
  .stButton>button:hover { border-color:#2563eb !important; color:#c8d8f0 !important; }
  /* active country button via primary type */
  .stButton>button[kind="primary"] {
    background:#1e3d7a !important; color:#e8edf5 !important;
    border-color:#3b82f6 !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────
HA_DATA = {
    "Saudi Arabia": {"lat": 24.0, "lng": 45.0, "zoom": 4, "areas": [
        {"name": "Riyadh",        "lat": 24.69, "lng": 46.72, "rank": 1, "centers": 39, "hd": 5700,  "priority": "Critical"},
        {"name": "Jeddah",        "lat": 21.49, "lng": 39.19, "rank": 2, "centers": 12, "hd": 2100,  "priority": "High"},
        {"name": "Makkah",        "lat": 21.39, "lng": 39.86, "rank": 3, "centers": 12, "hd": 1950,  "priority": "High"},
        {"name": "Dammam/Khobar", "lat": 26.43, "lng": 50.10, "rank": 4, "centers": 6,  "hd": 1200,  "priority": "High"},
        {"name": "Madinah",       "lat": 24.47, "lng": 39.61, "rank": 5, "centers": 5,  "hd": 900,   "priority": "Medium"},
        {"name": "Buraydah",      "lat": 26.33, "lng": 43.97, "rank": 6, "centers": 7,  "hd": 1020,  "priority": "Medium"},
        {"name": "Hail",          "lat": 27.51, "lng": 41.69, "rank": 7, "centers": 6,  "hd": 870,   "priority": "Medium"},
        {"name": "Abha",          "lat": 18.22, "lng": 42.51, "rank": 8, "centers": 4,  "hd": 600,   "priority": "Low"},
        {"name": "Tabuk",         "lat": 28.38, "lng": 36.57, "rank": 9, "centers": 3,  "hd": 450,   "priority": "Low"},
    ]},
    "UAE": {"lat": 24.0, "lng": 54.0, "zoom": 6, "areas": [
        {"name": "Dubai",        "lat": 25.20, "lng": 55.27, "rank": 1, "centers": 7, "hd": 840, "priority": "Critical"},
        {"name": "Abu Dhabi",    "lat": 24.45, "lng": 54.37, "rank": 2, "centers": 5, "hd": 600, "priority": "High"},
        {"name": "Sharjah",      "lat": 25.35, "lng": 55.42, "rank": 3, "centers": 3, "hd": 360, "priority": "Medium"},
        {"name": "Al Ain",       "lat": 24.21, "lng": 55.76, "rank": 4, "centers": 2, "hd": 240, "priority": "Medium"},
        {"name": "Ajman",        "lat": 25.41, "lng": 55.44, "rank": 5, "centers": 2, "hd": 200, "priority": "Low"},
        {"name": "Fujairah/RAK", "lat": 25.12, "lng": 56.34, "rank": 6, "centers": 2, "hd": 180, "priority": "Low"},
    ]},
    "Qatar": {"lat": 25.3, "lng": 51.2, "zoom": 8, "areas": [
        {"name": "Doha - FBJ",  "lat": 25.29, "lng": 51.53, "rank": 1, "centers": 4, "hd": 720, "priority": "Critical"},
        {"name": "Al Wakrah",   "lat": 25.17, "lng": 51.60, "rank": 2, "centers": 2, "hd": 240, "priority": "Medium"},
        {"name": "Al Khor",     "lat": 25.68, "lng": 51.50, "rank": 3, "centers": 1, "hd": 120, "priority": "Low"},
        {"name": "Al Shahania", "lat": 25.57, "lng": 51.27, "rank": 4, "centers": 1, "hd": 80,  "priority": "Low"},
        {"name": "Lusail",      "lat": 25.43, "lng": 51.49, "rank": 5, "centers": 1, "hd": 60,  "priority": "Low"},
    ]},
    "Kuwait": {"lat": 29.3, "lng": 47.7, "zoom": 8, "areas": [
        {"name": "Kuwait City",    "lat": 29.37, "lng": 47.98, "rank": 1, "centers": 8, "hd": 970, "priority": "Critical"},
        {"name": "Ahmadi",         "lat": 29.08, "lng": 48.08, "rank": 2, "centers": 3, "hd": 390, "priority": "High"},
        {"name": "Hawalli",        "lat": 29.33, "lng": 48.03, "rank": 3, "centers": 3, "hd": 340, "priority": "Medium"},
        {"name": "Farwaniya",      "lat": 29.27, "lng": 47.96, "rank": 4, "centers": 3, "hd": 280, "priority": "Medium"},
        {"name": "Jahra",          "lat": 29.33, "lng": 47.66, "rank": 5, "centers": 2, "hd": 180, "priority": "Low"},
        {"name": "Sabah Al-Ahmad", "lat": 28.90, "lng": 48.18, "rank": 6, "centers": 1, "hd": 80,  "priority": "Low"},
    ]},
    "Iraq": {"lat": 33.0, "lng": 44.0, "zoom": 5, "areas": [
        {"name": "Baghdad",      "lat": 33.34, "lng": 44.40, "rank": 1, "centers": 11, "hd": 3967, "priority": "Critical"},
        {"name": "Basra",        "lat": 30.51, "lng": 47.78, "rank": 2, "centers": 3,  "hd": 1500, "priority": "Critical"},
        {"name": "Erbil",        "lat": 36.19, "lng": 44.01, "rank": 3, "centers": 4,  "hd": 1200, "priority": "High"},
        {"name": "Sulaymaniyah", "lat": 35.56, "lng": 45.43, "rank": 4, "centers": 3,  "hd": 900,  "priority": "High"},
        {"name": "Kirkuk",       "lat": 35.47, "lng": 44.39, "rank": 5, "centers": 2,  "hd": 463,  "priority": "Medium"},
        {"name": "Mosul",        "lat": 36.34, "lng": 43.13, "rank": 6, "centers": 2,  "hd": 420,  "priority": "Medium"},
        {"name": "Najaf",        "lat": 31.99, "lng": 44.33, "rank": 7, "centers": 2,  "hd": 380,  "priority": "Medium"},
        {"name": "Diwaniyah",    "lat": 31.99, "lng": 44.92, "rank": 8, "centers": 2,  "hd": 300,  "priority": "Low"},
    ]},
    "Jordan": {"lat": 31.0, "lng": 36.5, "zoom": 6, "areas": [
        {"name": "Amman", "lat": 31.95, "lng": 35.93, "rank": 1, "centers": 5, "hd": 3200, "priority": "Critical"},
        {"name": "Irbid", "lat": 32.55, "lng": 35.85, "rank": 2, "centers": 2, "hd": 960,  "priority": "High"},
        {"name": "Zarqa", "lat": 32.07, "lng": 36.09, "rank": 3, "centers": 2, "hd": 768,  "priority": "Medium"},
        {"name": "Salt",  "lat": 32.03, "lng": 35.73, "rank": 4, "centers": 1, "hd": 480,  "priority": "Medium"},
        {"name": "Karak", "lat": 31.18, "lng": 35.70, "rank": 5, "centers": 1, "hd": 320,  "priority": "Low"},
    ]},
    "Lebanon": {"lat": 33.9, "lng": 35.9, "zoom": 7, "areas": [
        {"name": "Greater Beirut", "lat": 33.89, "lng": 35.50, "rank": 1, "centers": 30, "hd": 2365, "priority": "Critical"},
        {"name": "Tripoli",        "lat": 34.44, "lng": 35.85, "rank": 2, "centers": 12, "hd": 850,  "priority": "High"},
        {"name": "Sidon",          "lat": 33.56, "lng": 35.37, "rank": 3, "centers": 8,  "hd": 520,  "priority": "Medium"},
        {"name": "Zahle",          "lat": 33.85, "lng": 35.90, "rank": 4, "centers": 6,  "hd": 400,  "priority": "Medium"},
        {"name": "Jounieh",        "lat": 33.98, "lng": 35.62, "rank": 5, "centers": 4,  "hd": 280,  "priority": "Low"},
        {"name": "Nabatieh",       "lat": 33.38, "lng": 35.48, "rank": 6, "centers": 3,  "hd": 200,  "priority": "Low"},
    ]},
    "Oman": {"lat": 21.0, "lng": 57.0, "zoom": 5, "areas": [
        {"name": "Muscat",     "lat": 23.61, "lng": 58.59, "rank": 1, "centers": 4, "hd": 1000, "priority": "Critical"},
        {"name": "Salalah",    "lat": 17.02, "lng": 54.09, "rank": 2, "centers": 2, "hd": 500,  "priority": "High"},
        {"name": "Sohar",      "lat": 24.34, "lng": 56.75, "rank": 3, "centers": 2, "hd": 380,  "priority": "Medium"},
        {"name": "Ibri",       "lat": 23.22, "lng": 56.51, "rank": 4, "centers": 2, "hd": 250,  "priority": "Medium"},
        {"name": "Barka/Seeb", "lat": 23.68, "lng": 57.89, "rank": 5, "centers": 1, "hd": 180,  "priority": "Low"},
    ]},
    "Bahrain": {"lat": 26.0, "lng": 50.5, "zoom": 9, "areas": [
        {"name": "Manama / Riffa",  "lat": 26.22, "lng": 50.59, "rank": 1, "centers": 5, "hd": 2500, "priority": "Critical"},
        {"name": "A'Ali",           "lat": 26.15, "lng": 50.53, "rank": 2, "centers": 2, "hd": 900,  "priority": "High"},
        {"name": "Muharraq",        "lat": 26.26, "lng": 50.62, "rank": 3, "centers": 2, "hd": 680,  "priority": "Medium"},
        {"name": "Saar",            "lat": 26.21, "lng": 50.48, "rank": 4, "centers": 1, "hd": 320,  "priority": "Low"},
        {"name": "Riffa (private)", "lat": 26.13, "lng": 50.56, "rank": 5, "centers": 1, "hd": 150,  "priority": "Low"},
    ]},
}

PRIORITY_COLOR = {"Critical": "#ef4444", "High": "#f97316", "Medium": "#eab308", "Low": "#22c55e"}
PRIORITY_SIZE  = {"Critical": 22, "High": 18, "Medium": 14, "Low": 11}

PAGES = [
    ("overview",    "🏠", "Overview"),
    ("countries",   "🌍", "Country Analysis"),
    ("forecast",    "📈", "Revenue Forecast"),
    ("pricing",     "💲", "Pricing Intel"),
    ("tenders",     "📋", "Tenders"),
    ("competitors", "🏆", "Competitors"),
    ("hotareas",    "📍", "Hot Areas"),
    ("exhibitions", "📅", "Exhibitions"),
    ("regulatory",  "📜", "Regulatory"),
]

# ── Session state ─────────────────────────────────────────────────────────────
if "page"    not in st.session_state: st.session_state.page    = "overview"
if "country" not in st.session_state: st.session_state.country = "Saudi Arabia"

qp = st.query_params
if "page" in qp:
    st.session_state.page = qp["page"]

# ── Sidebar HTML ──────────────────────────────────────────────────────────────
sections = [
    ("Main",   ["overview","countries","forecast"]),
    ("Market", ["pricing","tenders","competitors"]),
    ("Field",  ["hotareas","exhibitions","regulatory"]),
]
page_map = {p[0]: p for p in PAGES}

sb_items = ""
for sec_label, ids in sections:
    sb_items += f'<div class="sb-section">{sec_label}</div>'
    for pid in ids:
        pg     = page_map[pid]
        active = "active" if st.session_state.page == pid else ""
        sb_items += (
            f'<a class="sb-item {active}" href="?page={pid}" target="_self">'
            f'<span class="sb-icon">{pg[1]}</span><span>{pg[2]}</span></a>'
        )

st.markdown(f"""
<div class="sb-wrap">
  <div class="sb-logo">
    <div class="sb-logo-text">AMECATH</div>
    <div class="sb-logo-sub">Market Intelligence</div>
  </div>
  {sb_items}
</div>
<div class="main-wrap">
""", unsafe_allow_html=True)

page = st.session_state.page

# ── OVERVIEW ──────────────────────────────────────────────────────────────────
if page == "overview":
    st.markdown("""
    <div class="top-banner">
      <div class="banner-title">🌐 REGIONAL EXECUTIVE OVERVIEW</div>
      <div class="banner-sub">📌 Scope: Middle East &amp; GCC Markets Performance</div>
    </div>
    <div class="section-hdr">🌐 Gulf Region — Executive Overview</div>
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon">🌍</div>
        <div class="kpi-label">Countries Covered</div>
        <div class="kpi-value">9</div>
        <div class="kpi-sub">Gulf Region</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">👥</div>
        <div class="kpi-label">Total Population 2026</div>
        <div class="kpi-value accent">127.68M</div>
        <div class="kpi-sub muted">127,681,500</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">🫀</div>
        <div class="kpi-label">Total HD Patients</div>
        <div class="kpi-value">65,254</div>
        <div class="kpi-sub">Hemodialysis</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">💉</div>
        <div class="kpi-label">Est. 2026 PD</div>
        <div class="kpi-value">4,114</div>
        <div class="kpi-sub">Peritoneal Dialysis</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">🏥</div>
        <div class="kpi-label">Dialysis Facilities</div>
        <div class="kpi-value">762</div>
        <div class="kpi-sub muted">Centers</div>
      </div>
    </div>
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-label">HD Machines</div>
        <div class="kpi-value">44,050</div>
        <div class="kpi-sub muted">Units</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">🩹</div>
        <div class="kpi-label">Annual Catheter Demand</div>
        <div class="kpi-value accent">167.87K</div>
        <div class="kpi-sub muted">167,867 units</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Market Value</div>
        <div class="kpi-value gold">$18.90M</div>
        <div class="kpi-sub amber">USD</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">🤝</div>
        <div class="kpi-label">Distributors</div>
        <div class="kpi-value">90</div>
        <div class="kpi-sub green">Active Partners</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">⭐</div>
        <div class="kpi-label">KOLs</div>
        <div class="kpi-value">90</div>
        <div class="kpi-sub green">Opinion Leaders</div>
      </div>
    </div>
    <div class="divider"></div>
    <div style="text-align:center;padding:8px 0 16px;font-size:10px;color:#2a4060;">
      Data source: Amecath_Dash.xlsx · 2026 Edition · 9 Markets
    </div>
    """, unsafe_allow_html=True)

# ── HOT AREAS ─────────────────────────────────────────────────────────────────
elif page == "hotareas":
    st.markdown('<div class="section-hdr">📍 Hot Areas — Dialysis Map</div>', unsafe_allow_html=True)

    # Country selector buttons
    countries = list(HA_DATA.keys())
    cols = st.columns(len(countries))
    for i, c in enumerate(countries):
        with cols[i]:
            btn_type = "primary" if st.session_state.country == c else "secondary"
            if st.button(c, key=f"btn_{c}", type=btn_type, use_container_width=True):
                st.session_state.country = c
                st.rerun()

    country = st.session_state.country
    d = HA_DATA[country]

    # Build Plotly map
    fig = go.Figure()
    for priority in ["Critical", "High", "Medium", "Low"]:
        pts = [a for a in d["areas"] if a["priority"] == priority]
        if not pts:
            continue
        fig.add_trace(go.Scattermapbox(
            lat=[p["lat"] for p in pts],
            lon=[p["lng"] for p in pts],
            mode="markers",
            marker=dict(
                size=[PRIORITY_SIZE[p["priority"]] for p in pts],
                color=PRIORITY_COLOR[priority],
                opacity=0.92,
            ),
            text=[
                f"<b>{p['name']}</b><br>"
                f"Rank: #{p['rank']} in {country}<br>"
                f"Centers: {p['centers']}<br>"
                f"HD Patients: {p['hd']:,}<br>"
                f"Priority: {p['priority']}"
                for p in pts
            ],
            hovertemplate="%{text}<extra></extra>",
            name=priority,
        ))

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=d["lat"], lon=d["lng"]),
            zoom=d["zoom"],
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=530,
        paper_bgcolor="#0b1628",
        plot_bgcolor="#0b1628",
        legend=dict(
            bgcolor="#0f1f3d", bordercolor="#1e3d7a", borderwidth=1,
            font=dict(color="#e8edf5", size=11),
            orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
        ),
        font=dict(color="#e8edf5"),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class="legend">
      <span style="color:#ef4444">⬤ Critical</span>
      <span style="color:#f97316">⬤ High</span>
      <span style="color:#eab308">⬤ Medium</span>
      <span style="color:#22c55e">⬤ Low</span>
    </div>
    """, unsafe_allow_html=True)

# ── PLACEHOLDER PAGES ─────────────────────────────────────────────────────────
else:
    labels = {
        "countries":   ("🌍", "Country Analysis"),
        "forecast":    ("📈", "Revenue Forecast"),
        "pricing":     ("💲", "Pricing Intel"),
        "tenders":     ("📋", "Tenders"),
        "competitors": ("🏆", "Competitors"),
        "exhibitions": ("📅", "Exhibitions"),
        "regulatory":  ("📜", "Regulatory"),
    }
    icon, title = labels.get(page, ("📄", page.title()))
    st.markdown(f"""
    <div class="placeholder">
      <div class="ph-icon">{icon}</div>
      <div class="ph-title">{title}</div>
      <div class="ph-sub">Coming soon</div>
    </div>
    """, unsafe_allow_html=True)

# close main-wrap
st.markdown('</div>', unsafe_allow_html=True)
