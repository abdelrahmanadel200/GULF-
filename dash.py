import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AMECATH Market Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide default streamlit chrome
st.markdown("""
<style>
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background: #0b1628; }
</style>
""", unsafe_allow_html=True)

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { background: #0b1628; height: 100%; }

  .dash {
    background: #0b1628;
    color: #e8edf5;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    display: flex;
  }

  /* ── Sidebar ── */
  .sidebar {
    width: 200px;
    min-width: 200px;
    background: #070f1f;
    border-right: 1px solid #1e3d7a;
    display: flex;
    flex-direction: column;
    padding: 18px 0;
    position: fixed;
    top: 0; left: 0; bottom: 0;
    z-index: 10;
  }
  .logo {
    padding: 0 16px 18px;
    border-bottom: 1px solid #1e3d7a;
    margin-bottom: 10px;
  }
  .logo-text { font-size: 15px; font-weight: 700; color: #60a5fa; letter-spacing: 1.5px; }
  .logo-sub  { font-size: 10px; color: #3a5278; margin-top: 2px; letter-spacing: 0.5px; }

  .nav-section-label {
    font-size: 9px;
    letter-spacing: 1.5px;
    color: #2a4060;
    text-transform: uppercase;
    padding: 14px 16px 6px;
    font-weight: 700;
  }
  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    cursor: pointer;
    font-size: 12px;
    color: #6a85b0;
    border-left: 3px solid transparent;
    transition: all 0.15s;
    user-select: none;
  }
  .nav-item:hover  { background: #0f1f3d; color: #c8d8f0; }
  .nav-item.active { background: #0f1f3d; color: #60a5fa; border-left-color: #2563eb; font-weight: 600; }
  .nav-icon  { font-size: 15px; width: 18px; text-align: center; }

  /* ── Main ── */
  .main { margin-left: 200px; flex: 1; min-height: 100vh; }

  /* ── Banner ── */
  .top-banner {
    background: linear-gradient(135deg, #0d2145 0%, #1a3a6e 50%, #0d2145 100%);
    border: 1px solid #1e3d7a;
    border-radius: 14px;
    padding: 20px 32px;
    margin: 16px 16px 0;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .top-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 50% -20%, #2563eb22 0%, transparent 65%);
    pointer-events: none;
  }
  .banner-title {
    font-size: 18px; font-weight: 700; letter-spacing: 2px; color: #e8edf5;
    display: flex; align-items: center; justify-content: center; gap: 10px;
  }
  .banner-sub {
    font-size: 11px; color: #f59e0b; margin-top: 5px;
    display: flex; align-items: center; justify-content: center; gap: 5px;
  }

  /* ── Section header ── */
  .section-header { display: flex; align-items: center; gap: 10px; margin: 18px 16px 12px; }
  .section-title  { font-size: 15px; font-weight: 600; color: #c8d8f0; }

  /* ── KPI grid ── */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin: 0 16px 10px;
  }
  .kpi-card {
    background: #0f1f3d;
    border: 1px solid #1e3d7a;
    border-radius: 12px;
    padding: 16px 12px 12px;
    display: flex; flex-direction: column; align-items: center; text-align: center; gap: 5px;
    transition: border-color 0.2s, transform 0.15s;
    cursor: default;
  }
  .kpi-card:hover { border-color: #2563eb; transform: translateY(-1px); }
  .kpi-icon  { font-size: 20px; margin-bottom: 2px; }
  .kpi-label { font-size: 9px; letter-spacing: 1px; color: #6a85b0; text-transform: uppercase; font-weight: 600; }
  .kpi-value { font-size: 22px; font-weight: 700; color: #e8edf5; line-height: 1.1; }
  .kpi-value.accent { color: #60a5fa; }
  .kpi-value.gold   { color: #f59e0b; }
  .kpi-sub          { font-size: 10px; color: #3b82f6; font-weight: 500; }
  .kpi-sub.muted    { color: #6a85b0; }
  .kpi-sub.green    { color: #34d399; }
  .kpi-sub.amber    { color: #f59e0b; }

  .divider { height: 1px; background: #1e3d7a; margin: 4px 16px 10px; }

  /* ── Placeholder pages ── */
  .page { display: none; }
  .page.active { display: block; }
  .placeholder-page {
    margin: 16px;
    background: #0f1f3d;
    border: 1px dashed #1e3d7a;
    border-radius: 14px;
    padding: 60px 32px;
    text-align: center;
    color: #3a5278;
  }
  .placeholder-icon  { font-size: 40px; margin-bottom: 14px; }
  .placeholder-title { font-size: 18px; font-weight: 600; color: #6a85b0; margin-bottom: 8px; }
  .placeholder-sub   { font-size: 13px; color: #3a5278; }
</style>
</head>
<body>
<div class="dash">

  <!-- ── Sidebar ── -->
  <div class="sidebar">
    <div class="logo">
      <div class="logo-text">AMECATH</div>
      <div class="logo-sub">Market Intelligence</div>
    </div>

    <div class="nav-section-label">Main</div>
    <div class="nav-item active" onclick="navigate(this,'overview')">
      <span class="nav-icon">🏠</span><span>Overview</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'countries')">
      <span class="nav-icon">🌍</span><span>Country Analysis</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'forecast')">
      <span class="nav-icon">📈</span><span>Revenue Forecast</span>
    </div>

    <div class="nav-section-label">Market</div>
    <div class="nav-item" onclick="navigate(this,'pricing')">
      <span class="nav-icon">💲</span><span>Pricing Intel</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'tenders')">
      <span class="nav-icon">📋</span><span>Tenders</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'competitors')">
      <span class="nav-icon">🏆</span><span>Competitors</span>
    </div>

    <div class="nav-section-label">Field</div>
    <div class="nav-item" onclick="navigate(this,'hotareas')">
      <span class="nav-icon">📍</span><span>Hot Areas</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'exhibitions')">
      <span class="nav-icon">📅</span><span>Exhibitions</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'regulatory')">
      <span class="nav-icon">📜</span><span>Regulatory</span>
    </div>
  </div>

  <!-- ── Main content ── -->
  <div class="main">

    <!-- Overview -->
    <div class="page active" id="page-overview">
      <div class="top-banner">
        <div class="banner-title">🌐 REGIONAL EXECUTIVE OVERVIEW</div>
        <div class="banner-sub">📌 Scope: Middle East &amp; GCC Markets Performance</div>
      </div>

      <div class="section-header">
        <span style="font-size:16px">🌐</span>
        <span class="section-title">Gulf Region — Executive Overview</span>
      </div>

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
          <div class="kpi-icon">🩺</div>
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
      <div style="text-align:center;padding:8px 16px 16px;font-size:10px;color:#2a4060;">
        Data source: Amecath_Dash.xlsx &nbsp;·&nbsp; 2026 Edition &nbsp;·&nbsp; 9 Markets
      </div>
    </div>

    <!-- Country Analysis -->
    <div class="page" id="page-countries">
      <div class="placeholder-page">
        <div class="placeholder-icon">🌍</div>
        <div class="placeholder-title">Country Analysis</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

<!-- Hot Areas -->
<div class="page" id="page-hotareas">
  <style>
    .ha-wrap { padding: 16px; }
    .ha-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
    .ha-title { font-size:15px; font-weight:600; color:#c8d8f0; display:flex; align-items:center; gap:8px; }
    .ha-tabs { display:flex; gap:6px; flex-wrap:wrap; margin-bottom:14px; }
    .ha-tab { padding:5px 12px; border-radius:20px; font-size:11px; font-weight:600; cursor:pointer; border:1px solid #1e3d7a; color:#6a85b0; background:#0f1f3d; transition:all .15s; user-select:none; }
    .ha-tab:hover { border-color:#2563eb; color:#c8d8f0; }
    .ha-tab.active { background:#1e3d7a; color:#e8edf5; border-color:#3b82f6; }
    .ha-map-area { position:relative; background:#0a1525; border:1px solid #1e3d7a; border-radius:14px; overflow:hidden; }
    #haCanvas { display:block; width:100%; cursor:crosshair; }
    .ha-tooltip { position:absolute; pointer-events:none; background:#0d2145; border:1px solid #2563eb; border-radius:10px; padding:10px 14px; font-size:12px; color:#e8edf5; min-width:180px; z-index:20; opacity:0; transition:opacity .15s; }
    .ha-tt-name { font-size:13px; font-weight:700; color:#60a5fa; margin-bottom:6px; }
    .ha-tt-row { display:flex; justify-content:space-between; gap:16px; margin-top:3px; font-size:11px; }
    .ha-tt-label { color:#6a85b0; }
    .ha-tt-val { color:#e8edf5; font-weight:600; }
    .ha-legend { display:flex; align-items:center; gap:8px; margin-top:10px; font-size:11px; color:#6a85b0; }
    .ha-legend-bar { width:160px; height:10px; border-radius:5px; }
  </style>

  <div class="ha-wrap">
    <div class="ha-header">
      <div class="ha-title">📍 Hot Areas — Dialysis Heatmap</div>
      <div style="font-size:11px;color:#3a5278">Hover over a point for details</div>
    </div>

    <div class="ha-tabs" id="haTabs"></div>

    <div class="ha-map-area" id="haMapArea">
      <canvas id="haCanvas"></canvas>
      <div class="ha-tooltip" id="haTooltip">
        <div class="ha-tt-name" id="ha-tt-name"></div>
        <div class="ha-tt-row"><span class="ha-tt-label">Rank</span><span class="ha-tt-val" id="ha-tt-rank"></span></div>
        <div class="ha-tt-row"><span class="ha-tt-label">Centers</span><span class="ha-tt-val" id="ha-tt-centers"></span></div>
        <div class="ha-tt-row"><span class="ha-tt-label">HD Patients</span><span class="ha-tt-val" id="ha-tt-hd"></span></div>
        <div class="ha-tt-row"><span class="ha-tt-label">Market Priority</span><span class="ha-tt-val" id="ha-tt-priority"></span></div>
      </div>
    </div>

    <div class="ha-legend">
      <span>Low</span>
      <canvas class="ha-legend-bar" id="haLegendBar" width="160" height="10"></canvas>
      <span>High intensity</span>
    </div>
  </div>

  <script>
  (function() {
    const HA_DATA = {
      "Saudi Arabia": {
        flag:"🇸🇦",
        areas:[
          {name:"Riyadh",        x:.48,y:.52,rank:1,centers:39,hd:5700, priority:"Critical"},
          {name:"Jeddah",        x:.30,y:.60,rank:2,centers:12,hd:2100, priority:"High"},
          {name:"Makkah",        x:.28,y:.62,rank:3,centers:12,hd:1950, priority:"High"},
          {name:"Dammam/Khobar", x:.70,y:.50,rank:4,centers:6, hd:1200, priority:"High"},
          {name:"Madinah",       x:.33,y:.42,rank:5,centers:5, hd:900,  priority:"Medium"},
          {name:"Buraydah",      x:.46,y:.35,rank:6,centers:7, hd:1020, priority:"Medium"},
          {name:"Hail",          x:.44,y:.27,rank:7,centers:6, hd:870,  priority:"Medium"},
          {name:"Abha",          x:.32,y:.72,rank:8,centers:4, hd:600,  priority:"Low"},
          {name:"Tabuk",         x:.22,y:.28,rank:9,centers:3, hd:450,  priority:"Low"},
        ]
      },
      "UAE": {
        flag:"🇦🇪",
        areas:[
          {name:"Dubai",       x:.68,y:.55,rank:1,centers:7,hd:840, priority:"Critical"},
          {name:"Abu Dhabi",   x:.35,y:.62,rank:2,centers:5,hd:600, priority:"High"},
          {name:"Sharjah",     x:.72,y:.45,rank:3,centers:3,hd:360, priority:"Medium"},
          {name:"Al Ain",      x:.55,y:.72,rank:4,centers:2,hd:240, priority:"Medium"},
          {name:"Ajman",       x:.74,y:.40,rank:5,centers:2,hd:200, priority:"Low"},
          {name:"Fujairah/RAK",x:.85,y:.35,rank:6,centers:2,hd:180, priority:"Low"},
        ]
      },
      "Qatar": {
        flag:"🇶🇦",
        areas:[
          {name:"Doha — FBJ Kidney Ctr",x:.40,y:.60,rank:1,centers:4,hd:720,priority:"Critical"},
          {name:"Al Wakrah",            x:.42,y:.70,rank:2,centers:2,hd:240,priority:"Medium"},
          {name:"Al Khor",              x:.38,y:.35,rank:3,centers:1,hd:120,priority:"Low"},
          {name:"Al Shahania",          x:.35,y:.30,rank:4,centers:1,hd:80, priority:"Low"},
          {name:"Lusail / Al Daayen",   x:.42,y:.50,rank:5,centers:1,hd:60, priority:"Low"},
        ]
      },
      "Kuwait": {
        flag:"🇰🇼",
        areas:[
          {name:"Kuwait City",    x:.42,y:.55,rank:1,centers:8,hd:970, priority:"Critical"},
          {name:"Ahmadi",         x:.48,y:.68,rank:2,centers:3,hd:390, priority:"High"},
          {name:"Hawalli",        x:.45,y:.52,rank:3,centers:3,hd:340, priority:"Medium"},
          {name:"Farwaniya",      x:.38,y:.48,rank:4,centers:3,hd:280, priority:"Medium"},
          {name:"Jahra",          x:.30,y:.42,rank:5,centers:2,hd:180, priority:"Low"},
          {name:"Sabah Al-Ahmad", x:.52,y:.72,rank:6,centers:1,hd:80,  priority:"Low"},
        ]
      },
      "Iraq": {
        flag:"🇮🇶",
        areas:[
          {name:"Baghdad",          x:.52,y:.48,rank:1,centers:11,hd:3967,priority:"Critical"},
          {name:"Basra",            x:.60,y:.78,rank:2,centers:3, hd:1500,priority:"Critical"},
          {name:"Erbil",            x:.65,y:.30,rank:3,centers:4, hd:1200,priority:"High"},
          {name:"Sulaymaniyah",     x:.72,y:.32,rank:4,centers:3, hd:900, priority:"High"},
          {name:"Kirkuk",           x:.62,y:.40,rank:5,centers:2, hd:463, priority:"Medium"},
          {name:"Mosul",            x:.58,y:.28,rank:6,centers:2, hd:420, priority:"Medium"},
          {name:"Najaf",            x:.50,y:.60,rank:7,centers:2, hd:380, priority:"Medium"},
          {name:"Diwaniyah/Amarah", x:.53,y:.65,rank:8,centers:2, hd:300, priority:"Low"},
        ]
      },
      "Jordan": {
        flag:"🇯🇴",
        areas:[
          {name:"Amman", x:.48,y:.52,rank:1,centers:5,hd:3200,priority:"Critical"},
          {name:"Irbid",  x:.46,y:.38,rank:2,centers:2,hd:960, priority:"High"},
          {name:"Zarqa",  x:.52,y:.48,rank:3,centers:2,hd:768, priority:"Medium"},
          {name:"Salt",   x:.44,y:.54,rank:4,centers:1,hd:480, priority:"Medium"},
          {name:"Karak",  x:.46,y:.66,rank:5,centers:1,hd:320, priority:"Low"},
        ]
      },
      "Lebanon": {
        flag:"🇱🇧",
        areas:[
          {name:"Greater Beirut",x:.40,y:.50,rank:1,centers:30,hd:2365,priority:"Critical"},
          {name:"Tripoli",       x:.38,y:.35,rank:2,centers:12,hd:850, priority:"High"},
          {name:"Sidon",         x:.38,y:.62,rank:3,centers:8, hd:520, priority:"Medium"},
          {name:"Zahle",         x:.48,y:.52,rank:4,centers:6, hd:400, priority:"Medium"},
          {name:"Jounieh",       x:.42,y:.45,rank:5,centers:4, hd:280, priority:"Low"},
          {name:"Nabatieh",      x:.40,y:.68,rank:6,centers:3, hd:200, priority:"Low"},
        ]
      },
      "Oman": {
        flag:"🇴🇲",
        areas:[
          {name:"Muscat",    x:.62,y:.40,rank:1,centers:4,hd:1000,priority:"Critical"},
          {name:"Salalah",   x:.45,y:.80,rank:2,centers:2,hd:500, priority:"High"},
          {name:"Sohar",     x:.55,y:.28,rank:3,centers:2,hd:380, priority:"Medium"},
          {name:"Ibri",      x:.48,y:.45,rank:4,centers:2,hd:250, priority:"Medium"},
          {name:"Barka/Seeb",x:.60,y:.38,rank:5,centers:1,hd:180, priority:"Low"},
        ]
      },
      "Bahrain": {
        flag:"🇧🇭",
        areas:[
          {name:"Manama / Riffa",  x:.52,y:.50,rank:1,centers:5,hd:2500,priority:"Critical"},
          {name:"A'Ali",           x:.48,y:.56,rank:2,centers:2,hd:900, priority:"High"},
          {name:"Muharraq",        x:.58,y:.42,rank:3,centers:2,hd:680, priority:"Medium"},
          {name:"Saar",            x:.44,y:.48,rank:4,centers:1,hd:320, priority:"Low"},
          {name:"Riffa (private)", x:.52,y:.60,rank:5,centers:1,hd:150, priority:"Low"},
        ]
      }
    };

    const HA_PRIORITY_COLOR = {Critical:"#ef4444",High:"#f97316",Medium:"#eab308",Low:"#22c55e"};
    let haActive = "Saudi Arabia";
    let haAnimPhase = 0;
    let haPulseT = 0;

    const haTabs    = document.getElementById("haTabs");
    const haCanvas  = document.getElementById("haCanvas");
    const haCtx     = haCanvas.getContext("2d");
    const haTooltip = document.getElementById("haTooltip");
    const haMapArea = document.getElementById("haMapArea");
    const haLegend  = document.getElementById("haLegendBar");
    const haLCtx    = haLegend.getContext("2d");

    function haFlameColor(t, alpha) {
      const r = Math.min(255, Math.round(255 * Math.min(t * 2, 1)));
      const g = Math.min(255, Math.round(255 * Math.max(0, t * 2 - 0.5)));
      const b = Math.round(10 * (1 - t));
      return `rgba(${r},${g},${b},${alpha})`;
    }

    function haResize() {
      const W = haMapArea.clientWidth;
      const H = Math.round(W * 0.52);
      haCanvas.width  = W;
      haCanvas.height = H;
    }

    function haDrawGrid(W, H) {
      haCtx.strokeStyle = "rgba(30,61,122,0.3)";
      haCtx.lineWidth = 0.5;
      for (let x = 0; x < W; x += W/8) { haCtx.beginPath(); haCtx.moveTo(x,0); haCtx.lineTo(x,H); haCtx.stroke(); }
      for (let y = 0; y < H; y += H/6) { haCtx.beginPath(); haCtx.moveTo(0,y); haCtx.lineTo(W,y); haCtx.stroke(); }
    }

    function haDrawBlobs(areas, W, H) {
      areas.forEach(a => {
        const cx = a.x*W, cy = a.y*H;
        const intensity = 1 - (a.rank-1)/areas.length;
        const r = (40 + intensity*70)*(W/700);
        const grad = haCtx.createRadialGradient(cx,cy,0,cx,cy,r);
        const alpha = 0.18 + intensity*0.32;
        grad.addColorStop(0,   haFlameColor(intensity, alpha));
        grad.addColorStop(0.5, haFlameColor(intensity*0.6, alpha*0.5));
        grad.addColorStop(1,   "rgba(0,0,0,0)");
        haCtx.beginPath(); haCtx.arc(cx,cy,r,0,Math.PI*2);
        haCtx.fillStyle = grad; haCtx.fill();
      });
    }

    function haDrawDots(areas, W, H, phase) {
      areas.forEach((a, i) => {
        const cx = a.x*W, cy = a.y*H;
        const intensity = 1 - (a.rank-1)/areas.length;
        const appear = Math.min(1, Math.max(0, (phase - i*0.12)/0.15));
        if (appear <= 0) return;
        const baseR = (5 + intensity*9)*(W/700);
        const pc = HA_PRIORITY_COLOR[a.priority];
        const pulse = Math.sin(haPulseT*0.05 + i*0.8)*0.5 + 0.5;
        const ringR = baseR + 3 + pulse*5;

        haCtx.beginPath(); haCtx.arc(cx,cy,ringR,0,Math.PI*2);
        haCtx.strokeStyle = pc+"55"; haCtx.lineWidth = 1.5; haCtx.stroke();

        haCtx.beginPath(); haCtx.arc(cx,cy,baseR*appear,0,Math.PI*2);
        haCtx.fillStyle = pc; haCtx.fill();

        haCtx.beginPath(); haCtx.arc(cx,cy,baseR*appear*0.45,0,Math.PI*2);
        haCtx.fillStyle = "rgba(255,255,255,0.7)"; haCtx.fill();

        if (appear >= 1 && W > 400) {
          haCtx.font = `bold ${Math.round(9*W/700+8)}px 'Segoe UI',sans-serif`;
          haCtx.fillStyle = "#e8edf5"; haCtx.textAlign = "center";
          const label = a.rank===1 ? a.name : (a.name.length>14 ? a.name.slice(0,13)+"…" : a.name);
          haCtx.fillText(label, cx, cy - baseR - 5);
        }
      });
    }

    function haDrawLegend() {
      const grad = haLCtx.createLinearGradient(0,0,160,0);
      for (let i=0; i<=10; i++) grad.addColorStop(i/10, haFlameColor(i/10, 1));
      haLCtx.clearRect(0,0,160,10);
      haLCtx.fillStyle = grad;
      haLCtx.roundRect(0,0,160,10,5); haLCtx.fill();
    }

    function haRenderAll() {
      const W = haCanvas.width, H = haCanvas.height;
      const areas = HA_DATA[haActive].areas;
      haCtx.clearRect(0,0,W,H);
      haCtx.fillStyle = "#0a1525"; haCtx.fillRect(0,0,W,H);
      haDrawGrid(W,H);
      haDrawBlobs(areas,W,H);
      haDrawDots(areas,W,H,haAnimPhase);
      haDrawLegend();
    }

    function haAnimate() {
      haPulseT++;
      if (haAnimPhase < 1.5) haAnimPhase += 0.018;
      haRenderAll();
      requestAnimationFrame(haAnimate);
    }

    function haGetHit(mx, my) {
      const W = haCanvas.width, H = haCanvas.height;
      const areas = HA_DATA[haActive].areas;
      for (let i = areas.length-1; i >= 0; i--) {
        const a = areas[i];
        const cx = a.x*W, cy = a.y*H;
        const intensity = 1 - (a.rank-1)/areas.length;
        const r = (8 + intensity*9)*(W/700) + 6;
        if (Math.hypot(mx-cx, my-cy) < r) return a;
      }
      return null;
    }

    // Build tabs
    Object.keys(HA_DATA).forEach(c => {
      const el = document.createElement("div");
      el.className = "ha-tab" + (c===haActive ? " active" : "");
      el.textContent = HA_DATA[c].flag + " " + c;
      el.onclick = () => {
        haActive = c;
        document.querySelectorAll(".ha-tab").forEach(t => t.classList.remove("active"));
        el.classList.add("active");
        haAnimPhase = 0;
        haRenderAll();
      };
      haTabs.appendChild(el);
    });

    // Tooltip
    haCanvas.addEventListener("mousemove", e => {
      const rect = haCanvas.getBoundingClientRect();
      const scaleX = haCanvas.width/rect.width;
      const scaleY = haCanvas.height/rect.height;
      const mx = (e.clientX - rect.left)*scaleX;
      const my = (e.clientY - rect.top)*scaleY;
      const hit = haGetHit(mx, my);
      if (hit) {
        document.getElementById("ha-tt-name").textContent    = hit.name;
        document.getElementById("ha-tt-rank").textContent    = "#"+hit.rank+" in "+haActive;
        document.getElementById("ha-tt-centers").textContent = hit.centers+" dialysis centers";
        document.getElementById("ha-tt-hd").textContent      = hit.hd.toLocaleString()+" patients (est.)";
        const prioEl = document.getElementById("ha-tt-priority");
        prioEl.textContent = hit.priority;
        prioEl.style.color = HA_PRIORITY_COLOR[hit.priority];
        const pxX = e.clientX - rect.left;
        const pxY = e.clientY - rect.top;
        const ttW = 190, ttH = 120;
        let left = pxX + 14;
        let top  = pxY - ttH/2;
        if (left + ttW > rect.width - 10) left = pxX - ttW - 14;
        if (top < 4) top = 4;
        haTooltip.style.left    = left+"px";
        haTooltip.style.top     = top+"px";
        haTooltip.style.opacity = "1";
        haCanvas.style.cursor   = "pointer";
      } else {
        haTooltip.style.opacity = "0";
        haCanvas.style.cursor   = "crosshair";
      }
    });
    haCanvas.addEventListener("mouseleave", () => { haTooltip.style.opacity = "0"; });

    window.addEventListener("resize", () => { haResize(); haAnimPhase = 0; });

    haResize();
    haAnimate();
  })();
  </script>
</div>

    <!-- Revenue Forecast -->
    <div class="page" id="page-forecast">
      <div class="placeholder-page">
        <div class="placeholder-icon">📈</div>
        <div class="placeholder-title">Revenue Forecast</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Pricing Intel -->
    <div class="page" id="page-pricing">
      <div class="placeholder-page">
        <div class="placeholder-icon">💲</div>
        <div class="placeholder-title">Pricing Intel</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Tenders -->
    <div class="page" id="page-tenders">
      <div class="placeholder-page">
        <div class="placeholder-icon">📋</div>
        <div class="placeholder-title">Tenders</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Competitors -->
    <div class="page" id="page-competitors">
      <div class="placeholder-page">
        <div class="placeholder-icon">🏆</div>
        <div class="placeholder-title">Competitors</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AMECATH Market Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide default streamlit chrome
st.markdown("""
<style>
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background: #0b1628; }
</style>
""", unsafe_allow_html=True)

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { background: #0b1628; height: 100%; }

  .dash {
    background: #0b1628;
    color: #e8edf5;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    display: flex;
  }

  /* ── Sidebar ── */
  .sidebar {
    width: 200px;
    min-width: 200px;
    background: #070f1f;
    border-right: 1px solid #1e3d7a;
    display: flex;
    flex-direction: column;
    padding: 18px 0;
    position: fixed;
    top: 0; left: 0; bottom: 0;
    z-index: 10;
  }
  .logo {
    padding: 0 16px 18px;
    border-bottom: 1px solid #1e3d7a;
    margin-bottom: 10px;
  }
  .logo-text { font-size: 15px; font-weight: 700; color: #60a5fa; letter-spacing: 1.5px; }
  .logo-sub  { font-size: 10px; color: #3a5278; margin-top: 2px; letter-spacing: 0.5px; }

  .nav-section-label {
    font-size: 9px;
    letter-spacing: 1.5px;
    color: #2a4060;
    text-transform: uppercase;
    padding: 14px 16px 6px;
    font-weight: 700;
  }
  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    cursor: pointer;
    font-size: 12px;
    color: #6a85b0;
    border-left: 3px solid transparent;
    transition: all 0.15s;
    user-select: none;
  }
  .nav-item:hover  { background: #0f1f3d; color: #c8d8f0; }
  .nav-item.active { background: #0f1f3d; color: #60a5fa; border-left-color: #2563eb; font-weight: 600; }
  .nav-icon  { font-size: 15px; width: 18px; text-align: center; }

  /* ── Main ── */
  .main { margin-left: 200px; flex: 1; min-height: 100vh; }

  /* ── Banner ── */
  .top-banner {
    background: linear-gradient(135deg, #0d2145 0%, #1a3a6e 50%, #0d2145 100%);
    border: 1px solid #1e3d7a;
    border-radius: 14px;
    padding: 20px 32px;
    margin: 16px 16px 0;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .top-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 50% -20%, #2563eb22 0%, transparent 65%);
    pointer-events: none;
  }
  .banner-title {
    font-size: 18px; font-weight: 700; letter-spacing: 2px; color: #e8edf5;
    display: flex; align-items: center; justify-content: center; gap: 10px;
  }
  .banner-sub {
    font-size: 11px; color: #f59e0b; margin-top: 5px;
    display: flex; align-items: center; justify-content: center; gap: 5px;
  }

  /* ── Section header ── */
  .section-header { display: flex; align-items: center; gap: 10px; margin: 18px 16px 12px; }
  .section-title  { font-size: 15px; font-weight: 600; color: #c8d8f0; }

  /* ── KPI grid ── */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin: 0 16px 10px;
  }
  .kpi-card {
    background: #0f1f3d;
    border: 1px solid #1e3d7a;
    border-radius: 12px;
    padding: 16px 12px 12px;
    display: flex; flex-direction: column; align-items: center; text-align: center; gap: 5px;
    transition: border-color 0.2s, transform 0.15s;
    cursor: default;
  }
  .kpi-card:hover { border-color: #2563eb; transform: translateY(-1px); }
  .kpi-icon  { font-size: 20px; margin-bottom: 2px; }
  .kpi-label { font-size: 9px; letter-spacing: 1px; color: #6a85b0; text-transform: uppercase; font-weight: 600; }
  .kpi-value { font-size: 22px; font-weight: 700; color: #e8edf5; line-height: 1.1; }
  .kpi-value.accent { color: #60a5fa; }
  .kpi-value.gold   { color: #f59e0b; }
  .kpi-sub          { font-size: 10px; color: #3b82f6; font-weight: 500; }
  .kpi-sub.muted    { color: #6a85b0; }
  .kpi-sub.green    { color: #34d399; }
  .kpi-sub.amber    { color: #f59e0b; }

  .divider { height: 1px; background: #1e3d7a; margin: 4px 16px 10px; }

  /* ── Placeholder pages ── */
  .page { display: none; }
  .page.active { display: block; }
  .placeholder-page {
    margin: 16px;
    background: #0f1f3d;
    border: 1px dashed #1e3d7a;
    border-radius: 14px;
    padding: 60px 32px;
    text-align: center;
    color: #3a5278;
  }
  .placeholder-icon  { font-size: 40px; margin-bottom: 14px; }
  .placeholder-title { font-size: 18px; font-weight: 600; color: #6a85b0; margin-bottom: 8px; }
  .placeholder-sub   { font-size: 13px; color: #3a5278; }
</style>
</head>
<body>
<div class="dash">

  <!-- ── Sidebar ── -->
  <div class="sidebar">
    <div class="logo">
      <div class="logo-text">AMECATH</div>
      <div class="logo-sub">Market Intelligence</div>
    </div>

    <div class="nav-section-label">Main</div>
    <div class="nav-item active" onclick="navigate(this,'overview')">
      <span class="nav-icon">🏠</span><span>Overview</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'countries')">
      <span class="nav-icon">🌍</span><span>Country Analysis</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'forecast')">
      <span class="nav-icon">📈</span><span>Revenue Forecast</span>
    </div>

    <div class="nav-section-label">Market</div>
    <div class="nav-item" onclick="navigate(this,'pricing')">
      <span class="nav-icon">💲</span><span>Pricing Intel</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'tenders')">
      <span class="nav-icon">📋</span><span>Tenders</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'competitors')">
      <span class="nav-icon">🏆</span><span>Competitors</span>
    </div>

    <div class="nav-section-label">Field</div>
    <div class="nav-item" onclick="navigate(this,'hotareas')">
      <span class="nav-icon">📍</span><span>Hot Areas</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'exhibitions')">
      <span class="nav-icon">📅</span><span>Exhibitions</span>
    </div>
    <div class="nav-item" onclick="navigate(this,'regulatory')">
      <span class="nav-icon">📜</span><span>Regulatory</span>
    </div>
  </div>

  <!-- ── Main content ── -->
  <div class="main">

    <!-- Overview -->
    <div class="page active" id="page-overview">
      <div class="top-banner">
        <div class="banner-title">🌐 REGIONAL EXECUTIVE OVERVIEW</div>
        <div class="banner-sub">📌 Scope: Middle East &amp; GCC Markets Performance</div>
      </div>

      <div class="section-header">
        <span style="font-size:16px">🌐</span>
        <span class="section-title">Gulf Region — Executive Overview</span>
      </div>

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
          <div class="kpi-icon">🩺</div>
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
      <div style="text-align:center;padding:8px 16px 16px;font-size:10px;color:#2a4060;">
        Data source: Amecath_Dash.xlsx &nbsp;·&nbsp; 2026 Edition &nbsp;·&nbsp; 9 Markets
      </div>
    </div>

    <!-- Country Analysis -->
    <div class="page" id="page-countries">
      <div class="placeholder-page">
        <div class="placeholder-icon">🌍</div>
        <div class="placeholder-title">Country Analysis</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Revenue Forecast -->
    <div class="page" id="page-forecast">
      <div class="placeholder-page">
        <div class="placeholder-icon">📈</div>
        <div class="placeholder-title">Revenue Forecast</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Pricing Intel -->
    <div class="page" id="page-pricing">
      <div class="placeholder-page">
        <div class="placeholder-icon">💲</div>
        <div class="placeholder-title">Pricing Intel</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Tenders -->
    <div class="page" id="page-tenders">
      <div class="placeholder-page">
        <div class="placeholder-icon">📋</div>
        <div class="placeholder-title">Tenders</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Competitors -->
    <div class="page" id="page-competitors">
      <div class="placeholder-page">
        <div class="placeholder-icon">🏆</div>
        <div class="placeholder-title">Competitors</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Hot Areas -->
    <div class="page" id="page-hotareas">
      <div class="placeholder-page">
        <div class="placeholder-icon">📍</div>
        <div class="placeholder-title">Hot Areas</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Exhibitions -->
    <div class="page" id="page-exhibitions">
      <div class="placeholder-page">
        <div class="placeholder-icon">📅</div>
        <div class="placeholder-title">Exhibitions</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Regulatory -->
    <div class="page" id="page-regulatory">
      <div class="placeholder-page">
        <div class="placeholder-icon">📜</div>
        <div class="placeholder-title">Regulatory</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

  </div>
</div>

<script>
  function navigate(el, pageId) {
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    el.classList.add('active');
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page-' + pageId).classList.add('active');
  }
</script>
</body>
</html>
"""

components.html(dashboard_html, height=800, scrolling=False)

    <!-- Exhibitions -->
    <div class="page" id="page-exhibitions">
      <div class="placeholder-page">
        <div class="placeholder-icon">📅</div>
        <div class="placeholder-title">Exhibitions</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

    <!-- Regulatory -->
    <div class="page" id="page-regulatory">
      <div class="placeholder-page">
        <div class="placeholder-icon">📜</div>
        <div class="placeholder-title">Regulatory</div>
        <div class="placeholder-sub">Coming soon — قولنا إيه اللي عايزه هنا</div>
      </div>
    </div>

  </div>
</div>

<script>
  function navigate(el, pageId) {
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    el.classList.add('active');
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page-' + pageId).classList.add('active');
  }
</script>
</body>
</html>
"""

components.html(dashboard_html, height=800, scrolling=False)
