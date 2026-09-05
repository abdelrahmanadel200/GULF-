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
.sidebar { width: 200px; min-width: 200px; background: #070f1f; border-right: 1px solid #1e3d7a; display: flex; flex-direction: column; padding: 18px 0; position: fixed; top: 0; left: 0; bottom: 0; z-index: 10; }
.logo { padding: 0 16px 18px; border-bottom: 1px solid #1e3d7a; margin-bottom: 10px; }
.logo-text { font-size: 15px; font-weight: 700; color: #60a5fa; letter-spacing: 1.5px; }
.logo-sub { font-size: 10px; color: #3a5278; margin-top: 2px; }
.nav-section-label { font-size: 9px; letter-spacing: 1.5px; color: #2a4060; text-transform: uppercase; padding: 14px 16px 6px; font-weight: 700; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 10px 16px; cursor: pointer; font-size: 12px; color: #6a85b0; border-left: 3px solid transparent; transition: all 0.15s; user-select: none; }
.nav-item:hover { background: #0f1f3d; color: #c8d8f0; }
.nav-item.active { background: #0f1f3d; color: #60a5fa; border-left-color: #2563eb; font-weight: 600; }
.nav-icon { font-size: 15px; width: 18px; text-align: center; }
.main { margin-left: 200px; flex: 1; min-height: 100vh; }
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
.country-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 0 16px 16px; }
.c-card { background: #0f1f3d; border: 1px solid #1e3d7a; border-radius: 14px; padding: 18px 14px; cursor: pointer; transition: all .18s; display: flex; flex-direction: column; align-items: center; gap: 8px; position: relative; overflow: hidden; }
.c-card:hover, .c-card:focus { outline: none; transform: translateY(-2px); border-color: var(--cc, #2563eb); box-shadow: 0 0 0 2px var(--cc, #2563eb); }
.c-flag { font-size: 42px; line-height: 1; }
.c-name { font-size: 13px; font-weight: 700; color: #e8edf5; }
.c-accent { position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: var(--cc, #2563eb); }
..c-img{width:100%;height:100px;object-fit:cover;border-radius:10px;display:block;}
.c-card{background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;padding:10px 10px 14px;cursor:pointer;transition:all .18s;display:flex;flex-direction:column;align-items:center;gap:6px;position:relative;overflow:hidden;}
.cd-panel { display: none; margin: 0 16px 16px; background: #0f1f3d; border: 1px solid #1e3d7a; border-radius: 14px; padding: 20px; animation: fadeIn .2s; }
.cd-panel.open { display: block; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.cd-header { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
.cd-flag { font-size: 44px; }
.cd-title { font-size: 18px; font-weight: 700; color: #e8edf5; }
.cd-sub { font-size: 11px; color: #6a85b0; margin-top: 2px; }
.cd-kpi { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 14px; }
.cd-kpi-item { background: #0b1628; border: 1px solid #1e3d7a; border-radius: 10px; padding: 12px; text-align: center; }
.cd-kpi-label { font-size: 9px; color: #6a85b0; text-transform: uppercase; letter-spacing: .8px; }
.cd-kpi-val { font-size: 18px; font-weight: 700; color: #60a5fa; margin-top: 4px; }
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
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/kuwait_flag.jpeg" class="c-img"/>
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
    <img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/iraq_flag.jpeg" class="c-img"/>
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
  <div class="placeholder-page"><div class="placeholder-icon">📈</div><div class="placeholder-title">Revenue Forecast</div><div class="placeholder-sub">Coming soon</div></div>
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
  <div class="placeholder-page"><div class="placeholder-icon">📅</div><div class="placeholder-title">Exhibitions</div><div class="placeholder-sub">Coming soon</div></div>
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
  sa:{flag:'🇸🇦',name:'Saudi Arabia',sub:'GCC — Largest Market',color:'#10b981',kpi:[{l:'HD Patients',v:'18,500'},{l:'HD Centers',v:'214'},{l:'HD Machines',v:'12,400'},{l:'Market Value',v:'$6.2M'}]},
  ae:{flag:'🇦🇪',name:'UAE',sub:'GCC — Premium Segment',color:'#f59e0b',kpi:[{l:'HD Patients',v:'10,900'},{l:'HD Centers',v:'98'},{l:'HD Machines',v:'6,800'},{l:'Market Value',v:'$3.8M'}]},
  kw:{flag:'🇰🇼',name:'Kuwait',sub:'GCC — High Spend Per Patient',color:'#3b82f6',kpi:[{l:'HD Patients',v:'3,500'},{l:'HD Centers',v:'42'},{l:'HD Machines',v:'2,100'},{l:'Market Value',v:'$1.4M'}]},
  qa:{flag:'🇶🇦',name:'Qatar',sub:'GCC — Centralized Procurement',color:'#8b5cf6',kpi:[{l:'HD Patients',v:'2,800'},{l:'HD Centers',v:'28'},{l:'HD Machines',v:'1,700'},{l:'Market Value',v:'$1.1M'}]},
  om:{flag:'🇴🇲',name:'Oman',sub:'GCC — Growing Market',color:'#ef4444',kpi:[{l:'HD Patients',v:'1,900'},{l:'HD Centers',v:'31'},{l:'HD Machines',v:'1,200'},{l:'Market Value',v:'$0.7M'}]},
  bh:{flag:'🇧🇭',name:'Bahrain',sub:'GCC — Small High-Income',color:'#ec4899',kpi:[{l:'HD Patients',v:'1,200'},{l:'HD Centers',v:'18'},{l:'HD Machines',v:'780'},{l:'Market Value',v:'$0.5M'}]},
  iq:{flag:'🇮🇶',name:'Iraq',sub:'ME — High Volume Opportunity',color:'#f97316',kpi:[{l:'HD Patients',v:'4,200'},{l:'HD Centers',v:'89'},{l:'HD Machines',v:'3,100'},{l:'Market Value',v:'$1.2M'}]},
  jo:{flag:'🇯🇴',name:'Jordan',sub:'ME — Medical Hub',color:'#06b6d4',kpi:[{l:'HD Patients',v:'2,100'},{l:'HD Centers',v:'67'},{l:'HD Machines',v:'1,400'},{l:'Market Value',v:'$0.8M'}]},
  lb:{flag:'🇱🇧',name:'Lebanon',sub:'ME — Under Renewal',color:'#a3e635',kpi:[{l:'HD Patients',v:'1,700'},{l:'HD Centers',v:'55'},{l:'HD Machines',v:'980'},{l:'Market Value',v:'$0.6M'}]}
};

function openCountry(code){
  const d=countryData[code];
  document.getElementById('cd-flag').textContent=d.flag;
  document.getElementById('cd-title').textContent=d.name;
  document.getElementById('cd-sub').textContent=d.sub;
  document.getElementById('cd-kpi').innerHTML=d.kpi.map(k=>'<div class="cd-kpi-item"><div class="cd-kpi-label">'+k.l+'</div><div class="cd-kpi-val" style="color:'+d.color+'">'+k.v+'</div></div>').join('');
  const p=document.getElementById('cd-panel');
  p.classList.add('open');
  p.scrollIntoView({behavior:'smooth',block:'nearest'});
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
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('page-'+pageId).classList.add('active');
  if(pageId==="hotareas"){setTimeout(()=>{createMarketMap();if(marketMap)marketMap.invalidateSize();},200);}
}
</script>
</body>
</html>
"""

components.html(dashboard_html, height=800, scrolling=False)
