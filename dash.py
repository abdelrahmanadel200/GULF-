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
  .leaflet-popup-content-wrapper { background:transparent !important; border:none !important; box-shadow:none !important; padding:0 !important; }
  .leaflet-popup-content { margin:0 !important; }
  .leaflet-popup-tip-container { display:none !important; }
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
          <div class="ha-title">&#128205; Hot Areas &#8212; Dialysis Map</div>
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
    if (pageId === 'hotareas') {
      if (!haInited) { initHaMap(); }
      else { setTimeout(function(){ haMap.invalidateSize(); }, 150); }
    }
  }

  var haInited = false;
  var haMap = null;
  var haMarkers = [];
  var haActive = 'Saudi Arabia';

  var HA_DATA = {
    'Saudi Arabia': { lat:24.0, lng:45.0, zoom:5, areas:[
      {name:'Riyadh',        lat:24.69, lng:46.72, rank:1, centers:39, hd:5700,  priority:'Critical'},
      {name:'Jeddah',        lat:21.49, lng:39.19, rank:2, centers:12, hd:2100,  priority:'High'},
      {name:'Makkah',        lat:21.39, lng:39.86, rank:3, centers:12, hd:1950,  priority:'High'},
      {name:'Dammam/Khobar', lat:26.43, lng:50.10, rank:4, centers:6,  hd:1200,  priority:'High'},
      {name:'Madinah',       lat:24.47, lng:39.61, rank:5, centers:5,  hd:900,   priority:'Medium'},
      {name:'Buraydah',      lat:26.33, lng:43.97, rank:6, centers:7,  hd:1020,  priority:'Medium'},
      {name:'Hail',          lat:27.51, lng:41.69, rank:7, centers:6,  hd:870,   priority:'Medium'},
      {name:'Abha',          lat:18.22, lng:42.51, rank:8, centers:4,  hd:600,   priority:'Low'},
      {name:'Tabuk',         lat:28.38, lng:36.57, rank:9, centers:3,  hd:450,   priority:'Low'}
    ]},
    'UAE': { lat:24.0, lng:54.0, zoom:7, areas:[
      {name:'Dubai',         lat:25.20, lng:55.27, rank:1, centers:7, hd:840,  priority:'Critical'},
      {name:'Abu Dhabi',     lat:24.45, lng:54.37, rank:2, centers:5, hd:600,  priority:'High'},
      {name:'Sharjah',       lat:25.35, lng:55.42, rank:3, centers:3, hd:360,  priority:'Medium'},
      {name:'Al Ain',        lat:24.21, lng:55.76, rank:4, centers:2, hd:240,  priority:'Medium'},
      {name:'Ajman',         lat:25.41, lng:55.44, rank:5, centers:2, hd:200,  priority:'Low'},
      {name:'Fujairah/RAK',  lat:25.12, lng:56.34, rank:6, centers:2, hd:180,  priority:'Low'}
    ]},
    'Qatar': { lat:25.3, lng:51.2, zoom:9, areas:[
      {name:'Doha - FBJ',    lat:25.29, lng:51.53, rank:1, centers:4, hd:720, priority:'Critical'},
      {name:'Al Wakrah',     lat:25.17, lng:51.60, rank:2, centers:2, hd:240, priority:'Medium'},
      {name:'Al Khor',       lat:25.68, lng:51.50, rank:3, centers:1, hd:120, priority:'Low'},
      {name:'Al Shahania',   lat:25.57, lng:51.27, rank:4, centers:1, hd:80,  priority:'Low'},
      {name:'Lusail',        lat:25.43, lng:51.49, rank:5, centers:1, hd:60,  priority:'Low'}
    ]},
    'Kuwait': { lat:29.3, lng:47.7, zoom:9, areas:[
      {name:'Kuwait City',    lat:29.37, lng:47.98, rank:1, centers:8, hd:970, priority:'Critical'},
      {name:'Ahmadi',         lat:29.08, lng:48.08, rank:2, centers:3, hd:390, priority:'High'},
      {name:'Hawalli',        lat:29.33, lng:48.03, rank:3, centers:3, hd:340, priority:'Medium'},
      {name:'Farwaniya',      lat:29.27, lng:47.96, rank:4, centers:3, hd:280, priority:'Medium'},
      {name:'Jahra',          lat:29.33, lng:47.66, rank:5, centers:2, hd:180, priority:'Low'},
      {name:'Sabah Al-Ahmad', lat:28.90, lng:48.18, rank:6, centers:1, hd:80,  priority:'Low'}
    ]},
    'Iraq': { lat:33.0, lng:44.0, zoom:6, areas:[
      {name:'Baghdad',        lat:33.34, lng:44.40, rank:1, centers:11, hd:3967, priority:'Critical'},
      {name:'Basra',          lat:30.51, lng:47.78, rank:2, centers:3,  hd:1500, priority:'Critical'},
      {name:'Erbil',          lat:36.19, lng:44.01, rank:3, centers:4,  hd:1200, priority:'High'},
      {name:'Sulaymaniyah',   lat:35.56, lng:45.43, rank:4, centers:3,  hd:900,  priority:'High'},
      {name:'Kirkuk',         lat:35.47, lng:44.39, rank:5, centers:2,  hd:463,  priority:'Medium'},
      {name:'Mosul',          lat:36.34, lng:43.13, rank:6, centers:2,  hd:420,  priority:'Medium'},
      {name:'Najaf',          lat:31.99, lng:44.33, rank:7, centers:2,  hd:380,  priority:'Medium'},
      {name:'Diwaniyah',      lat:31.99, lng:44.92, rank:8, centers:2,  hd:300,  priority:'Low'}
    ]},
    'Jordan': { lat:31.0, lng:36.5, zoom:7, areas:[
      {name:'Amman', lat:31.95, lng:35.93, rank:1, centers:5, hd:3200, priority:'Critical'},
      {name:'Irbid',  lat:32.55, lng:35.85, rank:2, centers:2, hd:960,  priority:'High'},
      {name:'Zarqa',  lat:32.07, lng:36.09, rank:3, centers:2, hd:768,  priority:'Medium'},
      {name:'Salt',   lat:32.03, lng:35.73, rank:4, centers:1, hd:480,  priority:'Medium'},
      {name:'Karak',  lat:31.18, lng:35.70, rank:5, centers:1, hd:320,  priority:'Low'}
    ]},
    'Lebanon': { lat:33.9, lng:35.9, zoom:8, areas:[
      {name:'Greater Beirut', lat:33.89, lng:35.50, rank:1, centers:30, hd:2365, priority:'Critical'},
      {name:'Tripoli',        lat:34.44, lng:35.85, rank:2, centers:12, hd:850,  priority:'High'},
      {name:'Sidon',          lat:33.56, lng:35.37, rank:3, centers:8,  hd:520,  priority:'Medium'},
      {name:'Zahle',          lat:33.85, lng:35.90, rank:4, centers:6,  hd:400,  priority:'Medium'},
      {name:'Jounieh',        lat:33.98, lng:35.62, rank:5, centers:4,  hd:280,  priority:'Low'},
      {name:'Nabatieh',       lat:33.38, lng:35.48, rank:6, centers:3,  hd:200,  priority:'Low'}
    ]},
    'Oman': { lat:21.0, lng:57.0, zoom:6, areas:[
      {name:'Muscat',    lat:23.61, lng:58.59, rank:1, centers:4, hd:1000, priority:'Critical'},
      {name:'Salalah',   lat:17.02, lng:54.09, rank:2, centers:2, hd:500,  priority:'High'},
      {name:'Sohar',     lat:24.34, lng:56.75, rank:3, centers:2, hd:380,  priority:'Medium'},
      {name:'Ibri',      lat:23.22, lng:56.51, rank:4, centers:2, hd:250,  priority:'Medium'},
      {name:'Barka/Seeb',lat:23.68, lng:57.89, rank:5, centers:1, hd:180,  priority:'Low'}
    ]},
    'Bahrain': { lat:26.0, lng:50.5, zoom:10, areas:[
      {name:'Manama / Riffa',  lat:26.22, lng:50.59, rank:1, centers:5, hd:2500, priority:'Critical'},
      {name:"A'Ali",           lat:26.15, lng:50.53, rank:2, centers:2, hd:900,  priority:'High'},
      {name:'Muharraq',        lat:26.26, lng:50.62, rank:3, centers:2, hd:680,  priority:'Medium'},
      {name:'Saar',            lat:26.21, lng:50.48, rank:4, centers:1, hd:320,  priority:'Low'},
      {name:'Riffa (private)', lat:26.13, lng:50.56, rank:5, centers:1, hd:150,  priority:'Low'}
    ]}
  };

  var PC = {Critical:'#ef4444', High:'#f97316', Medium:'#eab308', Low:'#22c55e'};

  function makeIcon(priority, rank) {
    var color = PC[priority];
    var size = rank === 1 ? 22 : rank <= 3 ? 16 : 12;
    var s = size * 2;
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="'+s+'" height="'+s+'" viewBox="0 0 100 100">'
      + '<circle cx="50" cy="50" r="40" fill="'+color+'" opacity="0.2"/>'
      + '<circle cx="50" cy="50" r="24" fill="'+color+'"/>'
      + '<circle cx="50" cy="50" r="11" fill="white" opacity="0.85"/>'
      + '</svg>';
    return L.divIcon({ html:svg, className:'', iconSize:[s,s], iconAnchor:[size,size], popupAnchor:[0,-size] });
  }

  function loadCountry(c) {
    var d = HA_DATA[c];
    haMarkers.forEach(function(m){ haMap.removeLayer(m); });
    haMarkers = [];
    haMap.flyTo([d.lat, d.lng], d.zoom, {duration:1.2});
    d.areas.forEach(function(a) {
      var m = L.marker([a.lat, a.lng], {icon: makeIcon(a.priority, a.rank)});
      var popup = '<div style="background:#0d2145;border:1px solid #2563eb;border-radius:10px;padding:10px 14px;min-width:170px;font-family:Segoe UI,sans-serif;">'
        + '<div style="font-size:13px;font-weight:700;color:#60a5fa;margin-bottom:6px;">'+a.name+'</div>'
        + '<div style="font-size:11px;color:#6a85b0;margin-top:3px;">Rank <span style="color:#e8edf5;font-weight:600;">#'+a.rank+' in '+c+'</span></div>'
        + '<div style="font-size:11px;color:#6a85b0;margin-top:3px;">Centers <span style="color:#e8edf5;font-weight:600;">'+a.centers+'</span></div>'
        + '<div style="font-size:11px;color:#6a85b0;margin-top:3px;">HD Patients <span style="color:#e8edf5;font-weight:600;">'+a.hd.toLocaleString()+'</span></div>'
        + '<div style="font-size:11px;color:#6a85b0;margin-top:3px;">Priority <span style="font-weight:700;color:'+PC[a.priority]+';">'+a.priority+'</span></div>'
        + '</div>';
      m.bindPopup(popup, {maxWidth:220});
      m.addTo(haMap);
      haMarkers.push(m);
    });
  }

  function initHaMap() {
    haInited = true;
    haMap = L.map('haMap', {zoomControl:true, attributionControl:false});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19}).addTo(haMap);
    loadCountry(haActive);
  }

  // Build tabs
  var haTabs = document.getElementById('haTabs');
  Object.keys(HA_DATA).forEach(function(c) {
    var el = document.createElement('div');
    el.className = 'ha-tab' + (c === haActive ? ' active' : '');
    el.textContent = c;
    el.onclick = function() {
      haActive = c;
      document.querySelectorAll('.ha-tab').forEach(function(t){ t.classList.remove('active'); });
      el.classList.add('active');
      if (haInited) { loadCountry(c); }
    };
    haTabs.appendChild(el);
  });
</script>
</body>
</html>
"""

components.html(dashboard_html, height=800, scrolling=False)
