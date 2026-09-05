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
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #0b1628; height: 100%; }
.dash { background: #0b1628; color: #e8edf5; font-family: 'Segoe UI', system-ui, sans-serif; min-height: 100vh; display: flex; }
.sidebar { width: 200px; min-width: 200px; background: #070f1f; border-right: 1px solid #1e3d7a; display: flex; flex-direction: column; padding: 18px 0; position: sticky; top: 0; height: 100vh; z-index: 10; align-self: flex-start; }
.logo { padding: 0 16px 18px; border-bottom: 1px solid #1e3d7a; margin-bottom: 10px; }
.logo-text { font-size: 15px; font-weight: 700; color: #60a5fa; letter-spacing: 1.5px; }
.logo-sub { font-size: 10px; color: #3a5278; margin-top: 2px; }
.nav-section-label { font-size: 9px; letter-spacing: 1.5px; color: #2a4060; text-transform: uppercase; padding: 14px 16px 6px; font-weight: 700; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 10px 16px; cursor: pointer; font-size: 12px; color: #6a85b0; border-left: 3px solid transparent; transition: all 0.15s; user-select: none; }
.nav-item:hover { background: #0f1f3d; color: #c8d8f0; }
.nav-item.active { background: #0f1f3d; color: #60a5fa; border-left-color: #2563eb; font-weight: 600; }
.nav-icon { font-size: 15px; width: 18px; text-align: center; }
.main { flex: 1; min-height: 100vh; overflow-y: auto; }
.top-banner { background: linear-gradient(135deg, #0d2145 0%, #1a3a6e 50%, #0d2145 100%); border: 1px solid #1e3d7a; border-radius: 14px; padding: 20px 32px; margin: 16px 16px 0; text-align: center; }
.banner-title { font-size: 18px; font-weight: 700; letter-spacing: 2px; color: #e8edf5; display: flex; align-items: center; justify-content: center; gap: 10px; }
.banner-sub { font-size: 11px; color: #f59e0b; margin-top: 5px; display: flex; align-items: center; justify-content: center; gap: 5px; }
.section-header { display: flex; align-items: center; gap: 10px; margin: 18px 16px 12px; }
.section-title { font-size: 15px; font-weight: 600; color: #c8d8f0; }
.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin: 0 16px 10px; }
.kpi-card { background: #0f1f3d; border: 1px solid #1e3d7a; border-radius: 12px; padding: 16px 12px 12px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 5px; transition: border-color 0.2s, transform 0.15s; cursor: default; }
.kpi-card:hover { border-color: #2563eb; transform: translateY(-1px); }
.kpi-icon { font-size: 20px; margin-bottom: 2px; }
.kpi-label { font-size: 9px; letter-spacing: 1px; color: #6a85b0; text-transform: uppercase; font-weight: 600; }
.kpi-value { font-size: 22px; font-weight: 700; color: #e8edf5; line-height: 1.1; }
.kpi-value.accent { color: #60a5fa; }
.kpi-value.gold { color: #f59e0b; }
.kpi-sub { font-size: 10px; color: #3b82f6; font-weight: 500; }
.kpi-sub.muted { color: #6a85b0; }
.kpi-sub.green { color: #34d399; }
.kpi-sub.amber { color: #f59e0b; }
.divider { height: 1px; background: #1e3d7a; margin: 4px 16px 10px; }
.page { display: none; }
.page.active { display: block; }
.placeholder-page { margin: 16px; background: #0f1f3d; border: 1px dashed #1e3d7a; border-radius: 14px; padding: 60px 32px; text-align: center; color: #3a5278; }
.placeholder-icon { font-size: 40px; margin-bottom: 14px; }
.placeholder-title { font-size: 18px; font-weight: 600; color: #6a85b0; margin-bottom: 8px; }
.placeholder-sub { font-size: 13px; color: #3a5278; }
/* Country page */
.country-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 0 16px 16px; }
.c-card { background: #0f1f3d; border: 1px solid #1e3d7a; border-radius: 14px; padding: 0; cursor: pointer; transition: all .18s; display: flex; flex-direction: column; align-items: stretch; position: relative; overflow: hidden; height: 180px; }
.c-card:hover, .c-card:focus { outline: none; transform: translateY(-2px); border-color: var(--cc, #2563eb); box-shadow: 0 0 0 3px var(--cc, #2563eb)55; }
.c-img { width: 100%; height: 140px; object-fit: contain; object-position: center; display: block; border-radius: 0; background: #0a1628; }
.c-name { font-size: 13px; font-weight: 700; color: #e8edf5; text-align: center; padding: 8px 0 10px; flex: 1; display: flex; align-items: center; justify-content: center; }
.c-accent { position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: var(--cc, #2563eb); }
.cd-panel { display: none; margin: 0 16px 16px; background: #0f1f3d; border: 1px solid #1e3d7a; border-radius: 14px; padding: 20px; animation: fadeIn .2s; }
.cd-panel.open { display: block; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.cd-header { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
.cd-flag { font-size: 44px; }
.cd-title { font-size: 18px; font-weight: 700; color: #e8edf5; }
.cd-sub { font-size: 11px; color: #6a85b0; margin-top: 2px; }
.cd-kpi { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 14px; }
.cd-kpi-item { background:#0b1628; border:1px solid #1e3d7a; border-radius:10px; padding:14px 12px; text-align:center; border-top:2px solid #2563eb; }
.cd-kpi-label { font-size:9px; color:#6a85b0; text-transform:uppercase; letter-spacing:1.2px; font-weight:600; }
.cd-kpi-val { font-size:20px; font-weight:800; color:#60a5fa; margin-top:6px; letter-spacing:.5px; }
.cd-close { margin-left: auto; background: #1e3d7a; border: none; color: #c8d8f0; border-radius: 8px; padding: 6px 14px; cursor: pointer; font-size: 12px; }
.cd-close:hover { background: #2563eb; }
/* Hot map */
.hot-map { margin: 0 16px 16px; height: 520px; border: 1px solid #1e3d7a; border-radius: 14px; overflow: hidden; background: #081321; }
#market-map { width: 100%; height: 100%; }
.leaflet-container { background: #081321; font-family: 'Segoe UI', system-ui, sans-serif; }
.map-popup { min-width: 180px; color: #111827; }
.map-popup-title { font-size: 14px; font-weight: 700; margin-bottom: 6px; }
.map-popup-row { font-size: 11px; margin: 3px 0; }
/* Regulatory */
.reg-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 0 16px 16px; }
.reg-table-container { margin: 0 16px 16px; background: #0f1f3d; border: 1px solid #1e3d7a; border-radius: 12px; overflow: hidden; }
.reg-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 12px; }
.reg-table th { background: #070f1f; color: #6a85b0; padding: 12px 16px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #1e3d7a; }
.reg-table td { padding: 12px 16px; color: #e8edf5; border-bottom: 1px solid #14284b; }
.reg-table tr:last-child td { border-bottom: none; }
.reg-table tr:hover { background: #13274c; }
.badge { display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 10px; font-weight: 600; }
.badge-approved { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.badge-pending { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
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
  <div class="nav-item active" onclick="navigate(this,'overview')"><span class="nav-icon">🏠</span><span>Overview</span></div>
  <div class="nav-item" onclick="navigate(this,'countries')"><span class="nav-icon">🌍</span><span>Country Analysis</span></div>
  <div class="nav-item" onclick="navigate(this,'forecast')"><span class="nav-icon">📈</span><span>Revenue Forecast</span></div>
  <div class="nav-section-label">Market</div>
  <div class="nav-item" onclick="navigate(this,'pricing')"><span class="nav-icon">💲</span><span>Pricing Intel</span></div>
  <div class="nav-item" onclick="navigate(this,'tenders')"><span class="nav-icon">📋</span><span>Tenders</span></div>
  <div class="nav-item" onclick="navigate(this,'competitors')"><span class="nav-icon">🏆</span><span>Competitors</span></div>
  <div class="nav-section-label">Field</div>
  <div class="nav-item" onclick="navigate(this,'hotareas')"><span class="nav-icon">📍</span><span>Hot Areas</span></div>
  <div class="nav-item" onclick="navigate(this,'exhibitions')"><span class="nav-icon">📅</span><span>Exhibitions</span></div>
  <div class="nav-item" onclick="navigate(this,'regulatory')"><span class="nav-icon">📜</span><span>Regulatory</span></div>
</div>

<div class="main">

<!-- OVERVIEW -->
<div class="page active" id="page-overview">
  <div class="top-banner">
    <div class="banner-title">🌐 REGIONAL EXECUTIVE OVERVIEW</div>
    <div class="banner-sub">📌 Scope: Middle East &amp; GCC Markets Performance</div>
  </div>
  <div class="section-header"><span style="font-size:16px">🌐</span><span class="section-title">Gulf Region — Executive Overview</span></div>
  <div class="kpi-grid">
    <div class="kpi-card"><div class="kpi-icon">🌍</div><div class="kpi-label">Countries Covered</div><div class="kpi-value">9</div><div class="kpi-sub">Gulf Region</div></div>
    <div class="kpi-card"><div class="kpi-icon">👥</div><div class="kpi-label">Total Population 2026</div><div class="kpi-value accent">127.68M</div><div class="kpi-sub muted">127,681,500</div></div>
    <div class="kpi-card"><div class="kpi-icon">🩺</div><div class="kpi-label">Total HD Patients</div><div class="kpi-value">65,254</div><div class="kpi-sub">Hemodialysis</div></div>
    <div class="kpi-card"><div class="kpi-icon">💉</div><div class="kpi-label">Est. 2026 PD</div><div class="kpi-value">4,114</div><div class="kpi-sub">Peritoneal Dialysis</div></div>
    <div class="kpi-card"><div class="kpi-icon">🏥</div><div class="kpi-label">Dialysis Facilities</div><div class="kpi-value">762</div><div class="kpi-sub muted">Centers</div></div>
  </div>
  <div class="kpi-grid">
    <div class="kpi-card"><div class="kpi-icon">⚡</div><div class="kpi-label">HD Machines</div><div class="kpi-value">44,050</div><div class="kpi-sub muted">Units</div></div>
    <div class="kpi-card"><div class="kpi-icon">🩹</div><div class="kpi-label">Annual Catheter Demand</div><div class="kpi-value accent">167.87K</div><div class="kpi-sub muted">167,867 units</div></div>
    <div class="kpi-card"><div class="kpi-icon">💰</div><div class="kpi-label">Market Value</div><div class="kpi-value gold">$18.90M</div><div class="kpi-sub amber">USD</div></div>
    <div class="kpi-card"><div class="kpi-icon">🤝</div><div class="kpi-label">Distributors</div><div class="kpi-value">90</div><div class="kpi-sub green">Active Partners</div></div>
    <div class="kpi-card"><div class="kpi-icon">⭐</div><div class="kpi-label">KOLs</div><div class="kpi-value">90</div><div class="kpi-sub green">Opinion Leaders</div></div>
  </div>
  <div class="divider"></div>
  <div style="text-align:center;padding:8px 16px 16px;font-size:10px;color:#2a4060;">Data source: Amecath_Dash.xlsx &nbsp;·&nbsp; 2026 Edition &nbsp;·&nbsp; 9 Markets</div>
</div>

<!-- COUNTRIES -->
<div class="page" id="page-countries">
  <div class="section-header"><span style="font-size:16px">🌍</span><span class="section-title">Country Analysis — 9 Markets</span></div>
  <div class="country-grid" role="list">
  <div class="c-card" style="--cc:#10b981" role="listitem" tabindex="0" onclick="openCountry('sa')" onkeydown="if(event.key==='Enter')openCountry('sa')" aria-label="Saudi Arabia">
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/saudi_arabia_flag.jpeg" class="c-img"/>
    <div class="c-name">Saudi Arabia</div><div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#f59e0b" role="listitem" tabindex="0" onclick="openCountry('ae')" onkeydown="if(event.key==='Enter')openCountry('ae')" aria-label="UAE">
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/uae_flag.jpeg" class="c-img"/>
    <div class="c-name">UAE</div><div class="c-accent"></div>
  </div>
<div class="c-card" style="--cc:#3b82f6" role="listitem" tabindex="0" onclick="openCountry('kw')" onkeydown="if(event.key==='Enter')openCountry('kw')" aria-label="Kuwait">
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/kuwait_flag.jpeg" class="c-img" onerror="this.replaceWith(Object.assign(document.createElement('div'),{textContent:'🇰🇼',style:'font-size:60px;padding:20px'}))"/>
    <div class="c-name">Kuwait</div><div class="c-accent"></div>
</div>
  <div class="c-card" style="--cc:#8b5cf6" role="listitem" tabindex="0" onclick="openCountry('qa')" onkeydown="if(event.key==='Enter')openCountry('qa')" aria-label="Qatar">
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/qatar_flag.jpeg" class="c-img"/>
    <div class="c-name">Qatar</div><div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#ef4444" role="listitem" tabindex="0" onclick="openCountry('om')" onkeydown="if(event.key==='Enter')openCountry('om')" aria-label="Oman">
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/oman_flag.jpeg" class="c-img"/>
    <div class="c-name">Oman</div><div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#ec4899" role="listitem" tabindex="0" onclick="openCountry('bh')" onkeydown="if(event.key==='Enter')openCountry('bh')" aria-label="Bahrain">
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/bahraien_flag.jpeg" class="c-img"/>
    <div class="c-name">Bahrain</div><div class="c-accent"></div>
  </div>
 <div class="c-card" style="--cc:#f97316" role="listitem" tabindex="0" onclick="openCountry('iq')" onkeydown="if(event.key==='Enter')openCountry('iq')" aria-label="Iraq">
  <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/iraq_flag.jpeg" class="c-img" onerror="this.style.display='none'"/>
    <div class="c-name">Iraq</div><div class="c-accent"></div>
</div>
  <div class="c-card" style="--cc:#06b6d4" role="listitem" tabindex="0" onclick="openCountry('jo')" onkeydown="if(event.key==='Enter')openCountry('jo')" aria-label="Jordan">
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/jordon_flag.jpeg" class="c-img"/>
    <div class="c-name">Jordan</div><div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#a3e635" role="listitem" tabindex="0" onclick="openCountry('lb')" onkeydown="if(event.key==='Enter')openCountry('lb')" aria-label="Lebanon">
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/lebanon_flag.jpeg" class="c-img"/>
    <div class="c-name">Lebanon</div><div class="c-accent"></div>
  </div>
</div>
  <div class="cd-panel" id="cd-panel" role="region" aria-live="polite">
    <div class="cd-header">
      <div class="cd-flag" id="cd-flag"></div>
      <div><div class="cd-title" id="cd-title"></div><div class="cd-sub" id="cd-sub"></div></div>
      <button class="cd-close" onclick="closeCountry()" aria-label="Close panel">✕ Close</button>
    </div>
    <div class="cd-kpi" id="cd-kpi"></div>
  </div>
</div>

<!-- FORECAST -->
<div class="page" id="page-forecast">
<div style="padding:0 16px 24px;">

  <!-- KPI Cards -->
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:18px;">
    <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #3b82f6;border-radius:12px;padding:16px;text-align:center;">
      <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">Total 3-Year Revenue (Base)</div>
      <div style="font-size:22px;font-weight:700;color:#60a5fa;margin-top:6px;">$964,939</div>
      <div style="font-size:10px;color:#3b82f6;margin-top:4px;">2026 – 2028</div>
    </div>
    <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #f59e0b;border-radius:12px;padding:16px;text-align:center;">
      <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">Best Case 3-Year Revenue</div>
      <div style="font-size:22px;font-weight:700;color:#f59e0b;margin-top:6px;">$1,609,369</div>
      <div style="font-size:10px;color:#f59e0b;margin-top:4px;">Upside Scenario</div>
    </div>
    <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #34d399;border-radius:12px;padding:16px;text-align:center;">
      <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">2028 Target (Base)</div>
      <div style="font-size:22px;font-weight:700;color:#34d399;margin-top:6px;">$467,575</div>
      <div style="font-size:10px;color:#34d399;margin-top:4px;">12,546 Units</div>
    </div>
    <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #a78bfa;border-radius:12px;padding:16px;text-align:center;">
      <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">Revenue CAGR</div>
      <div style="font-size:22px;font-weight:700;color:#a78bfa;margin-top:6px;">61%</div>
      <div style="font-size:10px;color:#a78bfa;margin-top:4px;">Base Case Growth</div>
    </div>
  </div>

  <!-- Scenario Cards -->
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:18px;">

    <!-- Conservative -->
    <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #3b82f6;border-radius:14px;padding:18px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
        <span style="font-size:18px;">🔵</span>
        <div>
          <div style="font-size:13px;font-weight:700;color:#60a5fa;">Conservative</div>
          <div style="font-size:10px;color:#3a5278;">Low adoption / slow ramp</div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;gap:8px;">
        <div style="background:#081321;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;">
          <div><div style="font-size:10px;color:#6a85b0;">2026</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">$120,296</div></div>
          <div style="text-align:right;"><div style="font-size:10px;color:#6a85b0;">Units</div><div style="font-size:13px;color:#60a5fa;">3,357</div></div>
        </div>
        <div style="background:#081321;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;">
          <div><div style="font-size:10px;color:#6a85b0;">2027</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">$253,536</div></div>
          <div style="text-align:right;"><div style="font-size:10px;color:#6a85b0;">Units</div><div style="font-size:13px;color:#60a5fa;">6,938</div></div>
        </div>
        <div style="background:#081321;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;">
          <div><div style="font-size:10px;color:#6a85b0;">2028</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">$400,779</div></div>
          <div style="text-align:right;"><div style="font-size:10px;color:#6a85b0;">Units</div><div style="font-size:13px;color:#60a5fa;">10,754</div></div>
        </div>
        <div style="background:#0b1a35;border-radius:10px;padding:10px;text-align:center;border:1px dashed #1e3d7a;margin-top:2px;">
          <div style="font-size:9px;color:#6a85b0;text-transform:uppercase;letter-spacing:1px;">3-Year Total</div>
          <div style="font-size:18px;font-weight:800;color:#3b82f6;margin-top:2px;">$774,611</div>
        </div>
      </div>
    </div>

    <!-- Base Case -->
    <div style="background:#0f2f1f;border:1px solid #1e5a3a;border-top:3px solid #34d399;border-radius:14px;padding:18px;box-shadow:0 0 20px rgba(52,211,153,0.08);">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
        <span style="font-size:18px;">🟢</span>
        <div>
          <div style="font-size:13px;font-weight:700;color:#34d399;">Base Case</div>
          <div style="font-size:10px;color:#2a6a4a;">Primary target scenario</div>
        </div>
        <span style="margin-left:auto;background:rgba(52,211,153,0.15);color:#34d399;border:1px solid rgba(52,211,153,0.3);font-size:9px;font-weight:700;padding:2px 8px;border-radius:6px;">TARGET</span>
      </div>
      <div style="display:flex;flex-direction:column;gap:8px;">
        <div style="background:#081321;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;">
          <div><div style="font-size:10px;color:#6a85b0;">2026</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">$180,444</div></div>
          <div style="text-align:right;"><div style="font-size:10px;color:#6a85b0;">Units</div><div style="font-size:13px;color:#34d399;">5,036</div></div>
        </div>
        <div style="background:#081321;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;">
          <div><div style="font-size:10px;color:#6a85b0;">2027</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">$316,920</div></div>
          <div style="text-align:right;"><div style="font-size:10px;color:#6a85b0;">Units</div><div style="font-size:13px;color:#34d399;">8,673</div></div>
        </div>
        <div style="background:#081321;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;">
          <div><div style="font-size:10px;color:#6a85b0;">2028</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">$467,575</div></div>
          <div style="text-align:right;"><div style="font-size:10px;color:#6a85b0;">Units</div><div style="font-size:13px;color:#34d399;">12,546</div></div>
        </div>
        <div style="background:#061a10;border-radius:10px;padding:10px;text-align:center;border:1px dashed #1e5a3a;margin-top:2px;">
          <div style="font-size:9px;color:#6a85b0;text-transform:uppercase;letter-spacing:1px;">3-Year Total</div>
          <div style="font-size:18px;font-weight:800;color:#34d399;margin-top:2px;">$964,939</div>
        </div>
      </div>
    </div>

    <!-- Upside -->
    <div style="background:#1f1800;border:1px solid #5a3e00;border-top:3px solid #f59e0b;border-radius:14px;padding:18px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
        <span style="font-size:18px;">🟡</span>
        <div>
          <div style="font-size:13px;font-weight:700;color:#f59e0b;">Upside</div>
          <div style="font-size:10px;color:#6a4a00;">Aggressive expansion</div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;gap:8px;">
        <div style="background:#081321;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;">
          <div><div style="font-size:10px;color:#6a85b0;">2026</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">$300,739</div></div>
          <div style="text-align:right;"><div style="font-size:10px;color:#6a85b0;">Units</div><div style="font-size:13px;color:#f59e0b;">8,393</div></div>
        </div>
        <div style="background:#081321;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;">
          <div><div style="font-size:10px;color:#6a85b0;">2027</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">$507,072</div></div>
          <div style="text-align:right;"><div style="font-size:10px;color:#6a85b0;">Units</div><div style="font-size:13px;color:#f59e0b;">13,876</div></div>
        </div>
        <div style="background:#081321;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;">
          <div><div style="font-size:10px;color:#6a85b0;">2028</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">$801,557</div></div>
          <div style="text-align:right;"><div style="font-size:10px;color:#6a85b0;">Units</div><div style="font-size:13px;color:#f59e0b;">21,507</div></div>
        </div>
        <div style="background:#100e00;border-radius:10px;padding:10px;text-align:center;border:1px dashed #5a3e00;margin-top:2px;">
          <div style="font-size:9px;color:#6a85b0;text-transform:uppercase;letter-spacing:1px;">3-Year Total</div>
          <div style="font-size:18px;font-weight:800;color:#f59e0b;margin-top:2px;">$1,609,369</div>
        </div>
      </div>
    </div>
  </div>

  <!-- SVG Bar Chart -->
  <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;padding:20px;margin-bottom:18px;">
    <div style="font-size:13px;font-weight:600;color:#c8d8f0;margin-bottom:4px;">📊 Scenario Comparison by Year</div>
    <div style="font-size:10px;color:#3a5278;margin-bottom:16px;">Revenue in USD — Grouped by year</div>
    <svg viewBox="0 0 760 260" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;">
      <!-- Grid lines -->
      <line x1="60" y1="20" x2="60" y2="210" stroke="#1e3d7a" stroke-width="1"/>
      <line x1="60" y1="210" x2="740" y2="210" stroke="#1e3d7a" stroke-width="1"/>
      <line x1="60" y1="160" x2="740" y2="160" stroke="#1e3d7a" stroke-width="0.5" stroke-dasharray="4,4"/>
      <line x1="60" y1="110" x2="740" y2="110" stroke="#1e3d7a" stroke-width="0.5" stroke-dasharray="4,4"/>
      <line x1="60" y1="60"  x2="740" y2="60"  stroke="#1e3d7a" stroke-width="0.5" stroke-dasharray="4,4"/>
      <!-- Y labels -->
      <text x="55" y="214" fill="#6a85b0" font-size="9" text-anchor="end">$0</text>
      <text x="55" y="164" fill="#6a85b0" font-size="9" text-anchor="end">$200K</text>
      <text x="55" y="114" fill="#6a85b0" font-size="9" text-anchor="end">$400K</text>
      <text x="55" y="64"  fill="#6a85b0" font-size="9" text-anchor="end">$600K</text>
      <!-- X labels -->
      <text x="200" y="230" fill="#c8d8f0" font-size="11" text-anchor="middle" font-weight="600">2026</text>
      <text x="420" y="230" fill="#c8d8f0" font-size="11" text-anchor="middle" font-weight="600">2027</text>
      <text x="640" y="230" fill="#c8d8f0" font-size="11" text-anchor="middle" font-weight="600">2028</text>

      <!-- Scale: max ~$802K → 190px usable height (210→20). $802K=190px → 1px=$4221 -->
      <!-- 2026: Conservative=120296→28.5px, Base=180444→42.7px, Upside=300739→71.2px -->
      <!-- 2027: Conservative=253536→60px,  Base=316920→75px,   Upside=507072→120px  -->
      <!-- 2028: Conservative=400779→94.9px, Base=467575→110.7px, Upside=801557→189.9px -->

      <!-- 2026 bars -->
      <rect x="130" y="181.5" width="42" height="28.5"  fill="#3b82f6" rx="3"/>
      <rect x="178" y="167.3" width="42" height="42.7"  fill="#34d399" rx="3"/>
      <rect x="226" y="138.8" width="42" height="71.2"  fill="#f59e0b" rx="3"/>
      <!-- value labels 2026 -->
      <text x="151" y="178" fill="#60a5fa" font-size="8" text-anchor="middle">$120K</text>
      <text x="199" y="163" fill="#34d399" font-size="8" text-anchor="middle">$180K</text>
      <text x="247" y="135" fill="#f59e0b" font-size="8" text-anchor="middle">$301K</text>

      <!-- 2027 bars -->
      <rect x="348" y="150" width="42" height="60"   fill="#3b82f6" rx="3"/>
      <rect x="396" y="135" width="42" height="75"   fill="#34d399" rx="3"/>
      <rect x="444" y="90"  width="42" height="120"  fill="#f59e0b" rx="3"/>
      <!-- value labels 2027 -->
      <text x="369" y="146" fill="#60a5fa" font-size="8" text-anchor="middle">$254K</text>
      <text x="417" y="131" fill="#34d399" font-size="8" text-anchor="middle">$317K</text>
      <text x="465" y="86"  fill="#f59e0b" font-size="8" text-anchor="middle">$507K</text>

      <!-- 2028 bars -->
      <rect x="568" y="115.1" width="42" height="94.9"  fill="#3b82f6" rx="3"/>
      <rect x="616" y="99.3"  width="42" height="110.7" fill="#34d399" rx="3"/>
      <rect x="664" y="20.1"  width="42" height="189.9" fill="#f59e0b" rx="3"/>
      <!-- value labels 2028 -->
      <text x="589" y="111" fill="#60a5fa" font-size="8" text-anchor="middle">$401K</text>
      <text x="637" y="95"  fill="#34d399" font-size="8" text-anchor="middle">$468K</text>
      <text x="685" y="16"  fill="#f59e0b" font-size="8" text-anchor="middle">$802K</text>
    </svg>
    <!-- Legend -->
    <div style="display:flex;gap:20px;justify-content:center;margin-top:10px;">
      <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#c8d8f0;"><span style="display:inline-block;width:12px;height:12px;background:#3b82f6;border-radius:3px;"></span>Conservative</div>
      <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#c8d8f0;"><span style="display:inline-block;width:12px;height:12px;background:#34d399;border-radius:3px;"></span>Base Case</div>
      <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#c8d8f0;"><span style="display:inline-block;width:12px;height:12px;background:#f59e0b;border-radius:3px;"></span>Upside</div>
    </div>
  </div>

  <!-- Bottom-Up Country Table -->
  <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;overflow:hidden;">
    <div style="padding:16px 20px;border-bottom:1px solid #1e3d7a;display:flex;align-items:center;gap:10px;">
      <span style="font-size:15px;">🌍</span>
      <div>
        <div style="font-size:13px;font-weight:600;color:#c8d8f0;">Bottom-Up Revenue Forecast by Country</div>
        <div style="font-size:10px;color:#3a5278;margin-top:2px;">Base Case — USD · Share of 3-Year Total ($964,939)</div>
      </div>
    </div>
    <table style="width:100%;border-collapse:collapse;font-size:12px;">
      <thead>
        <tr style="background:#070f1f;">
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Country</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:right;font-weight:600;">2026</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:right;font-weight:600;">2027</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:right;font-weight:600;">2028</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:right;font-weight:600;">3-Year Total</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;min-width:140px;">Share</th>
        </tr>
      </thead>
      <tbody id="country-forecast-body">
      </tbody>
    </table>
  </div>

</div>

<script>
(function(){
  const rows=[
    {flag:'🇸🇦',name:'Saudi Arabia', v26:85361,  v27:149466, v28:219841},
    {flag:'🇮🇶',name:'Iraq',         v26:26801,  v27:47612,  v28:71049},
    {flag:'🇯🇴',name:'Jordan',       v26:16788,  v27:29395,  v28:43236},
    {flag:'🇱🇧',name:'Lebanon',      v26:12380,  v27:21573,  v28:31576},
    {flag:'🇧🇭',name:'Bahrain',      v26:13085,  v27:23024,  v28:34029},
    {flag:'🇴🇲',name:'Oman',         v26:6903,   v27:12146,  v28:17951},
    {flag:'🇦🇪',name:'UAE',          v26:8914,   v27:15759,  v28:23404},
    {flag:'🇰🇼',name:'Kuwait',       v26:6470,   v27:11329,  v28:16663},
    {flag:'🇶🇦',name:'Qatar',        v26:3743,   v27:6617,   v28:9827},
  ];
  const grandTotal=964939;
  const fmt=n=>'$'+n.toLocaleString();
  const pct=(n,t)=>((n/t)*100).toFixed(1)+'%';
  const barColors=['#f59e0b','#60a5fa','#34d399','#a78bfa','#f97316','#06b6d4','#ec4899','#84cc16','#e879f9'];
  const tbody=document.getElementById('country-forecast-body');
  rows.forEach((r,i)=>{
    const total3=r.v26+r.v27+r.v28;
    const share=(total3/grandTotal)*100;
    const barW=Math.round(share*1.8);
    const color=barColors[i%barColors.length];
    const tr=document.createElement('tr');
    tr.style.cssText='border-bottom:1px solid #14284b;transition:background .15s;';
    tr.onmouseenter=()=>tr.style.background='#13274c';
    tr.onmouseleave=()=>tr.style.background='';
    tr.innerHTML=`
      <td style="padding:12px 16px;color:#e8edf5;font-weight:600;">${r.flag} ${r.name}</td>
      <td style="padding:12px 16px;color:#c8d8f0;text-align:right;">${fmt(r.v26)}</td>
      <td style="padding:12px 16px;color:#c8d8f0;text-align:right;">${fmt(r.v27)}</td>
      <td style="padding:12px 16px;color:#c8d8f0;text-align:right;">${fmt(r.v28)}</td>
      <td style="padding:12px 16px;color:${color};font-weight:700;text-align:right;">${fmt(total3)}</td>
      <td style="padding:12px 16px;">
        <div style="display:flex;align-items:center;gap:8px;">
          <div style="flex:1;background:#0b1628;border-radius:4px;height:6px;overflow:hidden;">
            <div style="width:${barW}%;height:100%;background:${color};border-radius:4px;transition:width .4s;"></div>
          </div>
          <span style="font-size:10px;color:${color};font-weight:600;min-width:36px;">${share.toFixed(1)}%</span>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
  // Total row
  const totalTr=document.createElement('tr');
  totalTr.style.cssText='background:#070f1f;border-top:2px solid #1e3d7a;';
  const t26=rows.reduce((s,r)=>s+r.v26,0);
  const t27=rows.reduce((s,r)=>s+r.v27,0);
  const t28=rows.reduce((s,r)=>s+r.v28,0);
  totalTr.innerHTML=`
    <td style="padding:12px 16px;color:#60a5fa;font-weight:700;font-size:12px;">🌐 Total</td>
    <td style="padding:12px 16px;color:#60a5fa;font-weight:700;text-align:right;">$${t26.toLocaleString()}</td>
    <td style="padding:12px 16px;color:#60a5fa;font-weight:700;text-align:right;">$${t27.toLocaleString()}</td>
    <td style="padding:12px 16px;color:#60a5fa;font-weight:700;text-align:right;">$${t28.toLocaleString()}</td>
    <td style="padding:12px 16px;color:#f59e0b;font-weight:800;text-align:right;font-size:14px;">$964,939</td>
    <td style="padding:12px 16px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="flex:1;background:#0b1628;border-radius:4px;height:6px;overflow:hidden;">
          <div style="width:100%;height:100%;background:linear-gradient(90deg,#3b82f6,#34d399,#f59e0b);border-radius:4px;"></div>
        </div>
        <span style="font-size:10px;color:#f59e0b;font-weight:700;">100%</span>
      </div>
    </td>
  `;
  tbody.appendChild(totalTr);
})();
</script>

</div>

<!-- PRICING -->
<div class="page" id="page-pricing">
  <div class="placeholder-page"><div class="placeholder-icon">💲</div><div class="placeholder-title">Pricing Intel</div><div class="placeholder-sub">Coming soon</div></div>
</div>

<!-- TENDERS -->
<div class="page" id="page-tenders">
  <div class="placeholder-page"><div class="placeholder-icon">📋</div><div class="placeholder-title">Tenders</div><div class="placeholder-sub">Coming soon</div></div>
</div>

<!-- COMPETITORS -->
<div class="page" id="page-competitors">
  <div class="p-4 space-y-6">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0f1f3d] p-5 rounded-2xl border border-[#1e3d7a]">
      <div>
        <h2 class="text-xl font-bold text-white flex items-center gap-2"><span>🏆</span> HD Catheters Global &amp; Regional Competitor Analysis</h2>
        <p class="text-slate-400 text-xs mt-1">Market share tracking, strengths, weaknesses, and AMECATH's strategic edge</p>
      </div>
      <div class="flex flex-wrap gap-2">
        <button onclick="filterCompetitors('all',this)" class="comp-filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-600 text-white">All (10)</button>
        <button onclick="filterCompetitors('high',this)" class="comp-filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#1a2d4d] text-slate-300">High Threat 🔴</button>
        <button onclick="filterCompetitors('medium',this)" class="comp-filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#1a2d4d] text-slate-300">Medium Threat 🟡</button>
      </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="comp-grid">

      <div class="comp-card high group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-red-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">Fresenius Medical Care</h3><span class="text-xs text-slate-400">Germany — Full Dialysis Ecosystem</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400 border border-red-500/30">High Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~18–20%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-blue-500 h-full rounded-full" style="width:20%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">Bundling catheters with machines</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">Lower standalone catheter focus</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Flexible customization + faster local supply</span></div>
      </div>

      <div class="comp-card high group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-red-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">Teleflex (Arrow)</h3><span class="text-xs text-slate-400">USA — Vascular Access Brand Equity</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400 border border-red-500/30">High Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~14–16%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-blue-500 h-full rounded-full" style="width:16%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">Arrowg+ard antimicrobial tech</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">Premium pricing structure</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Competitive pricing with equivalent flow</span></div>
      </div>

      <div class="comp-card high group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-red-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">B. Braun Melsungen</h3><span class="text-xs text-slate-400">Germany — Broad Pricing Power</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400 border border-red-500/30">High Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~12–14%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-blue-500 h-full rounded-full" style="width:14%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">Established institutional distribution</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">Standard design, slow iteration</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Specialized focus + regional agility</span></div>
      </div>

      <div class="comp-card medium group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-amber-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">Medtronic (Mahurkar)</h3><span class="text-xs text-slate-400">USA — Legacy Clinical Reputation</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">Medium Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~10–12%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-amber-500 h-full rounded-full" style="width:12%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">Mahurkar curved lumen benchmark</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">High acquisition cost</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Cost-effective with identical lumen specs</span></div>
      </div>

      <div class="comp-card medium group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-amber-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">MedComp</h3><span class="text-xs text-slate-400">USA — Vascular Access Specialist</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">Medium Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~8–10%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-amber-500 h-full rounded-full" style="width:10%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">Extensive HD portfolio</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">Reliance on third-party distributors</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Direct ME manufacturing</span></div>
      </div>

      <div class="comp-card medium group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-amber-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">BD (Bard / Pristine)</h3><span class="text-xs text-slate-400">USA — Global Sales Footprint</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">Medium Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~8–10%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-amber-500 h-full rounded-full" style="width:10%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">Pristine/Symmetrex tip designs</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">High tender price pressures</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Superior price-to-performance</span></div>
      </div>

      <div class="comp-card medium group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-amber-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">Merit Medical</h3><span class="text-xs text-slate-400">USA — Interventional Specialist</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">Medium Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~5–7%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-amber-500 h-full rounded-full" style="width:7%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">Interventional accessories bundle</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">Smaller chronic dialysis presence</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Acute and chronic HD focus</span></div>
      </div>

      <div class="comp-card medium group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-amber-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">Nipro Corporation</h3><span class="text-xs text-slate-400">Japan — Quality Engineering</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">Medium Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~5–7%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-amber-500 h-full rounded-full" style="width:7%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">Dialyzer and bloodline integration</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">Slow delivery from East Asia</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Regional inventory and rapid restocking</span></div>
      </div>

      <div class="comp-card medium group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-amber-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">AngioDynamics (BioFlo)</h3><span class="text-xs text-slate-400">USA — Advanced Material Science</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">Medium Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~4–6%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-amber-500 h-full rounded-full" style="width:6%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">Thrombus-resistant polymer</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">Limited tender participation</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Flexible options at budget tiers</span></div>
      </div>

      <div class="comp-card medium group bg-[#0f1f3d] border border-[#1e3d7a] hover:border-blue-500 rounded-xl p-4 relative overflow-hidden transition-all duration-300">
        <div class="absolute top-0 right-0 w-1.5 h-full bg-amber-500"></div>
        <div class="flex justify-between items-start mb-3"><div><h3 class="font-bold text-base text-white group-hover:text-blue-400">Cook Medical</h3><span class="text-xs text-slate-400">USA — Interventional Pioneer</span></div><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">Medium Threat</span></div>
        <div class="flex justify-between mb-1 text-slate-300 text-xs"><span>Market Share (GCC):</span><span class="text-blue-400 font-bold">~3–5%</span></div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mb-2"><div class="bg-amber-500 h-full rounded-full" style="width:5%"></div></div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Strength:</span><span class="text-slate-200">High quality introducer kits</span></div>
          <div class="bg-[#081321] p-2 rounded border border-[#1e3d7a]"><span class="text-slate-400 block">Weakness:</span><span class="text-slate-200">Slow dialysis space expansion</span></div>
        </div>
        <div class="pt-2 mt-2 border-t border-[#1e3d7a] text-xs"><span class="text-emerald-400 font-semibold">AMECATH: Comprehensive kit variations</span></div>
      </div>

    </div>
  </div>
</div>

<!-- HOT AREAS -->
<div class="page" id="page-hotareas">
  <div class="section-header"><span style="font-size:16px">📍</span><span class="section-title">Hot Areas — Dialysis Market</span></div>
  <div class="hot-map"><div id="market-map"></div></div>
</div>

<!-- EXHIBITIONS -->
<div class="page" id="page-exhibitions">
  <div style="padding:0 16px 24px;">

    <!-- KPI Cards -->
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:18px;">
      <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #60a5fa;border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">Total Events</div>
        <div style="font-size:28px;font-weight:700;color:#60a5fa;margin-top:6px;">12</div>
        <div style="font-size:10px;color:#3b82f6;margin-top:4px;">2027 – 2028</div>
      </div>
      <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #34d399;border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">2027 Events</div>
        <div style="font-size:28px;font-weight:700;color:#34d399;margin-top:6px;">10</div>
        <div style="font-size:10px;color:#34d399;margin-top:4px;">This cycle</div>
      </div>
      <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #a78bfa;border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">2028 Events</div>
        <div style="font-size:28px;font-weight:700;color:#a78bfa;margin-top:6px;">2</div>
        <div style="font-size:10px;color:#a78bfa;margin-top:4px;">Next cycle</div>
      </div>
      <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #ef4444;border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">Critical Priority 🔴</div>
        <div style="font-size:28px;font-weight:700;color:#ef4444;margin-top:6px;">6</div>
        <div style="font-size:10px;color:#ef4444;margin-top:4px;">Must attend</div>
      </div>
    </div>

    <!-- Filter Buttons -->
    <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;">
      <button onclick="filterExhibitions('all',this)" id="exh-btn-all"
        style="padding:7px 16px;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;border:1px solid #2563eb;background:#2563eb;color:#fff;">
        All (12)
      </button>
      <button onclick="filterExhibitions('2027',this)" id="exh-btn-2027"
        style="padding:7px 16px;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;border:1px solid #1e3d7a;background:#0f1f3d;color:#6a85b0;">
        2027 (10)
      </button>
      <button onclick="filterExhibitions('2028',this)" id="exh-btn-2028"
        style="padding:7px 16px;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;border:1px solid #1e3d7a;background:#0f1f3d;color:#6a85b0;">
        2028 (2)
      </button>
      <button onclick="filterExhibitions('critical',this)" id="exh-btn-critical"
        style="padding:7px 16px;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;border:1px solid #1e3d7a;background:#0f1f3d;color:#6a85b0;">
        🔴 Critical Only
      </button>
    </div>

    <!-- Timeline Grid -->
    <div id="exh-grid" style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">
    </div>
  </div>

  <script>
  (function(){
    const exhibitions = [
      {year:'2027',month:'01',date:'25–28 Jan 2027',name:'Arab Health (World Health Expo Dubai)',location:'Dubai, UAE',flag:'🇦🇪',focus:'General Healthcare + Dialysis',priority:'critical',icon:'🔴'},
      {year:'2027',month:'01',date:'Jan 2027',name:'SIRS 2027 — Saudi IR Society',location:'Riyadh, KSA',flag:'🇸🇦',focus:'IR + Dialysis Access',priority:'critical',icon:'🔴'},
      {year:'2027',month:'02',date:'Feb 2027',name:'Gulf Aorta Summit (GAS)',location:'Dubai, UAE',flag:'🇦🇪',focus:'Vascular + Endovascular',priority:'high',icon:'🟠'},
      {year:'2027',month:'03',date:'29–30 Mar 2027',name:'Urology & Nephrology Conference',location:'Dubai, UAE',flag:'🇦🇪',focus:'Nephrology + Dialysis',priority:'high',icon:'🟠'},
      {year:'2027',month:'04',date:'1–4 Apr 2027',name:'World Congress of Nephrology (WCN)',location:'Kuala Lumpur, Malaysia',flag:'🇲🇾',focus:'Global Nephrology',priority:'high',icon:'🟠'},
      {year:'2027',month:'04',date:'Apr–May 2027',name:'PAIRS 2027 — Pan Arab IR Society',location:'Dubai, UAE',flag:'🇦🇪',focus:'IR + Vascular Access + Dialysis',priority:'critical',icon:'🔴'},
      {year:'2027',month:'09',date:'2027 TBA',name:'TCT Plus Middle East',location:'Dubai, UAE',flag:'🇦🇪',focus:'Cardiovascular + Vascular Access',priority:'high',icon:'🟠'},
      {year:'2027',month:'10',date:'26–29 Oct 2027',name:'Global Health Exhibition (GHE)',location:'Riyadh, KSA',flag:'🇸🇦',focus:'Medical Devices + MOH / NUPCO',priority:'critical',icon:'🔴'},
      {year:'2027',month:'12',date:'Dec 2027',name:'Qatar Nephrology Conference (QNC)',location:'Doha, Qatar',flag:'🇶🇦',focus:'Nephrology + Dialysis',priority:'critical',icon:'🔴'},
      {year:'2027',month:'12',date:'Dec 2027',name:'PAVSS Annual Meeting',location:'Rotating',flag:'🌍',focus:'Vascular Surgery + HD Access',priority:'high',icon:'🟠'},
      {year:'2028',month:'01',date:'Jan 2028',name:'Arab Health 2028',location:'Dubai, UAE',flag:'🇦🇪',focus:'Medical Devices',priority:'critical',icon:'🔴'},
      {year:'2028',month:'04',date:'27–30 Apr 2028',name:'World Congress of Nephrology (WCN) 2028',location:'Montreal, Canada',flag:'🇨🇦',focus:'Global Nephrology',priority:'medium',icon:'🟡'},
    ];

    const priorityStyles = {
      critical:{bg:'rgba(239,68,68,0.12)',border:'rgba(239,68,68,0.4)',dot:'#ef4444',label:'Critical'},
      high:    {bg:'rgba(249,115,22,0.12)',border:'rgba(249,115,22,0.4)',dot:'#f97316',label:'High'},
      medium:  {bg:'rgba(234,179,8,0.12)', border:'rgba(234,179,8,0.4)', dot:'#eab308',label:'Medium'},
    };

    function renderGrid(filter){
      const grid = document.getElementById('exh-grid');
      grid.innerHTML = '';
      const filtered = exhibitions.filter(e => {
        if(filter==='all') return true;
        if(filter==='2027') return e.year==='2027';
        if(filter==='2028') return e.year==='2028';
        if(filter==='critical') return e.priority==='critical';
        return true;
      });
      filtered.forEach(e => {
        const ps = priorityStyles[e.priority] || priorityStyles.medium;
        const card = document.createElement('div');
        card.className = 'exh-card';
        card.dataset.year = e.year;
        card.dataset.priority = e.priority;
        card.style.cssText = `
          background:#0f1f3d;border:1px solid #1e3d7a;border-left:4px solid ${ps.dot};
          border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;gap:8px;
          transition:border-color .15s,transform .15s;cursor:default;
        `;
        card.onmouseenter = () => { card.style.borderColor = ps.dot; card.style.transform = 'translateY(-2px)'; };
        card.onmouseleave = () => { card.style.borderColor = '#1e3d7a'; card.style.borderLeftColor = ps.dot; card.style.transform = ''; };
        card.innerHTML = `
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;">
            <div style="font-size:13px;font-weight:700;color:#e8edf5;line-height:1.35;flex:1;">${e.name}</div>
            <span style="flex-shrink:0;padding:3px 9px;border-radius:6px;font-size:10px;font-weight:700;
              background:${ps.bg};color:${ps.dot};border:1px solid ${ps.border};">
              ${e.icon} ${ps.label}
            </span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#60a5fa;font-weight:600;">
            <span>📅</span><span>${e.date}</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#a0b4cc;">
            <span>${e.flag}</span><span>${e.location}</span>
          </div>
          <div style="margin-top:2px;background:#081321;border-radius:7px;padding:7px 10px;font-size:11px;color:#6a85b0;">
            <span style="color:#3b82f6;font-weight:600;">Focus: </span>${e.focus}
          </div>
        `;
        grid.appendChild(card);
      });
      if(filtered.length === 0){
        grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:#3a5278;">No events match this filter.</div>';
      }
    }

    window.filterExhibitions = function(filter, btn){
      ['all','2027','2028','critical'].forEach(f => {
        const b = document.getElementById('exh-btn-'+f);
        if(b){ b.style.background='#0f1f3d'; b.style.color='#6a85b0'; b.style.borderColor='#1e3d7a'; }
      });
      btn.style.background='#2563eb'; btn.style.color='#fff'; btn.style.borderColor='#2563eb';
      renderGrid(filter);
    };

    renderGrid('all');
  })();
  </script>
</div>

<!-- REGULATORY -->
<div class="page" id="page-regulatory">
  <div class="section-header"><span style="font-size:16px">📜</span><span class="section-title">Regulatory &amp; Registration Overview</span></div>
  <div class="reg-grid">
    <div class="kpi-card"><div class="kpi-icon">✅</div><div class="kpi-label">Active Registrations</div><div class="kpi-value" style="color:#34d399">7</div><div class="kpi-sub green">GCC &amp; ME Markets</div></div>
    <div class="kpi-card"><div class="kpi-icon">⏳</div><div class="kpi-label">Pending / Renewal</div><div class="kpi-value gold">2</div><div class="kpi-sub amber">In Progress</div></div>
    <div class="kpi-card"><div class="kpi-icon">🛡️</div><div class="kpi-label">Core Compliance</div><div class="kpi-value accent">CE / ISO</div><div class="kpi-sub muted">ISO 13485 Certified</div></div>
    <div class="kpi-card"><div class="kpi-icon">📄</div><div class="kpi-label">Key Requirement</div><div class="kpi-value">FSC</div><div class="kpi-sub muted">Free Sale Certificate</div></div>
  </div>
  <div class="reg-table-container">
    <table class="reg-table">
      <thead><tr><th>Country / Market</th><th>Health Authority</th><th>Registration Status</th><th>Key Requirements</th></tr></thead>
      <tbody>
        <tr><td><b>🇸🇦 Saudi Arabia</b></td><td>SFDA</td><td><span class="badge badge-approved">Approved</span></td><td>MDNR &amp; CE Mark</td></tr>
        <tr><td><b>🇦🇪 UAE</b></td><td>MOHAP</td><td><span class="badge badge-approved">Approved</span></td><td>Classification &amp; FSC</td></tr>
        <tr><td><b>🇰🇼 Kuwait</b></td><td>MOH Kuwait</td><td><span class="badge badge-approved">Approved</span></td><td>Local Agent + ISO 13485</td></tr>
        <tr><td><b>🇶🇦 Qatar</b></td><td>MOPH Qatar</td><td><span class="badge badge-approved">Approved</span></td><td>MOPH Registration &amp; Dossier</td></tr>
        <tr><td><b>🇴🇲 Oman</b></td><td>MOH Oman</td><td><span class="badge badge-approved">Approved</span></td><td>Medical Device Dept Approval</td></tr>
        <tr><td><b>🇧🇭 Bahrain</b></td><td>NHRA</td><td><span class="badge badge-approved">Approved</span></td><td>NHRA Medical Device License</td></tr>
        <tr><td><b>🇮🇶 Iraq</b></td><td>MOH Iraq (KIMADIA)</td><td><span class="badge badge-pending">Under Process</span></td><td>Tender Registration &amp; MOH Dossier</td></tr>
        <tr><td><b>🇯🇴 Jordan</b></td><td>JFDA</td><td><span class="badge badge-approved">Approved</span></td><td>JFDA Medical Device Registration</td></tr>
        <tr><td><b>🇱🇧 Lebanon</b></td><td>MOPH Lebanon</td><td><span class="badge badge-pending">Under Renewal</span></td><td>Import Permit &amp; Quality Cert</td></tr>
      </tbody>
    </table>
  </div>
</div>

</div><!-- end .main -->
</div><!-- end .dash -->

<script>
const countryData = {
  sa:{flag:'🇸🇦',name:'Saudi Arabia',sub:'GCC — Largest Market',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/saudi_landscape.jpeg',
    colors:{primary:'#006400',secondary:'#ffffff',accent:'#ffffff'},
    kpi:[{l:'HD Patients',v:'18,500'},{l:'PD Patients',v:'740'},{l:'Catheters Used',v:'47,970'},{l:'Market Value',v:'$6.2M'}]},
  ae:{flag:'🇦🇪',name:'UAE',sub:'GCC — Premium Segment',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/uae_landscape.jpeg',
    colors:{primary:'#00732f',secondary:'#ff0000',accent:'#ffffff'},
    kpi:[{l:'HD Patients',v:'10,900'},{l:'PD Patients',v:'436'},{l:'Catheters Used',v:'28,245'},{l:'Market Value',v:'$3.8M'}]},
  kw:{flag:'🇰🇼',name:'Kuwait',sub:'GCC — High Spend Per Patient',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/kuwait_landscape.jpeg',
    colors:{primary:'#007a3d',secondary:'#ffffff',accent:'#ce1126'},
    kpi:[{l:'HD Patients',v:'3,500'},{l:'PD Patients',v:'140'},{l:'Catheters Used',v:'9,065'},{l:'Market Value',v:'$1.4M'}]},
  qa:{flag:'🇶🇦',name:'Qatar',sub:'GCC — Centralized Procurement',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/qatar_landscape.jpeg',
    colors:{primary:'#8d1b3d',secondary:'#ffffff',accent:'#8d1b3d'},
    kpi:[{l:'HD Patients',v:'2,800'},{l:'PD Patients',v:'112'},{l:'Catheters Used',v:'7,252'},{l:'Market Value',v:'$1.1M'}]},
  om:{flag:'🇴🇲',name:'Oman',sub:'GCC — Growing Market',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/oman_landscape.jpeg',
    colors:{primary:'#db161b',secondary:'#ffffff',accent:'#008000'},
    kpi:[{l:'HD Patients',v:'1,900'},{l:'PD Patients',v:'76'},{l:'Catheters Used',v:'4,921'},{l:'Market Value',v:'$0.7M'}]},
  bh:{flag:'🇧🇭',name:'Bahrain',sub:'GCC — Small High-Income',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/bahrain_landscape.jpeg',
    colors:{primary:'#ce1126',secondary:'#ffffff',accent:'#ce1126'},
    kpi:[{l:'HD Patients',v:'1,200'},{l:'PD Patients',v:'48'},{l:'Catheters Used',v:'3,108'},{l:'Market Value',v:'$0.5M'}]},
  iq:{flag:'🇮🇶',name:'Iraq',sub:'ME — High Volume Opportunity',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/iraq_landscape.jpeg',
    colors:{primary:'#ce1126',secondary:'#ffffff',accent:'#ffffff'},
    kpi:[{l:'HD Patients',v:'4,200'},{l:'PD Patients',v:'168'},{l:'Catheters Used',v:'10,878'},{l:'Market Value',v:'$1.2M'}]},
  jo:{flag:'🇯🇴',name:'Jordan',sub:'ME — Medical Hub',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/jordon_landscape.jpeg',
    colors:{primary:'#007a3d',secondary:'#ffffff',accent:'#ce1126'},
    kpi:[{l:'HD Patients',v:'2,100'},{l:'PD Patients',v:'84'},{l:'Catheters Used',v:'5,439'},{l:'Market Value',v:'$0.8M'}]},
  lb:{flag:'🇱🇧',name:'Lebanon',sub:'ME — Under Renewal',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/lebanon_landscape.jpeg',
    colors:{primary:'#ee161f',secondary:'#ffffff',accent:'#00a650'},
    kpi:[{l:'HD Patients',v:'1,700'},{l:'PD Patients',v:'68'},{l:'Catheters Used',v:'4,403'},{l:'Market Value',v:'$0.6M'}]}
};

function openCountry(code){
  const d = countryData[code];
  if(!d) return;
  const existing = document.getElementById('country-overlay');
  if(existing) existing.remove();
  const overlay = document.createElement('div');
  overlay.id = 'country-overlay';
  overlay.style.cssText = `
    position:fixed;top:0;left:0;right:0;bottom:0;z-index:9999;
    display:flex;flex-direction:column;overflow-y:auto;
    background:linear-gradient(180deg,${d.colors.primary}dd 0%,#0b1628 45%);
  `;
  overlay.innerHTML = `
    <div style="position:relative;width:100%;height:320px;overflow:hidden;flex-shrink:0;">
      <img src="${d.landscape}" style="width:100%;height:100%;object-fit:cover;opacity:0.4;display:block;"/>
      <div style="position:absolute;inset:0;background:linear-gradient(to bottom,transparent 40%,#0b1628 100%);"></div>
      <div style="position:absolute;top:20px;left:24px;">
        <button onclick="document.getElementById('country-overlay').remove()"
          style="background:rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.3);color:#fff;padding:8px 18px;border-radius:8px;cursor:pointer;font-size:13px;backdrop-filter:blur(6px);">
          ← Back
        </button>
      </div>
      <div style="position:absolute;bottom:24px;left:32px;display:flex;align-items:center;gap:16px;">
        <span style="font-size:64px;filter:drop-shadow(0 2px 8px rgba(0,0,0,0.5));">${d.flag}</span>
        <div>
          <div style="font-size:32px;font-weight:800;color:#ffffff;text-shadow:0 2px 12px rgba(0,0,0,0.7);">${d.name}</div>
          <div style="font-size:13px;color:${d.colors.accent};filter:brightness(1.8);margin-top:4px;">${d.sub}</div>
        </div>
      </div>
    </div>
    <div style="padding:24px 32px;flex:1;">
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px;">
        ${d.kpi.map(k=>`
          <div style="background:rgba(255,255,255,0.06);border:1px solid ${d.colors.primary}55;border-top:3px solid ${d.colors.primary};border-radius:14px;padding:20px;text-align:center;backdrop-filter:blur(8px);">
            <div style="font-size:10px;color:#a0b0c8;text-transform:uppercase;letter-spacing:1.2px;font-weight:600;">${k.l}</div>
            <div style="font-size:28px;font-weight:800;color:#ffffff;margin-top:10px;">${k.v}</div>
          </div>
        `).join('')}
      </div>
      <div onmouseenter="this.style.transform='translateY(-4px)';this.style.boxShadow='0 8px 24px ${d.colors.primary}44';this.style.borderColor='${d.colors.primary}'"
     onmouseleave="this.style.transform='';this.style.boxShadow='';this.style.borderColor='${d.colors.primary}55'"
     style="background:rgba(255,255,255,0.06);border:1px solid ${d.colors.primary}55;border-top:3px solid ${d.colors.primary};border-radius:14px;padding:20px;text-align:center;backdrop-filter:blur(8px);transition:all 0.2s;cursor:default;">
        <div style="font-size:13px;font-weight:600;color:#c8d8f0;margin-bottom:10px;">📊 Market Overview</div>
        <div style="color:#6a85b0;font-size:12px;">Detailed market data coming soon...</div>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
}

function closeCountry(){document.getElementById('cd-panel').classList.remove('open');}

function filterCompetitors(type,btn){
  document.querySelectorAll('.comp-filter-btn').forEach(b=>{b.classList.remove('bg-blue-600','text-white');b.classList.add('bg-[#1a2d4d]','text-slate-300');});
  btn.classList.add('bg-blue-600','text-white');btn.classList.remove('bg-[#1a2d4d]','text-slate-300');
  document.querySelectorAll('.comp-card').forEach(c=>{
    if(type==='all'){c.style.display='';}
    else{c.style.display=c.classList.contains(type)?'':'none';}
  });
}

function toggleDetails(btn){
  const panel=btn.closest('.comp-card').querySelector('.details-panel');
  panel.classList.toggle('hidden');
  btn.textContent=panel.classList.contains('hidden')?'Details ←':'Hide ↑';
}

let marketMap=null;
const marketPoints=[
  {country:"Saudi Arabia",city:"Riyadh",lat:24.7136,lng:46.6753,patients:18500,priority:"Critical"},
  {country:"Saudi Arabia",city:"Jeddah",lat:21.4858,lng:39.1925,patients:9200,priority:"High"},
  {country:"UAE",city:"Dubai",lat:25.2048,lng:55.2708,patients:6100,priority:"High"},
  {country:"UAE",city:"Abu Dhabi",lat:24.4539,lng:54.3773,patients:4800,priority:"Medium"},
  {country:"Qatar",city:"Doha",lat:25.2854,lng:51.531,patients:2800,priority:"Medium"},
  {country:"Kuwait",city:"Kuwait City",lat:29.3759,lng:47.9774,patients:3500,priority:"High"},
  {country:"Iraq",city:"Baghdad",lat:33.3152,lng:44.3661,patients:4200,priority:"High"},
  {country:"Jordan",city:"Amman",lat:31.9539,lng:35.9106,patients:2100,priority:"Medium"},
  {country:"Lebanon",city:"Beirut",lat:33.8938,lng:35.5018,patients:1700,priority:"Low"},
  {country:"Oman",city:"Muscat",lat:23.588,lng:58.3829,patients:1900,priority:"Medium"},
  {country:"Bahrain",city:"Manama",lat:26.2235,lng:50.5876,patients:1200,priority:"Low"}
];
const priorityColors={Critical:"#ef4444",High:"#f97316",Medium:"#eab308",Low:"#22c55e"};

function createMarketMap(){
  if(!document.getElementById("market-map"))return;
  if(marketMap!==null){marketMap.invalidateSize();return;}
  marketMap=L.map("market-map",{zoomControl:true,scrollWheelZoom:true});
  marketMap.setView([27.5,46.5],5);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:18,attribution:"&copy; OpenStreetMap contributors"}).addTo(marketMap);
  marketPoints.forEach(pt=>{
    const color=priorityColors[pt.priority]||"#60a5fa";
    const radius=pt.priority==="Critical"?13:pt.priority==="High"?11:pt.priority==="Medium"?9:7;
    L.circleMarker([pt.lat,pt.lng],{radius,color:"#ffffff",weight:2,fillColor:color,fillOpacity:0.9}).addTo(marketMap)
     .bindPopup('<div class="map-popup"><div class="map-popup-title">'+pt.city+', '+pt.country+'</div><div class="map-popup-row"><b>HD Patients:</b> '+pt.patients.toLocaleString()+'</div><div class="map-popup-row"><b>Priority:</b> '+pt.priority+'</div></div>');
  });
  const legend=L.control({position:"bottomright"});
  legend.onAdd=function(){const div=L.DomUtil.create("div");div.style.cssText="background:#0b1628;padding:10px 12px;border:1px solid #1e3d7a;border-radius:8px;color:#e8edf5;font-size:11px;";div.innerHTML='<div style="font-weight:700;margin-bottom:7px;color:#c8d8f0">MARKET PRIORITY</div><div>🔴 Critical</div><div>🟠 High</div><div>🟡 Medium</div><div>🟢 Low</div>';return div;};
  legend.addTo(marketMap);
  setTimeout(()=>marketMap.invalidateSize(),300);
}

function navigate(el,pageId){
  const page=document.getElementById('page-'+pageId);
  if(!page) return;
  const overlay=document.getElementById('country-overlay');
  if(overlay) overlay.remove();
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  if(el) el.classList.add('active');
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  page.classList.add('active');
  if(pageId==="hotareas"){setTimeout(()=>{createMarketMap();if(marketMap)marketMap.invalidateSize();},200);}
}
</script>
</body>
</html>
"""
components.html(dashboard_html, height=1080, scrolling=True)
