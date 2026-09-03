import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AMECATH Market Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { background: #0b1628; height: 100%; }
  .dash { background: #0b1628; color: #e8edf5; font-family: 'Segoe UI', system-ui, sans-serif; min-height: 100vh; display: flex; }
  .sidebar { width: 200px; min-width: 200px; background: #070f1f; border-right: 1px solid #1e3d7a; display: flex; flex-direction: column; padding: 18px 0; position: fixed; top: 0; left: 0; bottom: 0; z-index: 10; }
  .logo { padding: 0 16px 18px; border-bottom: 1px solid #1e3d7a; margin-bottom: 10px; }
  .logo-text { font-size: 15px; font-weight: 700; color: #60a5fa; letter-spacing: 1.5px; }
  .logo-sub  { font-size: 10px; color: #3a5278; margin-top: 2px; letter-spacing: 0.5px; }
  .nav-section-label { font-size: 9px; letter-spacing: 1.5px; color: #2a4060; text-transform: uppercase; padding: 14px 16px 6px; font-weight: 700; }
  .nav-item { display: flex; align-items: center; gap: 10px; padding: 10px 16px; cursor: pointer; font-size: 12px; color: #6a85b0; border-left: 3px solid transparent; transition: all 0.15s; user-select: none; }
  .nav-item:hover  { background: #0f1f3d; color: #c8d8f0; }
  .nav-item.active { background: #0f1f3d; color: #60a5fa; border-left-color: #2563eb; font-weight: 600; }
  .nav-icon  { font-size: 15px; width: 18px; text-align: center; }
  .main { margin-left: 200px; flex: 1; min-height: 100vh; }
  .top-banner { background: linear-gradient(135deg, #0d2145 0%, #1a3a6e 50%, #0d2145 100%); border: 1px solid #1e3d7a; border-radius: 14px; padding: 20px 32px; margin: 16px 16px 0; text-align: center; position: relative; overflow: hidden; }
  .top-banner::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(ellipse at 50% -20%, #2563eb22 0%, transparent 65%); pointer-events: none; }
  .banner-title { font-size: 18px; font-weight: 700; letter-spacing: 2px; color: #e8edf5; display: flex; align-items: center; justify-content: center; gap: 10px; }
  .banner-sub { font-size: 11px; color: #f59e0b; margin-top: 5px; display: flex; align-items: center; justify-content: center; gap: 5px; }
  .section-header { display: flex; align-items: center; gap: 10px; margin: 18px 16px 12px; }
  .section-title  { font-size: 15px; font-weight: 600; color: #c8d8f0; }
  .kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin: 0 16px 10px; }
  .kpi-card { background: #0f1f3d; border: 1px solid #1e3d7a; border-radius: 12px; padding: 16px 12px 12px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 5px; transition: border-color 0.2s, transform 0.15s; cursor: default; }
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
  .page { display: none; }
  .page.active { display: block; }
  .placeholder-page { margin: 16px; background: #0f1f3d; border: 1px dashed #1e3d7a; border-radius: 14px; padding: 60px 32px; text-align: center; color: #3a5278; }
  .placeholder-icon  { font-size: 40px; margin-bottom: 14px; }
  .placeholder-title { font-size: 18px; font-weight: 600; color: #6a85b0; margin-bottom: 8px; }
  .placeholder-sub   { font-size: 13px; color: #3a5278; }
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
</head>
<body>
<div class="dash">

  <div class="sidebar">
    <div class="logo">
      <div class="logo-text">AMECATH</div>
      <div class="logo-sub">Market Intelligence</div>
    </div>
    <div class="nav-section-label">Main</div>
    <div class="nav-item active" onclick="navigate(this,'overview')"><span class="nav-icon">&#127968;</span><span>Overview</span></div>
    <div class="nav-item" onclick="navigate(this,'countries')"><span class="nav-icon">&#127757;</span><span>Country Analysis</span></div>
    <div class="nav-item" onclick="navigate(this,'forecast')"><span class="nav-icon">&#128200;</span><span>Revenue Forecast</span></div>
    <div class="nav-section-label">Market</div>
    <div class="nav-item" onclick="navigate(this,'pricing')"><span class="nav-icon">&#128178;</span><span>Pricing Intel</span></div>
    <div class="nav-item" onclick="navigate(this,'tenders')"><span class="nav-icon">&#128203;</span><span>Tenders</span></div>
    <div class="nav-item" onclick="navigate(this,'competitors')"><span class="nav-icon">&#127942;</span><span>Competitors</span></div>
    <div class="nav-section-label">Field</div>
    <div class="nav-item" onclick="navigate(this,'hotareas')"><span class="nav-icon">&#128205;</span><span>Hot Areas</span></div>
    <div class="nav-item" onclick="navigate(this,'exhibitions')"><span class="nav-icon">&#128197;</span><span>Exhibitions</span></div>
    <div class="nav-item" onclick="navigate(this,'regulatory')"><span class="nav-icon">&#128220;</span><span>Regulatory</span></div>
  </div>

  <div class="main">

    <!-- Overview -->
    <div class="page active" id="page-overview">
      <div class="top-banner">
        <div class="banner-title">&#127760; REGIONAL EXECUTIVE OVERVIEW</div>
        <div class="banner-sub">&#128204; Scope: Middle East &amp; GCC Markets Performance</div>
      </div>
      <div class="section-header">
        <span style="font-size:16px">&#127760;</span>
        <span class="section-title">Gulf Region &#8212; Executive Overview</span>
      </div>
      <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-icon">&#127757;</div><div class="kpi-label">Countries Covered</div><div class="kpi-value">9</div><div class="kpi-sub">Gulf Region</div></div>
        <div class="kpi-card"><div class="kpi-icon">&#128101;</div><div class="kpi-label">Total Population 2026</div><div class="kpi-value accent">127.68M</div><div class="kpi-sub muted">127,681,500</div></div>
        <div class="kpi-card"><div class="kpi-icon">&#129658;</div><div class="kpi-label">Total HD Patients</div><div class="kpi-value">65,254</div><div class="kpi-sub">Hemodialysis</div></div>
        <div class="kpi-card"><div class="kpi-icon">&#128137;</div><div class="kpi-label">Est. 2026 PD</div><div class="kpi-value">4,114</div><div class="kpi-sub">Peritoneal Dialysis</div></div>
        <div class="kpi-card"><div class="kpi-icon">&#127973;</div><div class="kpi-label">Dialysis Facilities</div><div class="kpi-value">762</div><div class="kpi-sub muted">Centers</div></div>
      </div>
      <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-icon">&#9889;</div><div class="kpi-label">HD Machines</div><div class="kpi-value">44,050</div><div class="kpi-sub muted">Units</div></div>
        <div class="kpi-card"><div class="kpi-icon">&#129657;</div><div class="kpi-label">Annual Catheter Demand</div><div class="kpi-value accent">167.87K</div><div class="kpi-sub muted">167,867 units</div></div>
        <div class="kpi-card"><div class="kpi-icon">&#128176;</div><div class="kpi-label">Market Value</div><div class="kpi-value gold">$18.90M</div><div class="kpi-sub amber">USD</div></div>
        <div class="kpi-card"><div class="kpi-icon">&#129309;</div><div class="kpi-label">Distributors</div><div class="kpi-value">90</div><div class="kpi-sub green">Active Partners</div></div>
        <div class="kpi-card"><div class="kpi-icon">&#11088;</div><div class="kpi-label">KOLs</div><div class="kpi-value">90</div><div class="kpi-sub green">Opinion Leaders</div></div>
      </div>
      <div class="divider"></div>
      <div style="text-align:center;padding:8px 16px 16px;font-size:10px;color:#2a4060;">
        Data source: Amecath_Dash.xlsx &nbsp;&middot;&nbsp; 2026 Edition &nbsp;&middot;&nbsp; 9 Markets
      </div>
    </div>

    <!-- Country Analysis -->
    <div class="page" id="page-countries">
      <div class="placeholder-page"><div class="placeholder-icon">&#127757;</div><div class="placeholder-title">Country Analysis</div><div class="placeholder-sub">Coming soon</div></div>
    </div>

    <!-- Revenue Forecast -->
    <div class="page" id="page-forecast">
      <div class="placeholder-page"><div class="placeholder-icon">&#128200;</div><div class="placeholder-title">Revenue Forecast</div><div class="placeholder-sub">Coming soon</div></div>
    </div>

    <!-- Pricing Intel -->
    <div class="page" id="page-pricing">
      <div class="placeholder-page"><div class="placeholder-icon">&#128178;</div><div class="placeholder-title">Pricing Intel</div><div class="placeholder-sub">Coming soon</div></div>
    </div>

    <!-- Tenders -->
    <div class="page" id="page-tenders">
      <div class="placeholder-page"><div class="placeholder-icon">&#128203;</div><div class="placeholder-title">Tenders</div><div class="placeholder-sub">Coming soon</div></div>
    </div>

    <!-- Competitors -->
    <div class="page" id="page-competitors">
      <div class="placeholder-page"><div class="placeholder-icon">&#127942;</div><div class="placeholder-title">Competitors</div><div class="placeholder-sub">Coming soon</div></div>
    </div>

        <!-- Hot Areas -->
    <div class="page" id="page-hotareas">
      <div class="ha-wrap">
        <div class="ha-header">
          <div class="ha-title">&#128205; Hot Areas &#8212; Dialysis Heatmap</div>
          <div style="font-size:11px;color:#3a5278">Click a marker for details</div>
        </div>
        <div class="ha-tabs" id="haTabs"></div>
        <div id="haMap" style="width:100%;height:520px;border-radius:14px;border:1px solid #1e3d7a;overflow:hidden;"></div>
        <div style="margin-top:10px;display:flex;gap:18px;flex-wrap:wrap;">
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;color:#ef4444;">&#11044; Critical</span>
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;color:#f97316;">&#11044; High</span>
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;color:#eab308;">&#11044; Medium</span>
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;color:#22c55e;">&#11044; Low</span>
        </div>
      </div>
    </div>

    <!-- Exhibitions -->
    <div class="page" id="page-exhibitions">
      <div class="placeholder-page"><div class="placeholder-icon">&#128197;</div><div class="placeholder-title">Exhibitions</div><div class="placeholder-sub">Coming soon</div></div>
    </div>

    <!-- Regulatory -->
    <div class="page" id="page-regulatory">
      <div class="placeholder-page"><div class="placeholder-icon">&#128220;</div><div class="placeholder-title">Regulatory</div><div class="placeholder-sub">Coming soon</div></div>
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

  (function() {
    const HA_DATA = {
      "Saudi Arabia": { flag:"SA", areas:[
        {name:"Riyadh",x:.48,y:.52,rank:1,centers:39,hd:5700,priority:"Critical"},
        {name:"Jeddah",x:.30,y:.60,rank:2,centers:12,hd:2100,priority:"High"},
        {name:"Makkah",x:.28,y:.62,rank:3,centers:12,hd:1950,priority:"High"},
        {name:"Dammam/Khobar",x:.70,y:.50,rank:4,centers:6,hd:1200,priority:"High"},
        {name:"Madinah",x:.33,y:.42,rank:5,centers:5,hd:900,priority:"Medium"},
        {name:"Buraydah",x:.46,y:.35,rank:6,centers:7,hd:1020,priority:"Medium"},
        {name:"Hail",x:.44,y:.27,rank:7,centers:6,hd:870,priority:"Medium"},
        {name:"Abha",x:.32,y:.72,rank:8,centers:4,hd:600,priority:"Low"},
        {name:"Tabuk",x:.22,y:.28,rank:9,centers:3,hd:450,priority:"Low"}
      ]},
      "UAE": { flag:"AE", areas:[
        {name:"Dubai",x:.68,y:.55,rank:1,centers:7,hd:840,priority:"Critical"},
        {name:"Abu Dhabi",x:.35,y:.62,rank:2,centers:5,hd:600,priority:"High"},
        {name:"Sharjah",x:.72,y:.45,rank:3,centers:3,hd:360,priority:"Medium"},
        {name:"Al Ain",x:.55,y:.72,rank:4,centers:2,hd:240,priority:"Medium"},
        {name:"Ajman",x:.74,y:.40,rank:5,centers:2,hd:200,priority:"Low"},
        {name:"Fujairah/RAK",x:.85,y:.35,rank:6,centers:2,hd:180,priority:"Low"}
      ]},
      "Qatar": { flag:"QA", areas:[
        {name:"Doha - FBJ",x:.40,y:.60,rank:1,centers:4,hd:720,priority:"Critical"},
        {name:"Al Wakrah",x:.42,y:.70,rank:2,centers:2,hd:240,priority:"Medium"},
        {name:"Al Khor",x:.38,y:.35,rank:3,centers:1,hd:120,priority:"Low"},
        {name:"Al Shahania",x:.35,y:.30,rank:4,centers:1,hd:80,priority:"Low"},
        {name:"Lusail",x:.42,y:.50,rank:5,centers:1,hd:60,priority:"Low"}
      ]},
      "Kuwait": { flag:"KW", areas:[
        {name:"Kuwait City",x:.42,y:.55,rank:1,centers:8,hd:970,priority:"Critical"},
        {name:"Ahmadi",x:.48,y:.68,rank:2,centers:3,hd:390,priority:"High"},
        {name:"Hawalli",x:.45,y:.52,rank:3,centers:3,hd:340,priority:"Medium"},
        {name:"Farwaniya",x:.38,y:.48,rank:4,centers:3,hd:280,priority:"Medium"},
        {name:"Jahra",x:.30,y:.42,rank:5,centers:2,hd:180,priority:"Low"},
        {name:"Sabah Al-Ahmad",x:.52,y:.72,rank:6,centers:1,hd:80,priority:"Low"}
      ]},
      "Iraq": { flag:"IQ", areas:[
        {name:"Baghdad",x:.52,y:.48,rank:1,centers:11,hd:3967,priority:"Critical"},
        {name:"Basra",x:.60,y:.78,rank:2,centers:3,hd:1500,priority:"Critical"},
        {name:"Erbil",x:.65,y:.30,rank:3,centers:4,hd:1200,priority:"High"},
        {name:"Sulaymaniyah",x:.72,y:.32,rank:4,centers:3,hd:900,priority:"High"},
        {name:"Kirkuk",x:.62,y:.40,rank:5,centers:2,hd:463,priority:"Medium"},
        {name:"Mosul",x:.58,y:.28,rank:6,centers:2,hd:420,priority:"Medium"},
        {name:"Najaf",x:.50,y:.60,rank:7,centers:2,hd:380,priority:"Medium"},
        {name:"Diwaniyah",x:.53,y:.65,rank:8,centers:2,hd:300,priority:"Low"}
      ]},
      "Jordan": { flag:"JO", areas:[
        {name:"Amman",x:.48,y:.52,rank:1,centers:5,hd:3200,priority:"Critical"},
        {name:"Irbid",x:.46,y:.38,rank:2,centers:2,hd:960,priority:"High"},
        {name:"Zarqa",x:.52,y:.48,rank:3,centers:2,hd:768,priority:"Medium"},
        {name:"Salt",x:.44,y:.54,rank:4,centers:1,hd:480,priority:"Medium"},
        {name:"Karak",x:.46,y:.66,rank:5,centers:1,hd:320,priority:"Low"}
      ]},
      "Lebanon": { flag:"LB", areas:[
        {name:"Greater Beirut",x:.40,y:.50,rank:1,centers:30,hd:2365,priority:"Critical"},
        {name:"Tripoli",x:.38,y:.35,rank:2,centers:12,hd:850,priority:"High"},
        {name:"Sidon",x:.38,y:.62,rank:3,centers:8,hd:520,priority:"Medium"},
        {name:"Zahle",x:.48,y:.52,rank:4,centers:6,hd:400,priority:"Medium"},
        {name:"Jounieh",x:.42,y:.45,rank:5,centers:4,hd:280,priority:"Low"},
        {name:"Nabatieh",x:.40,y:.68,rank:6,centers:3,hd:200,priority:"Low"}
      ]},
      "Oman": { flag:"OM", areas:[
        {name:"Muscat",x:.62,y:.40,rank:1,centers:4,hd:1000,priority:"Critical"},
        {name:"Salalah",x:.45,y:.80,rank:2,centers:2,hd:500,priority:"High"},
        {name:"Sohar",x:.55,y:.28,rank:3,centers:2,hd:380,priority:"Medium"},
        {name:"Ibri",x:.48,y:.45,rank:4,centers:2,hd:250,priority:"Medium"},
        {name:"Barka/Seeb",x:.60,y:.38,rank:5,centers:1,hd:180,priority:"Low"}
      ]},
      "Bahrain": { flag:"BH", areas:[
        {name:"Manama / Riffa",x:.52,y:.50,rank:1,centers:5,hd:2500,priority:"Critical"},
        {name:"A'Ali",x:.48,y:.56,rank:2,centers:2,hd:900,priority:"High"},
        {name:"Muharraq",x:.58,y:.42,rank:3,centers:2,hd:680,priority:"Medium"},
        {name:"Saar",x:.44,y:.48,rank:4,centers:1,hd:320,priority:"Low"},
        {name:"Riffa (private)",x:.52,y:.60,rank:5,centers:1,hd:150,priority:"Low"}
      ]}
    };

    const PC = {Critical:"#ef4444",High:"#f97316",Medium:"#eab308",Low:"#22c55e"};
    let haActive = "Saudi Arabia";
    let haAnimPhase = 0;
    let haPulseT = 0;

    const haTabs   = document.getElementById("haTabs");
    const haCanvas = document.getElementById("haCanvas");
    const haCtx    = haCanvas.getContext("2d");
    const haTip    = document.getElementById("haTooltip");
    const haArea   = document.getElementById("haMapArea");
    const haLeg    = document.getElementById("haLegendBar");
    const haLCtx   = haLeg.getContext("2d");

    function flameColor(t, a) {
      const r = Math.min(255, Math.round(255*Math.min(t*2,1)));
      const g = Math.min(255, Math.round(255*Math.max(0,t*2-0.5)));
      const b = Math.round(10*(1-t));
      return "rgba("+r+","+g+","+b+","+a+")";
    }

    function haResize() {
  const W = haArea.clientWidth || (window.innerWidth - 220);
  haCanvas.width  = W;
  haCanvas.height = Math.round(W * 0.52);
}

    function haRender() {
      const W = haCanvas.width, H = haCanvas.height;
      const areas = HA_DATA[haActive].areas;
      haCtx.clearRect(0,0,W,H);
      haCtx.fillStyle="#0a1525"; haCtx.fillRect(0,0,W,H);
      haCtx.strokeStyle="rgba(30,61,122,0.3)"; haCtx.lineWidth=0.5;
      for(var x=0;x<W;x+=W/8){haCtx.beginPath();haCtx.moveTo(x,0);haCtx.lineTo(x,H);haCtx.stroke();}
      for(var y=0;y<H;y+=H/6){haCtx.beginPath();haCtx.moveTo(0,y);haCtx.lineTo(W,y);haCtx.stroke();}
      areas.forEach(function(a){
        var cx=a.x*W,cy=a.y*H,intensity=1-(a.rank-1)/areas.length;
        var r=(40+intensity*70)*(W/700);
        var g=haCtx.createRadialGradient(cx,cy,0,cx,cy,r);
        var al=0.18+intensity*0.32;
        g.addColorStop(0,flameColor(intensity,al));
        g.addColorStop(0.5,flameColor(intensity*0.6,al*0.5));
        g.addColorStop(1,"rgba(0,0,0,0)");
        haCtx.beginPath();haCtx.arc(cx,cy,r,0,Math.PI*2);haCtx.fillStyle=g;haCtx.fill();
      });
      areas.forEach(function(a,i){
        var cx=a.x*W,cy=a.y*H,intensity=1-(a.rank-1)/areas.length;
        var appear=Math.min(1,Math.max(0,(haAnimPhase-i*0.12)/0.15));
        if(appear<=0)return;
        var baseR=(5+intensity*9)*(W/700);
        var pc=PC[a.priority];
        var pulse=Math.sin(haPulseT*0.05+i*0.8)*0.5+0.5;
        haCtx.beginPath();haCtx.arc(cx,cy,baseR+3+pulse*5,0,Math.PI*2);
        haCtx.strokeStyle=pc+"55";haCtx.lineWidth=1.5;haCtx.stroke();
        haCtx.beginPath();haCtx.arc(cx,cy,baseR*appear,0,Math.PI*2);
        haCtx.fillStyle=pc;haCtx.fill();
        haCtx.beginPath();haCtx.arc(cx,cy,baseR*appear*0.45,0,Math.PI*2);
        haCtx.fillStyle="rgba(255,255,255,0.7)";haCtx.fill();
        if(appear>=1&&W>400){
          haCtx.font="bold "+Math.round(9*W/700+8)+"px 'Segoe UI',sans-serif";
          haCtx.fillStyle="#e8edf5";haCtx.textAlign="center";
          var lbl=a.rank===1?a.name:(a.name.length>14?a.name.slice(0,13)+"...":a.name);
          haCtx.fillText(lbl,cx,cy-baseR-5);
        }
      });
      var lg=haLCtx.createLinearGradient(0,0,160,0);
      for(var i=0;i<=10;i++)lg.addColorStop(i/10,flameColor(i/10,1));
      haLCtx.clearRect(0,0,160,10);haLCtx.fillStyle=lg;
      haLCtx.roundRect(0,0,160,10,5);haLCtx.fill();
    }

    function haAnimate() {
      haPulseT++;
      if(haAnimPhase<1.5)haAnimPhase+=0.018;
      haRender();
      requestAnimationFrame(haAnimate);
    }

    Object.keys(HA_DATA).forEach(function(c){
      var el=document.createElement("div");
      el.className="ha-tab"+(c===haActive?" active":"");
      el.textContent=c;
      el.onclick=function(){
        haActive=c;
        document.querySelectorAll(".ha-tab").forEach(function(t){t.classList.remove("active");});
        el.classList.add("active");
        haAnimPhase=0;
      };
      haTabs.appendChild(el);
    });

    haCanvas.addEventListener("mousemove",function(e){
      var rect=haCanvas.getBoundingClientRect();
      var mx=(e.clientX-rect.left)*(haCanvas.width/rect.width);
      var my=(e.clientY-rect.top)*(haCanvas.height/rect.height);
      var areas=HA_DATA[haActive].areas, hit=null;
      for(var i=areas.length-1;i>=0;i--){
        var a=areas[i],cx=a.x*haCanvas.width,cy=a.y*haCanvas.height;
        var intensity=1-(a.rank-1)/areas.length;
        var r=(8+intensity*9)*(haCanvas.width/700)+6;
        if(Math.hypot(mx-cx,my-cy)<r){hit=a;break;}
      }
      if(hit){
        document.getElementById("ha-tt-name").textContent=hit.name;
        document.getElementById("ha-tt-rank").textContent="#"+hit.rank+" in "+haActive;
        document.getElementById("ha-tt-centers").textContent=hit.centers+" dialysis centers";
        document.getElementById("ha-tt-hd").textContent=hit.hd.toLocaleString()+" patients (est.)";
        var pe=document.getElementById("ha-tt-priority");
        pe.textContent=hit.priority;pe.style.color=PC[hit.priority];
        var pxX=e.clientX-rect.left,pxY=e.clientY-rect.top;
        var left=pxX+14,top=pxY-60;
        if(left+190>rect.width-10)left=pxX-204;
        if(top<4)top=4;
        haTip.style.left=left+"px";haTip.style.top=top+"px";haTip.style.opacity="1";
        haCanvas.style.cursor="pointer";
      } else {
        haTip.style.opacity="0";haCanvas.style.cursor="crosshair";
      }
    });
    window.addEventListener("resize", function(){ haResize(); haAnimPhase=0; });

const haObserver = new MutationObserver(function() {
  if (haArea.clientWidth > 0) {
    haResize();
    haAnimPhase = 0;
  }
});
haObserver.observe(document.getElementById("page-hotareas"), { attributes: true, attributeFilter: ["class"] });

haResize();
haAnimate();
  })();
</script>
</body>
</html>
"""

components.html(dashboard_html, height=800, scrolling=False)
