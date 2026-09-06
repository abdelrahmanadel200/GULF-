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
#page-countries { --country-primary:#2563eb; --country-secondary:#ffffff; --country-accent:#60a5fa; transition:background .35s ease, box-shadow .35s ease; }
#page-countries.country-theme { background:linear-gradient(180deg, color-mix(in srgb, var(--country-primary) 9%, transparent) 0%, transparent 32%); }
.country-inline-detail { margin:0 16px 24px; border:1px solid color-mix(in srgb, var(--country-primary) 70%, #1e3d7a); border-radius:14px; overflow:hidden; background:#0b1628; box-shadow:0 14px 40px rgba(0,0,0,.30),0 0 28px color-mix(in srgb, var(--country-primary) 16%, transparent); animation:fadeIn .22s ease; }
.cid-hero { position:relative; height:300px; overflow:hidden; background:#071426; }
.cid-landscape { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:center center; display:block; }
.cid-overlay { position:absolute; inset:0; background:linear-gradient(90deg,rgba(4,15,30,.86) 0%,rgba(4,15,30,.35) 45%,rgba(4,15,30,.15) 100%),linear-gradient(0deg,rgba(7,20,38,.94) 0%,rgba(7,20,38,.05) 48%); }
.cid-back { position:absolute; top:18px; left:20px; z-index:4; background:rgba(3,12,24,.72); border:1px solid rgba(255,255,255,.25); color:#fff; padding:8px 16px; border-radius:8px; cursor:pointer; font-size:12px; backdrop-filter:blur(7px); transition:.2s ease; }
.cid-back:hover { border-color:var(--country-accent); background:rgba(3,12,24,.88); }
.cid-title { position:absolute; left:28px; bottom:24px; z-index:4; display:flex; align-items:center; gap:14px; }
.cid-flag { width:58px; height:42px; display:flex; align-items:center; justify-content:center; filter:drop-shadow(0 3px 10px rgba(0,0,0,.55)); }
.cid-flag img { width:56px; height:38px; object-fit:cover; object-position:center; border-radius:7px; border:1px solid rgba(255,255,255,.35); display:block; }
.cid-name { font-size:32px; font-weight:800; color:#fff; text-shadow:0 2px 12px rgba(0,0,0,.7); }
.cid-sub { margin-top:4px; font-size:13px; color:#dbeafe; }
.cid-meta { position:absolute; right:28px; top:55px; z-index:4; display:flex; flex-direction:column; gap:18px; min-width:190px; }
.cid-meta div { display:grid; grid-template-columns:24px 1fr; column-gap:8px; align-items:center; }
.cid-meta span { grid-row:1 / span 2; font-size:20px; }
.cid-meta small { color:#7f9ac1; font-size:10px; }
.cid-meta b { color:#e8edf5; font-size:13px; }
.cid-body { padding:20px 24px 24px; background:#06152b; }
.cid-kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }
.cid-kpi { min-height:92px; background:rgba(255,255,255,.035); border:1px solid color-mix(in srgb, var(--country-primary) 65%, #1264a3); border-radius:13px; padding:16px 18px; transition:border-color .2s, box-shadow .2s; }
.cid-kpi:hover { border-color:var(--country-accent); box-shadow:0 0 18px color-mix(in srgb, var(--country-primary) 12%, transparent); }
.cid-kpi-label { color:#6fa9dc; font-size:10px; text-transform:uppercase; letter-spacing:1px; font-weight:700; }
.cid-kpi-value { margin-top:10px; color:#fff; font-size:24px; font-weight:800; }
.cid-network { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin-top:16px; }
.cid-network-card { min-height:78px; background:rgba(255,255,255,.035); border:1px solid color-mix(in srgb, var(--country-primary) 55%, #1e3d7a); border-radius:12px; padding:14px 18px; display:flex; align-items:center; justify-content:space-between; gap:12px; }
.cid-network-label { color:#7f9ac1; font-size:10px; text-transform:uppercase; letter-spacing:1px; font-weight:700; }
.cid-network-value { color:#fff; font-size:23px; font-weight:800; }
.cid-network-sub { color:var(--country-accent); font-size:10px; margin-top:3px; }
@media (max-width:1000px) { .cid-meta { position:static; display:none; } .cid-name { font-size:28px; } .cid-kpi-grid { grid-template-columns:repeat(2,1fr); } }
@media (max-width:600px) { .country-inline-detail { margin:0 10px 18px; } .cid-hero { height:235px; } .cid-title { left:16px; bottom:18px; } .cid-name { font-size:22px; } .cid-flag { width:46px; height:36px; } .cid-flag img { width:44px; height:30px; } .cid-kpi-grid { grid-template-columns:1fr; } .cid-network { grid-template-columns:1fr; } .cid-body { padding:14px; } }
.country-grid { display:flex; flex-wrap:wrap; justify-content:center; gap:14px; margin:0 16px 16px; }
.country-grid .c-card { flex:0 0 calc((100% - 56px)/5); }
.c-card { height:138px; background:#0f1f3d; border:1px solid #1e3d7a; border-radius:12px; padding:0; cursor:pointer; transition:all .22s ease; display:flex; align-items:flex-end; position:relative; overflow:hidden; min-width:0; }
.c-card:hover,.c-card:focus { outline:none; transform:translateY(-2px); border-color:var(--cc,#2563eb); box-shadow:0 8px 22px rgba(0,0,0,.28),0 0 0 2px var(--cc,#2563eb)44; }
.c-card.active { transform:translateY(-3px) scale(1.015); border-color:var(--cc,#2563eb); box-shadow:0 10px 28px rgba(0,0,0,.35),0 0 0 2px var(--cc,#2563eb),0 0 30px color-mix(in srgb, var(--cc,#2563eb) 28%, transparent); }
.c-card.active .c-overlay { background:linear-gradient(to bottom,rgba(4,15,31,.02) 20%,rgba(4,15,31,.14) 45%,rgba(4,15,31,.90) 100%); }
.c-card.active .c-accent { height:4px; box-shadow:0 0 14px var(--cc,#2563eb); }
.c-landscape { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:center center; display:block; transform:scale(1.01); transition:transform .25s ease,filter .25s ease; }
.c-card:hover .c-landscape { transform:scale(1.04); filter:brightness(1.06); }
.c-card.active .c-landscape { transform:scale(1.06); filter:brightness(1.08) saturate(1.05); }
.c-overlay { position:absolute; inset:0; background:linear-gradient(to bottom,rgba(4,15,31,.05) 25%,rgba(4,15,31,.18) 48%,rgba(4,15,31,.92) 100%); z-index:1; }
.c-bottom { position:relative; z-index:2; width:100%; display:flex; align-items:center; gap:9px; padding:0 13px 11px; min-width:0; }
.c-flag { width:30px; height:21px; flex:0 0 30px; display:flex; align-items:center; justify-content:center; filter:drop-shadow(0 2px 4px rgba(0,0,0,.45)); }
.c-flag img { width:30px; height:21px; object-fit:cover; object-position:center; display:block; border-radius:3px; border:1px solid rgba(255,255,255,.22); }
.c-name { font-size:13px; font-weight:700; color:#fff; text-align:left; padding:0; flex:1; display:block; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; text-shadow:0 2px 5px rgba(0,0,0,.7); }
.c-arrow { color:#fff; font-size:22px; line-height:1; flex:0 0 auto; opacity:.95; text-shadow:0 2px 5px rgba(0,0,0,.65); }
.c-accent { position:absolute; bottom:0; left:0; right:0; height:2px; background:var(--cc,#2563eb); z-index:3; transition:height .2s, box-shadow .2s; }
@media (max-width:1200px) { .country-grid .c-card { flex-basis:calc((100% - 42px)/4); } }
@media (max-width:900px) { .country-grid .c-card { flex-basis:calc((100% - 28px)/3); } }
@media (max-width:650px) { .country-grid { gap:10px; } .country-grid .c-card { flex-basis:calc((100% - 10px)/2); } .c-card { height:125px; } }
@media (max-width:430px) { .country-grid .c-card { flex-basis:100%; } }
.cd-panel { display:none; margin:0 16px 16px; background:#0f1f3d; border:1px solid #1e3d7a; border-radius:14px; padding:20px; animation:fadeIn .2s; }
.cd-panel.open { display:block; }
@keyframes fadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:none; } }
.cd-header { display:flex; align-items:center; gap:12px; margin-bottom:14px; }
.cd-flag { font-size:44px; }
.cd-title { font-size:18px; font-weight:700; color:#e8edf5; }
.cd-sub { font-size:11px; color:#6a85b0; margin-top:2px; }
.cd-kpi { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-bottom:14px; }
.cd-kpi-item { background:#0b1628; border:1px solid #1e3d7a; border-radius:10px; padding:14px 12px; text-align:center; border-top:2px solid #2563eb; }
.cd-kpi-label { font-size:9px; color:#6a85b0; text-transform:uppercase; letter-spacing:1.2px; font-weight:600; }
.cd-kpi-val { font-size:20px; font-weight:800; color:#60a5fa; margin-top:6px; letter-spacing:.5px; }
.cd-close { margin-left:auto; background:#1e3d7a; border:none; color:#c8d8f0; border-radius:8px; padding:6px 14px; cursor:pointer; font-size:12px; }
.cd-close:hover { background:#2563eb; }

/* Competitors by country */
.country-filter-btn,.comp-threat-btn{padding:8px 12px;border-radius:9px;border:1px solid #1e3d7a;background:#1a2d4d;color:#c8d8f0;font-size:11px;font-weight:600;cursor:pointer;transition:all .15s ease}.country-filter-btn:hover,.comp-threat-btn:hover{border-color:#3b82f6;transform:translateY(-1px)}.country-filter-btn.comp-country-active,.comp-threat-btn.comp-threat-active{background:#2563eb;border-color:#3b82f6;color:#fff}.comp-country-title{font-size:16px;font-weight:700;color:#e8edf5}.comp-country-sub{font-size:10px;color:#6a85b0;margin-top:3px}.comp-summary{display:flex;flex-wrap:wrap;gap:8px}.comp-summary-pill{background:#0f1f3d;border:1px solid #1e3d7a;border-radius:8px;padding:7px 10px;font-size:10px;color:#c8d8f0}.comp-card-new{background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;padding:16px;position:relative;overflow:hidden;transition:all .18s ease}.comp-card-new:hover{border-color:#3b82f6;transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.18)}.comp-card-topline{position:absolute;top:0;left:0;right:0;height:3px}.comp-card-company{font-size:14px;font-weight:700;color:#fff}.comp-card-origin{font-size:10px;color:#6a85b0;margin-top:3px}.comp-threat-badge{display:inline-flex;align-items:center;padding:4px 7px;border-radius:6px;font-size:9px;font-weight:700}.comp-share-row{display:flex;justify-content:space-between;align-items:center;margin:12px 0 5px;font-size:10px;color:#94a3b8}.comp-share-value{color:#60a5fa;font-weight:700}.comp-share-bar{width:100%;height:6px;background:#081321;border-radius:99px;overflow:hidden;border:1px solid #14284b}.comp-share-fill{height:100%;border-radius:99px}.comp-mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:12px}.comp-mini-box{background:#081321;border:1px solid #1e3d7a;border-radius:9px;padding:9px}.comp-mini-label{display:block;color:#6a85b0;font-size:8px;text-transform:uppercase;letter-spacing:.8px;margin-bottom:4px}.comp-mini-text{color:#e2e8f0;font-size:10px;line-height:1.35}.comp-edge{margin-top:11px;padding-top:10px;border-top:1px solid #1e3d7a;color:#34d399;font-size:10px;line-height:1.35}.comp-details-btn{width:100%;margin-top:11px;padding:8px 10px;border-radius:8px;border:1px solid #1e3d7a;background:#13274c;color:#60a5fa;font-size:10px;font-weight:700;cursor:pointer}.comp-details-btn:hover{background:#1a3a6e;border-color:#3b82f6}.comp-details-panel{display:none;margin-top:10px;padding:11px;background:#081321;border:1px solid #1e3d7a;border-radius:9px}.comp-details-panel.open{display:block}.comp-detail-row{display:flex;justify-content:space-between;gap:10px;padding:6px 0;border-bottom:1px solid #14284b;font-size:10px}.comp-detail-row:last-child{border-bottom:none}.comp-detail-label{color:#6a85b0}.comp-detail-value{color:#e8edf5;text-align:right}
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
  <div class="nav-item active" data-page="overview" role="button" tabindex="0"><span class="nav-icon">🏠</span><span>Overview</span></div>
  <div class="nav-item" data-page="countries" role="button" tabindex="0"><span class="nav-icon">🌍</span><span>Country Analysis</span></div>
  <div class="nav-item" data-page="forecast" role="button" tabindex="0"><span class="nav-icon">📈</span><span>Revenue Forecast</span></div>
  <div class="nav-section-label">Market</div>
  <div class="nav-item" data-page="pricing" role="button" tabindex="0"><span class="nav-icon">💲</span><span>Pricing Intel</span></div>
  <div class="nav-item" data-page="tenders" role="button" tabindex="0"><span class="nav-icon">📋</span><span>Tenders</span></div>
  <div class="nav-item" data-page="competitors" role="button" tabindex="0"><span class="nav-icon">🏆</span><span>Competitors</span></div>
  <div class="nav-section-label">Field</div>
  <div class="nav-item" data-page="hotareas" role="button" tabindex="0"><span class="nav-icon">📍</span><span>Hot Areas</span></div>
  <div class="nav-item" data-page="exhibitions" role="button" tabindex="0"><span class="nav-icon">📅</span><span>Exhibitions</span></div>
  <div class="nav-item" data-page="regulatory" role="button" tabindex="0"><span class="nav-icon">📜</span><span>Regulatory</span></div>
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
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/saudi_landscape.jpeg" alt="Saudi Arabia landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/saudi_arabia_flag.jpeg" alt="Saudi Arabia flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Saudi Arabia</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#f59e0b" role="listitem" tabindex="0" onclick="openCountry('ae')" onkeydown="if(event.key==='Enter')openCountry('ae')" aria-label="UAE">
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/uae_landscape.jpeg" alt="UAE landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/uae_flag.jpeg" alt="UAE flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">UAE</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#3b82f6" role="listitem" tabindex="0" onclick="openCountry('kw')" onkeydown="if(event.key==='Enter')openCountry('kw')" aria-label="Kuwait">
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/kuwait_landscape.jpeg" alt="Kuwait landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/kuwait_flag.jpeg" alt="Kuwait flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Kuwait</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#8b5cf6" role="listitem" tabindex="0" onclick="openCountry('qa')" onkeydown="if(event.key==='Enter')openCountry('qa')" aria-label="Qatar">
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/qatar_landscape.jpeg" alt="Qatar landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/qatar_flag.jpeg" alt="Qatar flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Qatar</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#ef4444" role="listitem" tabindex="0" onclick="openCountry('om')" onkeydown="if(event.key==='Enter')openCountry('om')" aria-label="Oman">
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/oman_landscape.jpeg" alt="Oman landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/oman_flag.jpeg" alt="Oman flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Oman</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#ec4899" role="listitem" tabindex="0" onclick="openCountry('bh')" onkeydown="if(event.key==='Enter')openCountry('bh')" aria-label="Bahrain">
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/bahrain_landscape.jpg" alt="Bahrain landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/bahraien_flag.jpeg" alt="Bahrain flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Bahrain</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#06b6d4" role="listitem" tabindex="0" onclick="openCountry('jo')" onkeydown="if(event.key==='Enter')openCountry('jo')" aria-label="Jordan">
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/jordon_landscape.jpeg" alt="Jordan landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/jordon_flag.jpeg" alt="Jordan flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Jordan</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#a3e635" role="listitem" tabindex="0" onclick="openCountry('lb')" onkeydown="if(event.key==='Enter')openCountry('lb')" aria-label="Lebanon">
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/lebanon_landscape.jpeg" alt="Lebanon landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/lebanon_flag.jpeg" alt="Lebanon flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Lebanon</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" style="--cc:#f97316" role="listitem" tabindex="0" onclick="openCountry('iq')" onkeydown="if(event.key==='Enter')openCountry('iq')" aria-label="Iraq">
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/iraq_landscape.jpg" alt="Iraq landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/iraq_flag.jpg" alt="Iraq flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Iraq</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
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
          <div style="font-size:18px;font-weight:800;color:#3b82f6;margin-top:2px;">$774,610</div>
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
  <div style="padding:0 16px 32px;">
    <style>
      #page-tenders * { box-sizing: border-box; }
      #page-tenders .tndr-kpis { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:14px; margin-bottom:18px; }
      #page-tenders .tndr-kpi { background:#0f1f3d; border:1px solid #1e3d7a; border-radius:13px; padding:17px 18px; position:relative; overflow:hidden; }
      #page-tenders .tndr-kpi::after { content:""; position:absolute; left:0; top:0; width:3px; height:100%; background:#2563eb; }
      #page-tenders .tndr-kpi:nth-child(2)::after { background:#60a5fa; }
      #page-tenders .tndr-kpi:nth-child(3)::after { background:#f59e0b; }
      #page-tenders .tndr-kpi:nth-child(4)::after { background:#3b82f6; }
      #page-tenders .tndr-kpi:nth-child(5)::after { background:#34d399; }
      #page-tenders .tndr-kpi-label { color:#6a85b0; font-size:9px; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }
      #page-tenders .tndr-kpi-value { color:#e8edf5; font-size:24px; font-weight:700; }
      #page-tenders .tndr-filters { background:#0f1f3d; border:1px solid #1e3d7a; border-radius:13px; padding:15px; margin-bottom:16px; }
      #page-tenders .tndr-filter-group { display:flex; align-items:center; flex-wrap:wrap; gap:7px; }
      #page-tenders .tndr-filter-group + .tndr-filter-group { margin-top:11px; padding-top:11px; border-top:1px solid rgba(30,61,122,.55); }
      #page-tenders .tndr-filter-label { color:#6a85b0; font-size:11px; font-weight:700; min-width:72px; text-transform:uppercase; }
      #page-tenders .tndr-filter-btn { border:1px solid #1e3d7a; background:#0b1628; color:#8fa8cf; border-radius:9px; padding:7px 11px; font-family:inherit; font-size:12px; font-weight:600; cursor:pointer; transition:all .16s; }
      #page-tenders .tndr-filter-btn:hover { border-color:#3b82f6; color:#e8edf5; background:#10264a; }
      #page-tenders .tndr-filter-btn.active { background:rgba(37,99,235,.22); border-color:#3b82f6; color:#e8edf5; }
      #page-tenders .tndr-table-wrap { width:100%; overflow-x:auto; background:#0f1f3d; border:1px solid #1e3d7a; border-radius:13px; }
      #page-tenders .tndr-table { width:100%; min-width:1050px; border-collapse:separate; border-spacing:0; font-size:12px; }
      #page-tenders .tndr-table thead th { background:#10264a; color:#6a85b0; text-align:left; padding:13px 14px; font-size:10px; text-transform:uppercase; letter-spacing:.55px; font-weight:700; border-bottom:1px solid #1e3d7a; white-space:nowrap; }
      #page-tenders .tndr-table tbody td { padding:13px 14px; border-bottom:1px solid rgba(30,61,122,.55); color:#cbd6e8; vertical-align:middle; }
      #page-tenders .tndr-table tbody tr { transition:background .14s; }
      #page-tenders .tndr-table tbody tr:hover { background:rgba(37,99,235,.07); }
      #page-tenders .tndr-table tbody tr:last-child td { border-bottom:0; }
      #page-tenders .tndr-number { width:40px; color:#6a85b0 !important; font-weight:700; }
      #page-tenders .tndr-name { color:#e8edf5 !important; font-weight:700; min-width:245px; }
      #page-tenders .tndr-value { color:#e8edf5 !important; font-weight:700; white-space:nowrap; }
      #page-tenders .tndr-country, #page-tenders .tndr-deadline { white-space:nowrap; }
      #page-tenders .tndr-authority { min-width:155px; }
      #page-tenders .tndr-status { display:inline-flex; align-items:center; border-radius:999px; padding:5px 9px; font-size:10px; font-weight:700; white-space:nowrap; border:1px solid; }
      #page-tenders .tndr-status-open { color:#fbbf24; background:rgba(245,158,11,.12); border-color:rgba(245,158,11,.5); }
      #page-tenders .tndr-status-submitted { color:#60a5fa; background:rgba(59,130,246,.12); border-color:rgba(59,130,246,.5); }
      #page-tenders .tndr-status-won { color:#34d399; background:rgba(52,211,153,.12); border-color:rgba(52,211,153,.5); }
      #page-tenders .tndr-status-closed { color:#8fa8cf; background:rgba(106,133,176,.12); border-color:rgba(106,133,176,.5); }
      #page-tenders .tndr-view-btn { border:1px solid #2563eb; background:rgba(37,99,235,.16); color:#60a5fa; border-radius:8px; padding:6px 12px; font-family:inherit; font-size:11px; font-weight:700; cursor:pointer; transition:all .16s; }
      #page-tenders .tndr-view-btn:hover { background:#2563eb; color:#fff; }
      #page-tenders .tndr-empty { text-align:center; padding:42px 20px !important; color:#6a85b0 !important; }
      #page-tenders .tndr-modal-overlay { display:none; position:fixed; inset:0; z-index:99999; background:rgba(3,10,22,.78); backdrop-filter:blur(5px); align-items:center; justify-content:center; padding:22px; }
      #page-tenders .tndr-modal-overlay.show { display:flex; }
      #page-tenders .tndr-modal-card { width:min(650px,100%); max-height:min(760px,92vh); overflow-y:auto; background:#0f1f3d; border:1px solid #1e3d7a; border-radius:14px; box-shadow:0 25px 80px rgba(0,0,0,.48); }
      #page-tenders .tndr-modal-header { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; padding:20px 21px; border-bottom:1px solid #1e3d7a; background:#10264a; }
      #page-tenders .tndr-modal-title { margin:0; color:#e8edf5; font-size:17px; font-weight:700; line-height:1.35; }
      #page-tenders .tndr-modal-kicker { margin:0 0 5px; color:#60a5fa; font-size:10px; text-transform:uppercase; letter-spacing:.65px; font-weight:800; }
      #page-tenders .tndr-modal-x { border:1px solid #1e3d7a; background:#0b1628; color:#8fa8cf; width:31px; height:31px; border-radius:8px; cursor:pointer; font-size:17px; display:flex; align-items:center; justify-content:center; }
      #page-tenders .tndr-modal-x:hover { color:#e8edf5; border-color:#3b82f6; }
      #page-tenders .tndr-modal-body { padding:20px 21px; }
      #page-tenders .tndr-detail-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }
      #page-tenders .tndr-detail { background:#0b1628; border:1px solid rgba(30,61,122,.75); border-radius:10px; padding:13px 14px; }
      #page-tenders .tndr-detail-full { grid-column:1/-1; }
      #page-tenders .tndr-detail-label { color:#6a85b0; font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:.55px; margin-bottom:6px; }
      #page-tenders .tndr-detail-value { color:#e8edf5; font-size:13px; font-weight:600; line-height:1.45; }
      #page-tenders .tndr-notes { color:#8fa8cf !important; font-weight:500 !important; }
      #page-tenders .tndr-modal-footer { padding:15px 21px 20px; display:flex; justify-content:flex-end; border-top:1px solid rgba(30,61,122,.65); }
      #page-tenders .tndr-close-btn { border:1px solid #1e3d7a; background:#10264a; color:#e8edf5; border-radius:9px; padding:8px 16px; font-family:inherit; font-size:12px; font-weight:700; cursor:pointer; }
      #page-tenders .tndr-close-btn:hover { border-color:#3b82f6; background:#15305c; }
      @media (max-width:900px) {
        #page-tenders .tndr-kpis { grid-template-columns:repeat(2,minmax(0,1fr)); }
        #page-tenders .tndr-detail-grid { grid-template-columns:1fr; }
        #page-tenders .tndr-detail-full { grid-column:auto; }
      }
    </style>

    <div style="margin-bottom:18px;">
      <div style="font-size:15px;font-weight:600;color:#c8d8f0;display:flex;align-items:center;gap:8px;margin-bottom:4px;">
        <span>📋</span> Tenders &amp; Procurement Intelligence
      </div>
      <div style="font-size:11px;color:#3a5278;">Gulf &amp; Middle East — Active Tenders + 2026/2027 Pipeline Forecast</div>
    </div>

    <div style="display:flex;gap:0;margin-bottom:18px;background:#0f1f3d;border:1px solid #1e3d7a;border-radius:12px;padding:5px;">
      <button id="tndr-tab-active" onclick="tndrSwitchTab('active')" style="flex:1;padding:10px 0;border:none;border-radius:9px;font-size:12px;font-weight:700;cursor:pointer;transition:all .2s;background:#2563eb;color:#fff;">
        📋 Active Tenders (14)
      </button>
      <button id="tndr-tab-pipeline" onclick="tndrSwitchTab('pipeline')" style="flex:1;padding:10px 0;border:none;border-radius:9px;font-size:12px;font-weight:700;cursor:pointer;transition:all .2s;background:transparent;color:#6a85b0;">
        🔭 Pipeline Forecast (20)
      </button>
    </div>

    <div id="tndr-section-active">
      <div class="tndr-kpis">
        <div class="tndr-kpi"><div class="tndr-kpi-label">Total Active Tenders</div><div class="tndr-kpi-value">14</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Estimated Total Value</div><div class="tndr-kpi-value" style="color:#60a5fa;">$4.2M</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Critical / Urgent</div><div class="tndr-kpi-value" style="color:#f59e0b;">4</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Submitted / Pending</div><div class="tndr-kpi-value" style="color:#3b82f6;">6</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Won YTD</div><div class="tndr-kpi-value" style="color:#34d399;">3</div></div>
      </div>

      <div class="tndr-filters">
        <div class="tndr-filter-group">
          <span class="tndr-filter-label">Country</span>
          <button class="tndr-filter-btn active" data-tndr-country="all">All</button>
          <button class="tndr-filter-btn" data-tndr-country="Saudi Arabia">🇸🇦 KSA</button>
          <button class="tndr-filter-btn" data-tndr-country="Iraq">🇮🇶 Iraq</button>
          <button class="tndr-filter-btn" data-tndr-country="Jordan">🇯🇴 Jordan</button>
          <button class="tndr-filter-btn" data-tndr-country="Lebanon">🇱🇧 Lebanon</button>
          <button class="tndr-filter-btn" data-tndr-country="Bahrain">🇧🇭 Bahrain</button>
          <button class="tndr-filter-btn" data-tndr-country="Oman">🇴🇲 Oman</button>
          <button class="tndr-filter-btn" data-tndr-country="UAE">🇦🇪 UAE</button>
          <button class="tndr-filter-btn" data-tndr-country="Qatar">🇶🇦 Qatar</button>
          <button class="tndr-filter-btn" data-tndr-country="Kuwait">🇰🇼 Kuwait</button>
        </div>
        <div class="tndr-filter-group">
          <span class="tndr-filter-label">Status</span>
          <button class="tndr-filter-btn active" data-tndr-status="all">All Status</button>
          <button class="tndr-filter-btn" data-tndr-status="Open">Open</button>
          <button class="tndr-filter-btn" data-tndr-status="Submitted">Submitted</button>
          <button class="tndr-filter-btn" data-tndr-status="Won">Won ✅</button>
          <button class="tndr-filter-btn" data-tndr-status="Closed">Closed</button>
        </div>
      </div>

      <div class="tndr-table-wrap">
        <table class="tndr-table">
          <thead><tr>
            <th>#</th><th>Tender Name</th><th>Country</th><th>Authority</th>
            <th>Est. Value</th><th>Deadline</th><th>Status</th><th>Action</th>
          </tr></thead>
          <tbody id="tndr-table-body"></tbody>
        </table>
      </div>
    </div>

    <div id="tndr-section-pipeline" style="display:none;">
      <div class="tndr-kpis">
        <div class="tndr-kpi"><div class="tndr-kpi-label">Total Pipeline</div><div class="tndr-kpi-value" style="color:#60a5fa;">20</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Est. Total Value</div><div class="tndr-kpi-value" style="color:#f59e0b;">$27M+</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Critical Priority</div><div class="tndr-kpi-value" style="color:#ef4444;">8</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Launching Q4 2026</div><div class="tndr-kpi-value" style="color:#a78bfa;">6</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Countries</div><div class="tndr-kpi-value" style="color:#34d399;">7</div></div>
      </div>
      <div class="tndr-filters">
        <div class="tndr-filter-group">
          <span class="tndr-filter-label">Country</span>
          <button class="tndr-filter-btn active" data-pipe-country="all">All</button>
          <button class="tndr-filter-btn" data-pipe-country="🇸🇦 Saudi Arabia">🇸🇦 KSA</button>
          <button class="tndr-filter-btn" data-pipe-country="🇶🇦 Qatar">🇶🇦 Qatar</button>
          <button class="tndr-filter-btn" data-pipe-country="🇦🇪 UAE">🇦🇪 UAE</button>
          <button class="tndr-filter-btn" data-pipe-country="🇴🇲 Oman">🇴🇲 Oman</button>
          <button class="tndr-filter-btn" data-pipe-country="🇰🇼 Kuwait">🇰🇼 Kuwait</button>
          <button class="tndr-filter-btn" data-pipe-country="🇯🇴 Jordan">🇯🇴 Jordan</button>
          <button class="tndr-filter-btn" data-pipe-country="🇱🇧 Lebanon">🇱🇧 Lebanon</button>
          <button class="tndr-filter-btn" data-pipe-country="🇮🇶 Iraq">🇮🇶 Iraq</button>
          <button class="tndr-filter-btn" data-pipe-country="🇧🇭 Bahrain">🇧🇭 Bahrain</button>
        </div>
        <div class="tndr-filter-group">
          <span class="tndr-filter-label">Priority</span>
          <button class="tndr-filter-btn active" data-pipe-priority="all">All Priority</button>
          <button class="tndr-filter-btn" data-pipe-priority="Critical">🔴 Critical</button>
          <button class="tndr-filter-btn" data-pipe-priority="High">🟠 High</button>
          <button class="tndr-filter-btn" data-pipe-priority="Medium">🟡 Medium</button>
        </div>
      </div>
      <div class="tndr-table-wrap">
        <table class="tndr-table" style="min-width:1200px;">
          <thead><tr>
            <th>#</th><th>Expected Tender Title</th><th>Country</th><th>Issuing Entity</th>
            <th>Ref. (Est.)</th><th>Launch</th><th>Closing</th><th>Est. Value</th><th>Priority</th>
          </tr></thead>
          <tbody id="pipe-table-body"></tbody>
        </table>
      </div>
      <div style="margin-top:14px;background:#0f1f3d;border:1px solid #1e3d7a;border-left:3px solid #f59e0b;border-radius:10px;padding:14px 16px;font-size:11px;color:#6a85b0;line-height:1.7;">
        <span style="color:#f59e0b;font-weight:700;">⚠️ Note:</span>
        Pipeline data represents <b style="color:#c8d8f0;">expected / forecasted tenders</b> based on historical procurement cycles and market intelligence.
        Tender references marked <b style="color:#c8d8f0;">(est.)</b> are estimated. Monitor official portals: NUPCO Etimad · HMC Portal · DAHC · Kimadia · MOH portals per country.
      </div>
    </div>

    <div class="tndr-modal-overlay" id="tndr-modal">
      <div class="tndr-modal-card">
        <div class="tndr-modal-header">
          <div><p class="tndr-modal-kicker">Tender Details</p><h3 class="tndr-modal-title" id="tndr-modal-title">—</h3></div>
          <button class="tndr-modal-x" id="tndr-modal-x" type="button">×</button>
        </div>
        <div class="tndr-modal-body">
          <div class="tndr-detail-grid">
            <div class="tndr-detail tndr-detail-full"><div class="tndr-detail-label">Tender Name</div><div class="tndr-detail-value" id="tndr-d-name"></div></div>
            <div class="tndr-detail"><div class="tndr-detail-label">Country</div><div class="tndr-detail-value" id="tndr-d-country"></div></div>
            <div class="tndr-detail"><div class="tndr-detail-label">Authority</div><div class="tndr-detail-value" id="tndr-d-authority"></div></div>
            <div class="tndr-detail"><div class="tndr-detail-label">Estimated Value</div><div class="tndr-detail-value" style="color:#60a5fa;font-size:18px;" id="tndr-d-value"></div></div>
            <div class="tndr-detail"><div class="tndr-detail-label">Deadline</div><div class="tndr-detail-value" id="tndr-d-deadline"></div></div>
            <div class="tndr-detail"><div class="tndr-detail-label">Status</div><div class="tndr-detail-value" id="tndr-d-status"></div></div>
            <div class="tndr-detail tndr-detail-full"><div class="tndr-detail-label">Notes</div><div class="tndr-detail-value tndr-notes" id="tndr-d-notes"></div></div>
          </div>
        </div>
        <div class="tndr-modal-footer"><button class="tndr-close-btn" id="tndr-modal-close" type="button">✕ Close</button></div>
      </div>
    </div>

  </div>
</div>

<!-- COMPETITORS -->
<!-- COMPETITORS -->
<div class="page" id="page-competitors">
  <div class="p-4 space-y-5">
    <div class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 bg-[#0f1f3d] p-5 rounded-2xl border border-[#1e3d7a]">
      <div><h2 class="text-xl font-bold text-white flex items-center gap-2"><span>🏆</span> Competitor Intelligence by Country</h2><p class="text-slate-400 text-xs mt-1">Select a market, review the competitor benchmark, and open any company for full details.</p></div>
      <div class="flex flex-wrap gap-2">
        <button onclick="setCompetitorCountry('sa',this)" class="country-filter-btn comp-country-active">🇸🇦 Saudi Arabia</button>
        <button onclick="setCompetitorCountry('ae',this)" class="country-filter-btn">🇦🇪 UAE</button>
        <button onclick="setCompetitorCountry('kw',this)" class="country-filter-btn">🇰🇼 Kuwait</button>
        <button onclick="setCompetitorCountry('qa',this)" class="country-filter-btn">🇶🇦 Qatar</button>
        <button onclick="setCompetitorCountry('om',this)" class="country-filter-btn">🇴🇲 Oman</button>
        <button onclick="setCompetitorCountry('bh',this)" class="country-filter-btn">🇧🇭 Bahrain</button>
        <button onclick="setCompetitorCountry('iq',this)" class="country-filter-btn">🇮🇶 Iraq</button>
        <button onclick="setCompetitorCountry('jo',this)" class="country-filter-btn">🇯🇴 Jordan</button>
        <button onclick="setCompetitorCountry('lb',this)" class="country-filter-btn">🇱🇧 Lebanon</button>
      </div>
    </div>
    <div id="competitor-country-header" class="bg-[#081321] border border-[#1e3d7a] rounded-xl p-4"></div>
    <div class="bg-[#081321] border border-[#1e3d7a] rounded-xl p-3 text-xs text-slate-400">
      📌 Competitor data below is taken directly from the <b class="text-slate-200">Competitor_Matrix</b> sheet. Market-share figures are shown exactly as provided in the workbook; <b class="text-slate-200">N/D</b> means no country-specific share was provided.
    </div>
    <div id="comp-grid" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"></div>
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
  sa:{flag:'🇸🇦',flagImg:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/saudi_arabia_flag.jpeg',name:'Saudi Arabia',sub:'GCC — Largest Market',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/saudi_landscape.jpeg',colors:{primary:'#006400',secondary:'#ffffff',accent:'#ffffff'},
    kpi:[{l:'Population 2026',v:'35,165,787'},{l:'HD Patients',v:'30,000'},{l:'PD Patients',v:'2,200'},{l:'Dialysis Facilities',v:'360'},{l:'HD Machines',v:'18,000'},{l:'Annual Catheter Demand',v:'77,530'},{l:'Market Value',v:'$9.30M'},{l:'Distributors / KOLs',v:'10 / 10'}]},
  ae:{flag:'🇦🇪',flagImg:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/uae_flag.jpeg',name:'UAE',sub:'GCC — Premium Segment',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/uae_landscape.jpeg',colors:{primary:'#00732f',secondary:'#ff0000',accent:'#ffffff'},
    kpi:[{l:'Population 2026',v:'11,574,682'},{l:'HD Patients',v:'3,000'},{l:'PD Patients',v:'120'},{l:'Dialysis Facilities',v:'60'},{l:'HD Machines',v:'4,500'},{l:'Annual Catheter Demand',v:'7,638'},{l:'Market Value',v:'$0.99M'},{l:'Distributors / KOLs',v:'10 / 10'}]},
  kw:{flag:'🇰🇼',flagImg:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/kuwait_flag.jpeg',name:'Kuwait',sub:'GCC — High Spend Per Patient',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/kuwait_landscape.jpeg',colors:{primary:'#007a3d',secondary:'#ffffff',accent:'#ce1126'},
    kpi:[{l:'Population 2026',v:'5,102,773'},{l:'HD Patients',v:'2,156'},{l:'PD Patients',v:'294'},{l:'Dialysis Facilities',v:'25'},{l:'HD Machines',v:'3,000'},{l:'Annual Catheter Demand',v:'5,728'},{l:'Market Value',v:'$0.72M'},{l:'Distributors / KOLs',v:'10 / 10'}]},
  qa:{flag:'🇶🇦',flagImg:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/qatar_flag.jpeg',name:'Qatar',sub:'GCC — Centralized Procurement',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/qatar_landscape.jpeg',colors:{primary:'#8d1b3d',secondary:'#ffffff',accent:'#8d1b3d'},
    kpi:[{l:'Population 2026',v:'3,173,559'},{l:'HD Patients',v:'1,200'},{l:'PD Patients',v:'180'},{l:'Dialysis Facilities',v:'18'},{l:'HD Machines',v:'1,100'},{l:'Annual Catheter Demand',v:'3,207'},{l:'Market Value',v:'$0.42M'},{l:'Distributors / KOLs',v:'10 / 10'}]},
  om:{flag:'🇴🇲',flagImg:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/oman_flag.jpeg',name:'Oman',sub:'GCC — Growing Market',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/oman_landscape.jpeg',colors:{primary:'#db161b',secondary:'#ffffff',accent:'#008000'},
    kpi:[{l:'Population 2026',v:'5,494,691'},{l:'HD Patients',v:'2,500'},{l:'PD Patients',v:'100'},{l:'Dialysis Facilities',v:'20'},{l:'HD Machines',v:'2,200'},{l:'Annual Catheter Demand',v:'6,365'},{l:'Market Value',v:'$0.76M'},{l:'Distributors / KOLs',v:'10 / 10'}]},
  bh:{flag:'🇧🇭',flagImg:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/bahraien_flag.jpeg',name:'Bahrain',sub:'GCC — Small High-Income',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/bahrain_landscape.jpg',colors:{primary:'#ce1126',secondary:'#ffffff',accent:'#ce1126'},
    kpi:[{l:'Population 2026',v:'1,675,572'},{l:'HD Patients',v:'4,547'},{l:'PD Patients',v:'450'},{l:'Dialysis Facilities',v:'14'},{l:'HD Machines',v:'750'},{l:'Annual Catheter Demand',v:'11,885'},{l:'Market Value',v:'$1.43M'},{l:'Distributors / KOLs',v:'10 / 10'}]},
  iq:{flag:'🇮🇶',flagImg:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/iraq_flag.jpg',name:'Iraq',sub:'ME — High Volume Opportunity',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/iraq_landscape.jpg',colors:{primary:'#ce1126',secondary:'#ffffff',accent:'#ffffff'},
    kpi:[{l:'Population 2026',v:'48,007,437'},{l:'HD Patients',v:'10,721'},{l:'PD Patients',v:'450'},{l:'Dialysis Facilities',v:'130'},{l:'HD Machines',v:'9,000'},{l:'Annual Catheter Demand',v:'27,320'},{l:'Market Value',v:'$2.46M'},{l:'Distributors / KOLs',v:'10 / 10'}]},
  jo:{flag:'🇯🇴',flagImg:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/jordon_flag.jpeg',name:'Jordan',sub:'ME — Medical Hub',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/jordon_landscape.jpeg',colors:{primary:'#007a3d',secondary:'#ffffff',accent:'#ce1126'},
    kpi:[{l:'Population 2026',v:'11,589,532'},{l:'HD Patients',v:'6,400'},{l:'PD Patients',v:'110'},{l:'Dialysis Facilities',v:'50'},{l:'HD Machines',v:'2,500'},{l:'Annual Catheter Demand',v:'16,127'},{l:'Market Value',v:'$1.61M'},{l:'Distributors / KOLs',v:'10 / 10'}]},
  lb:{flag:'🇱🇧',flagImg:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/lebanon_flag.jpeg',name:'Lebanon',sub:'ME — Under Renewal',
    landscape:'https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/lebanon_landscape.jpeg',colors:{primary:'#ee161f',secondary:'#ffffff',accent:'#00a650'},
    kpi:[{l:'Population 2026',v:'5,897,467'},{l:'HD Patients',v:'4,730'},{l:'PD Patients',v:'210'},{l:'Dialysis Facilities',v:'85'},{l:'HD Machines',v:'3,000'},{l:'Annual Catheter Demand',v:'12,067'},{l:'Market Value',v:'$1.21M'},{l:'Distributors / KOLs',v:'10 / 10'}]}
};

function openCountry(code){
  const d = countryData[code];
  const page = document.getElementById('page-countries');
  if(!d || !page) return;

  const old = document.getElementById('country-inline-detail');
  if(old) old.remove();

  // Apply the selected country's flag colors to the Country Analysis page.
  page.classList.add('country-theme');
  page.style.setProperty('--country-primary', d.colors.primary);
  page.style.setProperty('--country-secondary', d.colors.secondary);
  page.style.setProperty('--country-accent', d.colors.accent);

  // Make the selected country card visibly active.
  document.querySelectorAll('#page-countries .c-card').forEach(function(card){
    card.classList.toggle('active', card.getAttribute('aria-label') === d.name);
  });

  const detail = document.createElement('div');
  detail.id = 'country-inline-detail';
  detail.className = 'country-inline-detail';

  const capitalMap = {
    sa:'Riyadh', ae:'Abu Dhabi', kw:'Kuwait City', qa:'Doha', om:'Muscat',
    bh:'Manama', jo:'Amman', lb:'Beirut', iq:'Baghdad'
  };
  const systemMap = {
    sa:'MOH / NUPCO / SFDA', ae:'MOH / DHA / DOH', kw:'MOH Kuwait',
    qa:'HMC / PHCC', om:'MOH Oman', bh:'MOH Bahrain',
    jo:'MOH / RMS', lb:'MOH Lebanon', iq:'MOH / Kimadia'
  };

  const networkValue = (d.kpi[7] && d.kpi[7].v) ? d.kpi[7].v.split('/') : ['—','—'];
  const distributors = (networkValue[0] || '—').trim();
  const kols = (networkValue[1] || '—').trim();

  detail.innerHTML = `
    <div class="cid-hero">
      <img class="cid-landscape" src="${d.landscape}" alt="${d.name} landscape"
           onerror="this.style.display='none'">
      <div class="cid-overlay"></div>
      <button class="cid-back" onclick="closeCountry()">← Back</button>
      <div class="cid-title">
        <span class="cid-flag">
          <img src="${d.flagImg}" alt="${d.name} flag" onerror="this.onerror=null;this.replaceWith(document.createTextNode('${d.flag}'))">
        </span>
        <div>
          <div class="cid-name">${d.name}</div>
          <div class="cid-sub">${d.sub}</div>
        </div>
      </div>
      <div class="cid-meta">
        <div><span>📍</span><small>Capital</small><b>${capitalMap[code] || '—'}</b></div>
        <div><span>👥</span><small>Population</small><b>${d.kpi[0]?.v || '—'}</b></div>
        <div><span>🏥</span><small>Healthcare System</small><b>${systemMap[code] || '—'}</b></div>
      </div>
    </div>

    <div class="cid-body">
      <div class="cid-kpi-grid">
        ${d.kpi.slice(0,7).map(k=>`
          <div class="cid-kpi">
            <div class="cid-kpi-label">${k.l}</div>
            <div class="cid-kpi-value">${k.v}</div>
          </div>
        `).join('')}
      </div>

      <div class="cid-network">
        <div class="cid-network-card">
          <div>
            <div class="cid-network-label">🤝 Distributors</div>
            <div class="cid-network-sub">Active Partners</div>
          </div>
          <div class="cid-network-value">${distributors}</div>
        </div>
        <div class="cid-network-card">
          <div>
            <div class="cid-network-label">⭐ KOLs</div>
            <div class="cid-network-sub">Key Opinion Leaders</div>
          </div>
          <div class="cid-network-value">${kols}</div>
        </div>
      </div>
    </div>
  `;

  const header = page.querySelector('.section-header');
  const grid = page.querySelector('.country-grid');
  if(header) header.insertAdjacentElement('afterend', detail);
  else page.prepend(detail);

  if(grid) grid.scrollIntoView({behavior:'smooth', block:'start'});
  setTimeout(()=>window.scrollTo({top:0,behavior:'smooth'}),80);
}

function closeCountry(){
  const page = document.getElementById('page-countries');
  const detail = document.getElementById('country-inline-detail');
  if(detail) detail.remove();
  if(page){
    page.classList.remove('country-theme');
    page.style.removeProperty('--country-primary');
    page.style.removeProperty('--country-secondary');
    page.style.removeProperty('--country-accent');
    page.querySelectorAll('.c-card').forEach(function(card){ card.classList.remove('active'); });
  }
  const cd = document.getElementById('cd-panel');
  if(cd) cd.classList.remove('open');
}

const competitorCountries={"sa":{"flag":"🇸🇦","name":"Saudi Arabia","market":"Largest market in the workbook scope","hd":30000,"pd":2200,"facilities":360,"machines":18000,"demand":77530,"marketValue":9.3},"ae":{"flag":"🇦🇪","name":"UAE","market":"Major GCC regional hub","hd":3000,"pd":120,"facilities":60,"machines":4500,"demand":7638,"marketValue":0.99},"qa":{"flag":"🇶🇦","name":"Qatar","market":"Centralized procurement market","hd":1200,"pd":180,"facilities":18,"machines":1100,"demand":3207,"marketValue":0.42},"kw":{"flag":"🇰🇼","name":"Kuwait","market":"GCC dialysis market","hd":2156,"pd":294,"facilities":25,"machines":3000,"demand":5728,"marketValue":0.72},"om":{"flag":"🇴🇲","name":"Oman","market":"Growing GCC dialysis market","hd":2500,"pd":100,"facilities":20,"machines":2200,"demand":6365,"marketValue":0.76},"jo":{"flag":"🇯🇴","name":"Jordan","market":"Levant medical hub","hd":6400,"pd":110,"facilities":50,"machines":2500,"demand":16127,"marketValue":1.61},"lb":{"flag":"🇱🇧","name":"Lebanon","market":"Levant market under pressure","hd":4730,"pd":210,"facilities":85,"machines":3000,"demand":12067,"marketValue":1.21},"iq":{"flag":"🇮🇶","name":"Iraq","market":"High-volume expansion market","hd":10721,"pd":450,"facilities":130,"machines":9000,"demand":27320,"marketValue":2.46},"bh":{"flag":"🇧🇭","name":"Bahrain","market":"Small high-income GCC market","hd":4547,"pd":450,"facilities":14,"machines":750,"demand":11885,"marketValue":1.43}};
const competitorData={"sa":[{"name":"Fresenius Medical Care","share":"~18–20% KSA HD catheter market businesswire+2","coverage":"⭐⭐⭐⭐⭐ (Nationwide via NUPCO + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance; NUPCO framework winner","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster supply"},{"name":"B. Braun Melsungen","share":"~12–14% KSA HD catheter market businesswire+1","coverage":"⭐⭐⭐⭐⭐ (NUPCO framework + SFDA distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + Aesculap brand; NUPCO presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Medtronic (Covidien)","share":"~10–12% KSA HD catheter market grandviewresearch","coverage":"⭐⭐⭐⭐⭐ (NUPCO winner NPT0048-22, Apr 2026) scribd","weakness":"Premium pricing; peritoneal catheters stronger than HD","advantage":"Technology + clinical evidence + NUPCO tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~8–10% KSA HD catheter market grandviewresearch","coverage":"⭐⭐⭐⭐⭐ (SFDA-licensed, major NUPCO supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + GCC manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~6–8% KSA HD catheter market","coverage":"⭐⭐⭐⭐ (NUPCO participant, SFDA-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Baxter International","share":"~10–12% KSA HD catheter market businesswire+1","coverage":"⭐⭐⭐⭐⭐ (NUPCO framework, SFDA-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus","advantage":"Renal-care ecosystem (PD + HD catheters)","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility"},{"name":"Merit Medical","share":"~4–6% KSA HD catheter market","coverage":"⭐⭐⭐⭐ (SFDA-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited KSA distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow)","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + GCC credibility"},{"name":"Nipro Corporation","share":"~5–7% KSA HD catheter market grandviewresearch+1","coverage":"⭐⭐⭐⭐ (SFDA-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~2–3% KSA HD catheter market","coverage":"⭐⭐⭐ (Limited KSA distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader KSA distribution"},{"name":"Medcomp","share":"~1–2% KSA HD catheter market","coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + GCC manufacturing + regional support"}],"ae":[{"name":"BD","share":"~13.9% global","coverage":"⭐⭐⭐⭐⭐","weakness":"Premium pricing","advantage":"Brand + clinical evidence","specializes":"Vascular access / HD","edge":"Better value proposition + regional agility"},{"name":"Medtronic","share":"~15–16% global estimates","coverage":"⭐⭐⭐⭐⭐","weakness":"Large organization; less focused","advantage":"Technology + distribution","specializes":"Vascular access","edge":"Specialized HD focus + competitive price"},{"name":"Merit Medical","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller scale","advantage":"Strong dialysis-access portfolio","specializes":"Dialysis access","edge":"Price + flexible supply/customization"},{"name":"Vygon","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller global footprint","advantage":"Vascular-access specialization","specializes":"Vascular access","edge":"Regional proximity + value"},{"name":"B. Braun","share":"N/D","coverage":"⭐⭐⭐⭐⭐","weakness":"Large diversified portfolio","advantage":"Dialysis ecosystem","specializes":"Dialysis / vascular access","edge":"Focused HD catheter company"},{"name":"Teleflex/Arrow","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium positioning","advantage":"Advanced vascular access","specializes":"HD / vascular access","edge":"Cost + product flexibility"},{"name":"Baxter","share":"N/D","coverage":"⭐⭐⭐⭐⭐","weakness":"Broad renal portfolio","advantage":"Renal-care ecosystem","specializes":"Renal care","edge":"Catheter specialization"},{"name":"Advin","share":"N/D","coverage":"⭐⭐⭐","weakness":"Cost-focused competitor","advantage":"Competitive pricing","specializes":"Dialysis catheters","edge":"AMECATH can compete on quality + GCC credibility"}],"qa":[{"name":"BD","share":"~13.9% global","coverage":"⭐⭐⭐⭐⭐","weakness":"Premium cost","advantage":"Strong brand + evidence","specializes":"Vascular access","edge":"Price/value + responsiveness"},{"name":"Medtronic","share":"~15–16% global estimates","coverage":"⭐⭐⭐⭐⭐","weakness":"Large organization","advantage":"Technology + infrastructure","specializes":"Vascular access","edge":"HD specialization + flexibility"},{"name":"B. Braun","share":"N/D","coverage":"⭐⭐⭐⭐⭐","weakness":"Diversified portfolio","advantage":"Dialysis ecosystem","specializes":"Dialysis","edge":"Focused catheter portfolio"},{"name":"Merit","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller corporate scale","advantage":"Dialysis access","specializes":"HD access","edge":"Price + regional supply"},{"name":"Teleflex/Arrow","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium product positioning","advantage":"Vascular-access technology","specializes":"HD / vascular access","edge":"Competitive pricing"},{"name":"Vygon","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Less scale","advantage":"Vascular access","specializes":"Vascular access","edge":"Regional flexibility"},{"name":"Baxter","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Broad renal portfolio","advantage":"Renal ecosystem","specializes":"Renal care","edge":"Catheter specialization"},{"name":"Cook","share":"N/D","coverage":"⭐⭐⭐","weakness":"Broad interventional portfolio","advantage":"Interventional technology","specializes":"Vascular/interventional","edge":"HD-focused proposition"}],"kw":[{"name":"BD","share":"~13.9% global","coverage":"⭐⭐⭐⭐⭐","weakness":"Premium","advantage":"Strong vascular-access brand","specializes":"Vascular access / HD","edge":"Value + pricing"},{"name":"Medtronic","share":"~15–16% global estimates","coverage":"⭐⭐⭐⭐⭐","weakness":"Large organization","advantage":"Global infrastructure","specializes":"Vascular access","edge":"Agility + HD focus"},{"name":"Merit","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller network","advantage":"Strong dialysis portfolio","specializes":"Dialysis access","edge":"Cost + regional supply"},{"name":"B. Braun","share":"N/D","coverage":"⭐⭐⭐⭐⭐","weakness":"Diversified","advantage":"Integrated dialysis offering","specializes":"Dialysis / vascular access","edge":"Specialization + price"},{"name":"Teleflex","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium","advantage":"Arrow technology","specializes":"HD access","edge":"Cost-effective alternative"},{"name":"Vygon","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller global footprint","advantage":"Vascular access","specializes":"Vascular access","edge":"Regional responsiveness"},{"name":"Nipro","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Strong dialysis ecosystem can compete broadly","advantage":"Dialysis","specializes":"Dialysis products","edge":"Catheter specialization"},{"name":"Cook","share":"N/D","coverage":"⭐⭐⭐","weakness":"Broad portfolio","advantage":"Interventional","specializes":"Vascular","edge":"HD specialization"}],"om":[{"name":"BD","share":"~13.9% global","coverage":"⭐⭐⭐⭐⭐","weakness":"Premium","advantage":"Brand + clinical validation","specializes":"Vascular access","edge":"Price/value"},{"name":"Medtronic","share":"~15–16% global estimates","coverage":"⭐⭐⭐⭐⭐","weakness":"Large corporate structure","advantage":"Technology","specializes":"Vascular access","edge":"Agility + HD specialization"},{"name":"B. Braun","share":"N/D","coverage":"⭐⭐⭐⭐⭐","weakness":"Broad portfolio","advantage":"Dialysis ecosystem","specializes":"Dialysis","edge":"Focused catheter portfolio"},{"name":"Merit","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller scale","advantage":"Dialysis access","specializes":"HD access","edge":"Cost + supply flexibility"},{"name":"Teleflex","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium","advantage":"Arrow technology","specializes":"HD access","edge":"Competitive price"},{"name":"Vygon","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller scale","advantage":"Vascular access","specializes":"Vascular access","edge":"Regional responsiveness"},{"name":"Baxter","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Diversified","advantage":"Renal-care ecosystem","specializes":"Renal care","edge":"Catheter specialization"},{"name":"Polymedicure","share":"N/D","coverage":"⭐⭐⭐","weakness":"Price competition","advantage":"Cost-effective medical devices","specializes":"Catheters / vascular access","edge":"Quality + regional credibility"}],"jo":[{"name":"Merit Medical","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium vs. low-cost suppliers","advantage":"Strong HD-access specialization","specializes":"Dialysis access","edge":"Price + regional manufacturing advantage"},{"name":"BD","share":"~13.9% global","coverage":"⭐⭐⭐⭐⭐","weakness":"Premium","advantage":"Brand/clinical evidence","specializes":"Vascular access","edge":"Lower cost + flexibility"},{"name":"Medtronic","share":"~15–16% global estimates","coverage":"⭐⭐⭐⭐⭐","weakness":"Large organization","advantage":"Technology","specializes":"Vascular access","edge":"HD focus"},{"name":"B. Braun","share":"N/D","coverage":"⭐⭐⭐⭐⭐","weakness":"Diversified","advantage":"Dialysis ecosystem","specializes":"Dialysis","edge":"Specialized catheter proposition"},{"name":"Teleflex","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium","advantage":"Arrow technology","specializes":"Vascular/HD","edge":"Value pricing"},{"name":"Vygon","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller scale","advantage":"Vascular access","specializes":"Vascular access","edge":"Regional flexibility"},{"name":"Polymedicure","share":"N/D","coverage":"⭐⭐⭐","weakness":"Price-driven","advantage":"Cost competitiveness","specializes":"Catheters","edge":"Quality + Middle East positioning"},{"name":"Medcomp","share":"N/D","coverage":"⭐⭐⭐","weakness":"Less broad brand presence","advantage":"Dialysis access","specializes":"HD catheters","edge":"Regional reach + value"}],"lb":[{"name":"BD","share":"~13.9% global","coverage":"⭐⭐⭐⭐⭐","weakness":"Premium","advantage":"Strong brand","specializes":"Vascular access","edge":"Price/value"},{"name":"Medtronic","share":"~15–16% global estimates","coverage":"⭐⭐⭐⭐⭐","weakness":"Large organization","advantage":"Technology","specializes":"Vascular access","edge":"Specialized HD focus"},{"name":"B. Braun","share":"N/D","coverage":"⭐⭐⭐⭐⭐","weakness":"Diversified","advantage":"Dialysis ecosystem","specializes":"Dialysis","edge":"Focused portfolio"},{"name":"Merit","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium","advantage":"Dialysis access","specializes":"HD access","edge":"Price + regional responsiveness"},{"name":"Teleflex","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium","advantage":"Arrow technology","specializes":"HD/vascular","edge":"Value proposition"},{"name":"Vygon","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Scale","advantage":"Vascular access","specializes":"Vascular","edge":"Flexibility"},{"name":"Baxter","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Diversified","advantage":"Renal ecosystem","specializes":"Renal care","edge":"Catheter specialization"},{"name":"Polymedicure","share":"N/D","coverage":"⭐⭐⭐","weakness":"Price-oriented","advantage":"Cost","specializes":"Catheters","edge":"Quality + regional positioning"}],"iq":[{"name":"Medtronic","share":"~15–16% global estimates","coverage":"⭐⭐⭐⭐","weakness":"Premium cost","advantage":"Brand + technology","specializes":"Vascular access","edge":"Much stronger price/value argument"},{"name":"BD","share":"~13.9% global","coverage":"⭐⭐⭐⭐","weakness":"Premium","advantage":"Clinical reputation","specializes":"Vascular access","edge":"Lower-cost alternative"},{"name":"B. Braun","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium / diversified","advantage":"Dialysis ecosystem","specializes":"Dialysis","edge":"Price + HD specialization"},{"name":"Baxter","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Diversified","advantage":"Renal-care ecosystem","specializes":"Renal care","edge":"Catheter specialization"},{"name":"Merit","share":"N/D","coverage":"⭐⭐⭐","weakness":"Premium","advantage":"Dialysis access","specializes":"HD access","edge":"Price + regional proximity"},{"name":"Teleflex","share":"N/D","coverage":"⭐⭐⭐","weakness":"Premium","advantage":"Arrow technology","specializes":"Vascular access","edge":"Cost advantage"},{"name":"Vygon","share":"N/D","coverage":"⭐⭐⭐","weakness":"Distribution dependence","advantage":"Vascular access","specializes":"Vascular access","edge":"Regional supply flexibility"},{"name":"Polymedicure","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Less premium brand perception","advantage":"Cost competitiveness","specializes":"Catheters","edge":"Quality + regional reputation"},{"name":"Advin","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller global brand","advantage":"Low-cost products","specializes":"Dialysis catheters","edge":"Quality + GCC/MENA positioning"},{"name":"Chinese manufacturers","share":"N/D","coverage":"⭐⭐⭐","weakness":"Variable clinical/brand perception","advantage":"Very low price","specializes":"Medical disposables/catheters","edge":"Better quality/clinical positioning at competitive price"}],"bh":[{"name":"BD","share":"~13.9% global","coverage":"⭐⭐⭐⭐⭐","weakness":"Premium","advantage":"Brand + vascular access","specializes":"Vascular access","edge":"Value + price"},{"name":"Medtronic","share":"~15–16% global estimates","coverage":"⭐⭐⭐⭐⭐","weakness":"Large organization","advantage":"Technology + distribution","specializes":"Vascular access","edge":"Agility + specialization"},{"name":"B. Braun","share":"N/D","coverage":"⭐⭐⭐⭐⭐","weakness":"Diversified","advantage":"Dialysis ecosystem","specializes":"Dialysis","edge":"Focused HD-catheter company"},{"name":"Merit","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller scale","advantage":"Dialysis access","specializes":"HD access","edge":"Cost + supply"},{"name":"Teleflex","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Premium","advantage":"Arrow","specializes":"HD/vascular","edge":"Competitive pricing"},{"name":"Vygon","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Smaller scale","advantage":"Vascular access","specializes":"Vascular","edge":"Regional flexibility"},{"name":"Baxter","share":"N/D","coverage":"⭐⭐⭐⭐","weakness":"Broad renal portfolio","advantage":"Renal care","specializes":"Renal care","edge":"HD catheter specialization"},{"name":"Cook","share":"N/D","coverage":"⭐⭐⭐","weakness":"Broad interventional","advantage":"Interventional","specializes":"Vascular","edge":"HD focus"}]};
let selectedCompetitorCountry='sa';
function renderCompetitors(){const country=competitorCountries[selectedCompetitorCountry],header=document.getElementById('competitor-country-header'),grid=document.getElementById('comp-grid');if(!header||!grid)return;const list=competitorData[selectedCompetitorCountry]||[];header.innerHTML=`<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3"><div><div class="comp-country-title">${country.flag} ${country.name}</div><div class="comp-country-sub">${country.market} · Source: Competitor_Matrix</div></div><div class="comp-summary"><div class="comp-summary-pill">🏢 ${list.length} Competitors</div><div class="comp-summary-pill">👥 HD ${country.hd.toLocaleString()}</div><div class="comp-summary-pill">💉 Demand ${country.demand.toLocaleString()}</div><div class="comp-summary-pill">💰 Market $${country.marketValue}M</div></div></div>`;grid.innerHTML=list.map((c,i)=>{const id='comp-detail-'+selectedCompetitorCountry+'-'+i;return `<div class="comp-card-new"><div class="comp-card-topline" style="background:#3b82f6;"></div><div class="flex justify-between items-start gap-3"><div><div class="comp-card-company">${c.name}</div><div class="comp-card-origin">${c.coverage}</div></div><span class="comp-threat-badge" style="background:rgba(59,130,246,.12);color:#60a5fa;border:1px solid rgba(59,130,246,.3);">${c.share}</span></div><div class="comp-share-row"><span>Market Share*</span><span class="comp-share-value">${c.share}</span></div><div class="comp-mini-grid"><div class="comp-mini-box"><span class="comp-mini-label">Main Advantage</span><span class="comp-mini-text">${c.advantage}</span></div><div class="comp-mini-box"><span class="comp-mini-label">Weakness / Gap</span><span class="comp-mini-text">${c.weakness}</span></div></div><div class="comp-edge"><b>Specializes in:</b> ${c.specializes}</div><button class="comp-details-btn" onclick="toggleCompetitorDetails('${id}',this)">View Details ↓</button><div class="comp-details-panel" id="${id}"><div class="comp-detail-row"><span class="comp-detail-label">Company</span><span class="comp-detail-value">${c.name}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Market Share*</span><span class="comp-detail-value">${c.share}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Coverage</span><span class="comp-detail-value">${c.coverage}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Main Advantage</span><span class="comp-detail-value">${c.advantage}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Specializes in</span><span class="comp-detail-value">${c.specializes}</span></div><div style="margin-top:8px;color:#34d399;font-size:10px;line-height:1.45;"><b>AMECATH Competitive Advantage:</b> ${c.edge}</div></div></div>`;}).join('')||'<div class="placeholder-page">No competitor data available for this country.</div>'; }
function setCompetitorCountry(id,btn){selectedCompetitorCountry=id;document.querySelectorAll('.country-filter-btn').forEach(b=>b.classList.remove('comp-country-active'));if(btn)btn.classList.add('comp-country-active');renderCompetitors();}
function toggleCompetitorDetails(id,btn){const panel=document.getElementById(id);if(!panel)return;const open=panel.classList.toggle('open');btn.textContent=open?'Hide Details ↑':'View Details ↓';}
function filterCompetitors(type,btn){setCompetitorThreat(type,btn);}
function toggleDetails(btn){const panel=btn.closest('.comp-card-new')?.querySelector('.comp-details-panel');if(!panel)return;const open=panel.classList.toggle('open');btn.textContent=open?'Hide Details ↑':'View Details ↓';}
renderCompetitors();

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
  if(pageId !== 'countries') closeCountry();
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  if(el) el.classList.add('active');
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  page.classList.add('active');
  if(pageId==="hotareas"){setTimeout(()=>{createMarketMap();if(marketMap)marketMap.invalidateSize();},200);}
}

// Robust navigation: use real event listeners instead of inline onclick handlers.
window.navigate = navigate;
window.openCountry = openCountry;
window.closeCountry = closeCountry;

document.querySelectorAll('.nav-item[data-page]').forEach(function(item){
  const go=function(){ navigate(item,item.getAttribute('data-page')); };
  item.addEventListener('click',go);
  item.addEventListener('keydown',function(e){
    if(e.key==='Enter' || e.key===' '){ e.preventDefault(); go(); }
  });
});
/* ─── TENDERS ─── */
(function () {
  var tndrData = [
    {id:1,  name:'National HD Catheter Supply 2026–2027',      country:'Saudi Arabia', display:'🇸🇦 Saudi Arabia', authority:'NUPCO / SFDA',       value:'$820,000', deadline:'30 Sep 2026', status:'Open',      notes:'Active national procurement. Monitor tender clarifications, submission requirements, and award timeline via NUPCO Etimad portal.'},
    {id:2,  name:'Hemodialysis Access Devices Framework',       country:'Saudi Arabia', display:'🇸🇦 Saudi Arabia', authority:'MOH KSA',             value:'$540,000', deadline:'15 Oct 2026', status:'Open',      notes:'Framework opportunity for HD access devices. Review commercial and technical requirements before final submission.'},
    {id:3,  name:'Kimadia HD Catheter Bulk Order Q4 2026',      country:'Iraq',         display:'🇮🇶 Iraq',         authority:'Kimadia (MOH Iraq)',  value:'$610,000', deadline:'20 Oct 2026', status:'Open',      notes:'Q4 bulk procurement via Kimadia. Confirm product registration, delivery requirements, and quantities.'},
    {id:4,  name:'RMS HD Catheter Annual Contract',             country:'Jordan',       display:'🇯🇴 Jordan',       authority:'Royal Medical Serv.', value:'$280,000', deadline:'05 Nov 2026', status:'Submitted', notes:'Submission completed. Pending evaluation and award decision by Royal Medical Services.'},
    {id:5,  name:'MOH Jordan Dialysis Consumables 2027',        country:'Jordan',       display:'🇯🇴 Jordan',       authority:'MOH Jordan',          value:'$195,000', deadline:'12 Nov 2026', status:'Submitted', notes:'Submitted. Track evaluation progress and any requests for clarification from MOH Jordan.'},
    {id:6,  name:'MOH Lebanon Hospital Catheter Supply',        country:'Lebanon',      display:'🇱🇧 Lebanon',      authority:'MOH Lebanon',         value:'$145,000', deadline:'18 Nov 2026', status:'Open',      notes:'Validate local procurement documentation and ensure technical files are complete before deadline.'},
    {id:7,  name:'BDF / RMS Bahrain HD Catheter 2027',          country:'Bahrain',      display:'🇧🇭 Bahrain',      authority:'BDF Hospital / RMS', value:'$210,000', deadline:'25 Nov 2026', status:'Submitted', notes:'Submitted to BDF/RMS. Awaiting evaluation and award communication from Bahrain procurement team.'},
    {id:8,  name:'MOH Oman Vascular Access Framework',          country:'Oman',         display:'🇴🇲 Oman',         authority:'MOH Oman Central',   value:'$320,000', deadline:'01 Dec 2026', status:'Submitted', notes:'Framework submission pending award. Maintain follow-up with central procurement team.'},
    {id:9,  name:'DHA Dubai HD Catheter Framework 2027',        country:'UAE',          display:'🇦🇪 UAE',          authority:'DHA Dubai',           value:'$175,000', deadline:'10 Dec 2026', status:'Submitted', notes:'Submitted to DHA Dubai for evaluation. Monitor award status and technical clarification requests.'},
    {id:10, name:'HMC Qatar Catheter Annual Contract',          country:'Qatar',        display:'🇶🇦 Qatar',        authority:'HMC Qatar',           value:'$130,000', deadline:'15 Dec 2026', status:'Submitted', notes:'Annual contract submitted to HMC. Follow procurement updates through evaluation and award process.'},
    {id:11, name:'MOH Kuwait Dialysis Access 2027',             country:'Kuwait',       display:'🇰🇼 Kuwait',       authority:'MOH Kuwait Central', value:'$185,000', deadline:'20 Dec 2026', status:'Open',      notes:'Open 2027 dialysis access procurement. Prepare technical and commercial documentation before closing date.'},
    {id:12, name:'NUPCO KSA Emergency HD Catheter Lot',         country:'Saudi Arabia', display:'🇸🇦 Saudi Arabia', authority:'NUPCO',               value:'$390,000', deadline:'31 Dec 2026', status:'Won',       notes:'Awarded. Coordinate order execution, delivery planning, and post-award documentation with NUPCO.'},
    {id:13, name:'MOH Iraq Regional HD Catheter Supply',        country:'Iraq',         display:'🇮🇶 Iraq',         authority:'MOH Iraq Regional',  value:'$165,000', deadline:'10 Jan 2027', status:'Won',       notes:'Won. Proceed with contracting, fulfillment planning, and required delivery documentation.'},
    {id:14, name:'Kimadia Framework Extension 2027',            country:'Iraq',         display:'🇮🇶 Iraq',         authority:'Kimadia (MOH Iraq)', value:'$245,000', deadline:'28 Feb 2027', status:'Won',       notes:'Framework extension awarded. Coordinate documentation, forecasted quantities, and implementation schedule.'}
  ];

  var tndrCountryFilter = 'all';
  var tndrStatusFilter  = 'all';

  function tndrStatusClass(s) {
    if (s === 'Open')      return 'tndr-status-open';
    if (s === 'Submitted') return 'tndr-status-submitted';
    if (s === 'Won')       return 'tndr-status-won';
    return 'tndr-status-closed';
  }
  function tndrStatusLabel(s) { return s === 'Won' ? 'Won ✅' : s; }

  function tndrRender() {
    var tbody = document.getElementById('tndr-table-body');
    if (!tbody) return;
    var filtered = tndrData.filter(function(r) {
      return (tndrCountryFilter === 'all' || r.country === tndrCountryFilter) &&
             (tndrStatusFilter  === 'all' || r.status  === tndrStatusFilter);
    });
    if (!filtered.length) {
      tbody.innerHTML = '<tr><td colspan="8" class="tndr-empty">No tenders match the selected filters.</td></tr>';
      return;
    }
    var html = '';
    filtered.forEach(function(r) {
      var sc = tndrStatusClass(r.status);
      var sl = tndrStatusLabel(r.status);
      html += '<tr>' +
        '<td class="tndr-number">' + r.id + '</td>' +
        '<td class="tndr-name">' + r.name + '</td>' +
        '<td class="tndr-country">' + r.display + '</td>' +
        '<td class="tndr-authority" style="color:#8fa8cf;">' + r.authority + '</td>' +
        '<td class="tndr-value">' + r.value + '</td>' +
        '<td class="tndr-deadline" style="color:#b8c7dd;">' + r.deadline + '</td>' +
        '<td><span class="tndr-status ' + sc + '">' + sl + '</span></td>' +
        '<td><button class="tndr-view-btn" onclick="tndrOpenModal(' + r.id + ')">View</button></td>' +
      '</tr>';
    });
    /* Total row */
    html += '<tr>' +
      '<td colspan="4" style="padding:13px 14px;background:#10264a;color:#6a85b0;font-size:11px;font-weight:700;text-align:right;border-top:1px solid #1e3d7a;">TOTAL PIPELINE VALUE</td>' +
      '<td style="padding:13px 14px;background:#10264a;color:#60a5fa;font-size:14px;font-weight:800;border-top:1px solid #1e3d7a;">$4,210,000</td>' +
      '<td colspan="3" style="background:#10264a;border-top:1px solid #1e3d7a;"></td>' +
    '</tr>';
    tbody.innerHTML = html;
  }

  window.tndrOpenModal = function(id) {
    var r = tndrData.find(function(x){ return x.id === id; });
    if (!r) return;
    document.getElementById('tndr-modal-title').textContent = r.name;
    document.getElementById('tndr-d-name').textContent      = r.name;
    document.getElementById('tndr-d-country').textContent   = r.display;
    document.getElementById('tndr-d-authority').textContent = r.authority;
    document.getElementById('tndr-d-value').textContent     = r.value;
    document.getElementById('tndr-d-deadline').textContent  = r.deadline;
    document.getElementById('tndr-d-status').innerHTML =
      '<span class="tndr-status ' + tndrStatusClass(r.status) + '">' + tndrStatusLabel(r.status) + '</span>';
    document.getElementById('tndr-d-notes').textContent = r.notes;
    document.getElementById('tndr-modal').classList.add('show');
  };

  function tndrCloseModal() {
    var m = document.getElementById('tndr-modal');
    if (m) m.classList.remove('show');
  }

  function tndrSetCountry(val) {
    tndrCountryFilter = val;
    document.querySelectorAll('[data-tndr-country]').forEach(function(b) {
      b.classList.toggle('active', b.getAttribute('data-tndr-country') === val);
    });
    tndrRender();
  }

  function tndrSetStatus(val) {
    tndrStatusFilter = val;
    document.querySelectorAll('[data-tndr-status]').forEach(function(b) {
      b.classList.toggle('active', b.getAttribute('data-tndr-status') === val);
    });
    tndrRender();
  }

  document.querySelectorAll('[data-tndr-country]').forEach(function(b) {
    b.addEventListener('click', function() { tndrSetCountry(b.getAttribute('data-tndr-country')); });
  });
  document.querySelectorAll('[data-tndr-status]').forEach(function(b) {
    b.addEventListener('click', function() { tndrSetStatus(b.getAttribute('data-tndr-status')); });
  });

  var mx = document.getElementById('tndr-modal-x');
  var mc = document.getElementById('tndr-modal-close');
  var mo = document.getElementById('tndr-modal');
  if (mx) mx.addEventListener('click', tndrCloseModal);
  if (mc) mc.addEventListener('click', tndrCloseModal);
  if (mo) mo.addEventListener('click', function(e) { if (e.target === mo) tndrCloseModal(); });
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape') tndrCloseModal(); });

      tndrRender();

  /* ─── TAB SWITCHER ─── */
  window.tndrSwitchTab = function(tab) {
    var isActive = tab === 'active';
    var sa = document.getElementById('tndr-section-active');
    var sp = document.getElementById('tndr-section-pipeline');
    var ta = document.getElementById('tndr-tab-active');
    var tp = document.getElementById('tndr-tab-pipeline');
    if (sa) sa.style.display = isActive ? '' : 'none';
    if (sp) sp.style.display = isActive ? 'none' : '';
    if (ta) { ta.style.background = isActive ? '#2563eb' : 'transparent'; ta.style.color = isActive ? '#fff' : '#6a85b0'; }
    if (tp) { tp.style.background = isActive ? 'transparent' : '#2563eb'; tp.style.color = isActive ? '#6a85b0' : '#fff'; }
  };

})();
/* ─── END TENDERS ─── */

/* ─── PIPELINE FORECAST ─── */
(function() {
  var pipeData = [
    {id:1,  country:'🇸🇦 Saudi Arabia', name:'Open Framework – Dialysis & Artificial Kidney Supplies (Re-tender / Phase 2)', ref:'NPT0043/26-1 (est.)', entity:'NUPCO',                     launch:'Oct–Dec 2026',        closing:'Jan–Mar 2027',      value:'$3M–$8M',     priority:'Critical', notes:'NUPCO dialysis framework expired Aug 2026; re-tender expected Q4 2026. Localization (MiS) scoring critical.'},
    {id:2,  country:'🇸🇦 Saudi Arabia', name:'General Medical Supplies – INUPCO Platform',                                    ref:'NDP0807/26 series',   entity:'NUPCO (INUPCO)',             launch:'Rolling Sep–Dec 2026', closing:'Rolling',           value:'$50K–$200K',  priority:'High',     notes:'INUPCO e-marketplace tenders published weekly; catheters included in general medical supplies.'},
    {id:3,  country:'🇸🇦 Saudi Arabia', name:'Medical Devices – Direct Purchase (Health Clusters)',                           ref:'NDP series',          entity:'NUPCO / Health Clusters',    launch:'Rolling',             closing:'Rolling',           value:'$100K–$500K', priority:'High',     notes:'Cluster-specific tenders (Riyadh, Jazan, Makkah); catheters possible.'},
    {id:4,  country:'🇶🇦 Qatar',        name:'Medical Consumables – HMC Annual Framework',                                    ref:'HMC/TCS/9XXX/2027',   entity:'Hamad Medical Corp',         launch:'Jan–Mar 2027',        closing:'Mar–May 2027',      value:'$1M–$3M',     priority:'Critical', notes:'HMC issues annual consumables frameworks; dialysis catheters typically included.'},
    {id:5,  country:'🇶🇦 Qatar',        name:'Medical Supplies – MOH Qatar (Monaqasat)',                                      ref:'Various',             entity:'MOH Qatar',                  launch:'Q1 2027',             closing:'Q2 2027',           value:'$300K–$800K', priority:'High',     notes:'MOH Qatar tenders via Monaqasat portal; dialysis items periodic.'},
    {id:6,  country:'🇦🇪 UAE',          name:'Medical Consumables – DAHC 5-Year Blanket Renewal',                            ref:'IPR 126XXXXX',        entity:'Dubai Academic Health Corp', launch:'Q1–Q2 2027',          closing:'Q2–Q3 2027',        value:'$2M–$5M',     priority:'Critical', notes:'DAHC renews 5-year blankets annually; dialysis catheters in medical consumables category.'},
    {id:7,  country:'🇦🇪 UAE',          name:'Hemodialysis Machines & Consumables – SEHA',                                   ref:'Various',             entity:'SEHA / Abu Dhabi Health',    launch:'Q2 2027',             closing:'Q3 2027',           value:'$800K–$2M',   priority:'High',     notes:'SEHA tenders for HD machines + consumables; catheters included.'},
    {id:8,  country:'🇴🇲 Oman',         name:'Renal Dialysis Consumables – MOH Oman (Annual)',                               ref:'Various',             entity:'MOH Oman',                   launch:'Q1 2027',             closing:'Q2 2027',           value:'$600K–$1.5M', priority:'Critical', notes:'Oman MOH issues annual dialysis consumables tenders; re-tender common.'},
    {id:9,  country:'🇴🇲 Oman',         name:'Medical Equipment for Dialysis Centers – MOH Oman',                            ref:'Various',             entity:'MOH Oman',                   launch:'Q2 2027',             closing:'Q3 2027',           value:'$400K–$1M',   priority:'High',     notes:'New dialysis center equipment + consumables.'},
    {id:10, country:'🇰🇼 Kuwait',       name:'Dialysis Consumables & Equipment – MOH Kuwait (Annual)',                       ref:'Various',             entity:'MOH Kuwait',                 launch:'Q1 2027',             closing:'Q2 2027',           value:'$500K–$1.5M', priority:'Critical', notes:'Kuwait MOH annual dialysis tender; listed on GCC aggregators.'},
    {id:11, country:'🇯🇴 Jordan',       name:'Peritoneal Dialysis Consumables & Solutions (Annual)',                         ref:'Various',             entity:'MOH Jordan',                 launch:'Q1 2027',             closing:'Q2 2027',           value:'$200K–$500K', priority:'High',     notes:'Annual PD consumables tender; solutions + catheters.'},
    {id:12, country:'🇯🇴 Jordan',       name:'Dialysis Machines & Consumables – Public Hospitals',                           ref:'Various',             entity:'MOH Jordan',                 launch:'Q2 2027',             closing:'Q3 2027',           value:'$400K–$900K', priority:'High',     notes:'HD machines + consumables for public hospitals.'},
    {id:13, country:'🇱🇧 Lebanon',      name:'Permanent & Single-Use Catheters (Annual)',                                    ref:'Various',             entity:'MOH / Public Hospitals',     launch:'Q1 2027',             closing:'Q2 2027',           value:'$150K–$400K', priority:'Critical', notes:'Annual catheter tender; permanent + single-use.'},
    {id:14, country:'🇮🇶 Iraq',         name:'CVC & Dialysis Catheters – Kimadia Framework',                                 ref:'Various',             entity:'Kimadia / MOH Iraq',         launch:'Rolling Q4 2026',     closing:'Rolling',           value:'$1M–$3M',     priority:'Critical', notes:'Kimadia issues rolling CVC/dialysis catheter tenders; high-volume public procurement.'},
    {id:15, country:'🇧🇭 Bahrain',      name:'Supply of Dialysis Items (AKU & PDU) – Renewal',                              ref:'MOH/XXX/2027',        entity:'MOH Bahrain',                launch:'Q1 2027',             closing:'Q2 2027',           value:'$300K–$700K', priority:'Critical', notes:'Annual dialysis consumables for government centers.'},
    {id:16, country:'🇸🇦 Saudi Arabia', name:'NUPCO – Specialized Surgery Supplies (incl. catheters)',                       ref:'NPT0016/26 series',   entity:'NUPCO',                      launch:'Oct 2026',            closing:'06 Oct 2026',       value:'$500K–$1.5M', priority:'Medium',   notes:'Open framework for surgical sutures, laparoscopy; central venous catheters may be included.'},
    {id:17, country:'🇸🇦 Saudi Arabia', name:'NUPCO – General Nursing & Wound Care Supplies',                                ref:'NPT series',          entity:'NUPCO',                      launch:'Sep–Dec 2026',        closing:'Oct 2026–Jan 2027', value:'$300K–$800K', priority:'Medium',   notes:'General nursing/wound care; dialysis catheters possible but not primary.'},
    {id:18, country:'🇶🇦 Qatar',        name:'Medical Consumables – Quotation Invited (HMC)',                                ref:'HMC/TCS/9XXX/2026',   entity:'Hamad Medical Corp',         launch:'Sep–Dec 2026',        closing:'Oct 2026–Jan 2027', value:'$200K–$600K', priority:'High',     notes:'HMC issues periodic quotation invites for consumables; catheters likely.'},
    {id:19, country:'🇦🇪 UAE',          name:'Pharmaceutical & Medical Items – DAHC (Rolling RFQ)',                          ref:'IPR 126XXXXX',        entity:'Dubai Academic Health Corp', launch:'Rolling',             closing:'Rolling',           value:'$100K–$400K', priority:'Medium',   notes:'DAHC issues rolling RFQs for pharmaceutical/medical items; catheters possible.'},
    {id:20, country:'🇴🇲 Oman',         name:'Medical Devices – Governorate-Specific Medical Store',                         ref:'Various',             entity:'MOH Oman',                   launch:'Q4 2026',             closing:'Q1 2027',           value:'$200K–$600K', priority:'Medium',   notes:'Governorate-specific medical device tenders; dialysis items periodic.'}
  ];

  var pipeCountryFilter  = 'all';
  var pipePriorityFilter = 'all';

  var pipeStyles = {
    'Critical': {dot:'#ef4444', bg:'rgba(239,68,68,0.12)',  border:'rgba(239,68,68,0.35)',  icon:'🔴'},
    'High':     {dot:'#f97316', bg:'rgba(249,115,22,0.12)', border:'rgba(249,115,22,0.35)', icon:'🟠'},
    'Medium':   {dot:'#eab308', bg:'rgba(234,179,8,0.12)',  border:'rgba(234,179,8,0.35)',  icon:'🟡'}
  };

  function pipeRender() {
    var tbody = document.getElementById('pipe-table-body');
    if (!tbody) return;
    var filtered = pipeData.filter(function(r) {
      return (pipeCountryFilter  === 'all' || r.country  === pipeCountryFilter) &&
             (pipePriorityFilter === 'all' || r.priority === pipePriorityFilter);
    });
    if (!filtered.length) {
      tbody.innerHTML = '<tr><td colspan="9" class="tndr-empty">No pipeline tenders match the selected filters.</td></tr>';
      return;
    }
    var html = '';
    filtered.forEach(function(r) {
      var ps = pipeStyles[r.priority] || pipeStyles['Medium'];
      html += '<tr>' +
        '<td class="tndr-number">' + r.id + '</td>' +
        '<td class="tndr-name" style="min-width:260px;" title="' + r.notes + '">' + r.name + '</td>' +
        '<td class="tndr-country">' + r.country + '</td>' +
        '<td style="color:#8fa8cf;font-size:11px;min-width:160px;">' + r.entity + '</td>' +
        '<td style="color:#6a85b0;font-size:10px;white-space:nowrap;">' + r.ref + '</td>' +
        '<td style="color:#b8c7dd;white-space:nowrap;font-size:11px;">' + r.launch + '</td>' +
        '<td style="color:#b8c7dd;white-space:nowrap;font-size:11px;">' + r.closing + '</td>' +
        '<td style="color:#60a5fa;font-weight:700;white-space:nowrap;">' + r.value + '</td>' +
        '<td><span style="display:inline-flex;align-items:center;gap:4px;padding:4px 8px;border-radius:999px;font-size:10px;font-weight:700;background:' + ps.bg + ';color:' + ps.dot + ';border:1px solid ' + ps.border + ';">' + ps.icon + ' ' + r.priority + '</span></td>' +
      '</tr>';
    });
    tbody.innerHTML = html;
  }

  document.querySelectorAll('[data-pipe-country]').forEach(function(b) {
    b.addEventListener('click', function() {
      pipeCountryFilter = b.getAttribute('data-pipe-country');
      document.querySelectorAll('[data-pipe-country]').forEach(function(x) { x.classList.toggle('active', x === b); });
      pipeRender();
    });
  });

  document.querySelectorAll('[data-pipe-priority]').forEach(function(b) {
    b.addEventListener('click', function() {
      pipePriorityFilter = b.getAttribute('data-pipe-priority');
      document.querySelectorAll('[data-pipe-priority]').forEach(function(x) { x.classList.toggle('active', x === b); });
      pipeRender();
    });
  });

  pipeRender();
})();
/* ─── END PIPELINE ─── */
</script>
</body>
</html>
"""
components.html(dashboard_html, height=1080, scrolling=True)
