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
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
.hot-map {
  margin: 0 16px 16px;
  height: 520px;
  border: 1px solid #1e3d7a;
  border-radius: 14px;
  overflow: hidden;
  background: #081321;
}

#market-map {
  width: 100%;
  height: 100%;
}

.leaflet-container {
  background: #081321;
  font-family: 'Segoe UI', system-ui, sans-serif;
}

.map-popup {
  min-width: 180px;
  color: #111827;
}

.map-popup-title {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 6px;
}

.map-popup-row {
  font-size: 11px;
  margin: 3px 0;
}
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

  <div class="section-header">
    <span style="font-size:16px">📍</span>
    <span class="section-title">Hot Areas — Dialysis Market</span>
  </div>

  <div class="hot-map">
    <div id="market-map"></div>
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
      <style>
        .reg-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 10px;
          margin: 0 16px 16px;
        }
        .reg-table-container {
          margin: 0 16px 16px;
          background: #0f1f3d;
          border: 1px solid #1e3d7a;
          border-radius: 12px;
          overflow: hidden;
        }
        .reg-table {
          width: 100%;
          border-collapse: collapse;
          text-align: left;
          font-size: 12px;
        }
        .reg-table th {
          background: #070f1f;
          color: #6a85b0;
          padding: 12px 16px;
          font-size: 10px;
          text-transform: uppercase;
          letter-spacing: 1px;
          border-bottom: 1px solid #1e3d7a;
        }
        .reg-table td {
          padding: 12px 16px;
          color: #e8edf5;
          border-bottom: 1px solid #14284b;
        }
        .reg-table tr:last-child td {
          border-bottom: none;
        }
        .reg-table tr:hover {
          background: #13274c;
        }
        .badge {
          display: inline-block;
          padding: 3px 8px;
          border-radius: 6px;
          font-size: 10px;
          font-weight: 600;
        }
        .badge-approved { background: rgba(52, 211, 153, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }
        .badge-pending  { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
      </style>

      <div class="section-header">
        <span style="font-size:16px">📜</span>
        <span class="section-title">Regulatory & Registration Overview</span>
      </div>

      <!-- Regulatory KPI Summary -->
      <div class="reg-grid">
        <div class="kpi-card">
          <div class="kpi-icon">✅</div>
          <div class="kpi-label">Active Registrations</div>
          <div class="kpi-value green">7</div>
          <div class="kpi-sub green">GCC & ME Markets</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">⏳</div>
          <div class="kpi-label">Pending / Renewal</div>
          <div class="kpi-value gold">2</div>
          <div class="kpi-sub amber">In Progress</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">🛡️</div>
          <div class="kpi-label">Core Compliance</div>
          <div class="kpi-value accent">CE / ISO</div>
          <div class="kpi-sub muted">ISO 13485 Certified</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">📄</div>
          <div class="kpi-label">Key Requirement</div>
          <div class="kpi-value">FSC</div>
          <div class="kpi-sub muted">Free Sale Certificate</div>
        </div>
      </div>

      <!-- Regulatory Status Table -->
      <div class="reg-table-container">
        <table class="reg-table">
          <thead>
            <tr>
              <th>Country / Market</th>
              <th>Health Authority</th>
              <th>Registration Status</th>
              <th>Key Requirements & Notes</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>🇸🇦 Saudi Arabia</b></td>
              <td>SFDA (Saudi FDA)</td>
              <td><span class="badge badge-approved">Approved</span></td>
              <td>Medical Device National Registry (MDNR) & CE Mark</td>
            </tr>
            <tr>
              <td><b>🇦🇪 UAE</b></td>
              <td>MOHAP</td>
              <td><span class="badge badge-approved">Approved</span></td>
              <td>Classification & Free Sale Certificate (FSC)</td>
            </tr>
            <tr>
              <td><b>🇰🇼 Kuwait</b></td>
              <td>MOH Kuwait</td>
              <td><span class="badge badge-approved">Approved</span></td>
              <td>Local Agent Registration + ISO 13485</td>
            </tr>
            <tr>
              <td><b>🇶🇦 Qatar</b></td>
              <td>MOPH Qatar</td>
              <td><span class="badge badge-approved">Approved</span></td>
              <td>MOPH Registration & Product Dossier</td>
            </tr>
            <tr>
              <td><b>🇴🇲 Oman</b></td>
              <td>MOH Oman</td>
              <td><span class="badge badge-approved">Approved</span></td>
              <td>Medical Device Department Approval</td>
            </tr>
            <tr>
              <td><b>🇧🇭 Bahrain</b></td>
              <td>NHRA</td>
              <td><span class="badge badge-approved">Approved</span></td>
              <td>NHRA Medical Device License</td>
            </tr>
            <tr>
              <td><b>🇮🇶 Iraq</b></td>
              <td>MOH Iraq (KIMADIA)</td>
              <td><span class="badge badge-pending">Under Process</span></td>
              <td>Tender Registration & MOH Dossier</td>
            </tr>
            <tr>
              <td><b>🇯🇴 Jordan</b></td>
              <td>JFDA</td>
              <td><span class="badge badge-approved">Approved</span></td>
              <td>JFDA Medical Device Registration</td>
            </tr>
            <tr>
              <td><b>🇱🇧 Lebanon</b></td>
              <td>MOPH Lebanon</td>
              <td><span class="badge badge-pending">Under Renewal</span></td>
              <td>Import Permit & Quality Certificate</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
<script>

// ─────────────────────────────────────────────
// REAL GEOGRAPHIC MARKET MAP
// ─────────────────────────────────────────────

let marketMap = null;

const marketPoints = [
  {
    country: "Saudi Arabia",
    city: "Riyadh",
    lat: 24.7136,
    lng: 46.6753,
    patients: 18500,
    priority: "Critical"
  },
  {
    country: "Saudi Arabia",
    city: "Jeddah",
    lat: 21.4858,
    lng: 39.1925,
    patients: 9200,
    priority: "High"
  },
  {
    country: "UAE",
    city: "Dubai",
    lat: 25.2048,
    lng: 55.2708,
    patients: 6100,
    priority: "High"
  },
  {
    country: "UAE",
    city: "Abu Dhabi",
    lat: 24.4539,
    lng: 54.3773,
    patients: 4800,
    priority: "Medium"
  },
  {
    country: "Qatar",
    city: "Doha",
    lat: 25.2854,
    lng: 51.5310,
    patients: 2800,
    priority: "Medium"
  },
  {
    country: "Kuwait",
    city: "Kuwait City",
    lat: 29.3759,
    lng: 47.9774,
    patients: 3500,
    priority: "High"
  },
  {
    country: "Iraq",
    city: "Baghdad",
    lat: 33.3152,
    lng: 44.3661,
    patients: 4200,
    priority: "High"
  },
  {
    country: "Jordan",
    city: "Amman",
    lat: 31.9539,
    lng: 35.9106,
    patients: 2100,
    priority: "Medium"
  },
  {
    country: "Lebanon",
    city: "Beirut",
    lat: 33.8938,
    lng: 35.5018,
    patients: 1700,
    priority: "Low"
  },
  {
    country: "Oman",
    city: "Muscat",
    lat: 23.5880,
    lng: 58.3829,
    patients: 1900,
    priority: "Medium"
  },
  {
    country: "Bahrain",
    city: "Manama",
    lat: 26.2235,
    lng: 50.5876,
    patients: 1200,
    priority: "Low"
  }
];

const priorityColors = {
  Critical: "#ef4444",
  High: "#f97316",
  Medium: "#eab308",
  Low: "#22c55e"
};

function createMarketMap() {

  const mapElement = document.getElementById("market-map");

  if (!mapElement) {
    console.log("Market map element not found");
    return;
  }

  if (marketMap !== null) {
    marketMap.invalidateSize();
    return;
  }

  // Create real geographic map
  marketMap = L.map("market-map", {
    zoomControl: true,
    scrollWheelZoom: true
  });

  // Center on Middle East
  marketMap.setView([27.5, 46.5], 5);

  // Real world map tiles
  L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      maxZoom: 18,
      attribution: "&copy; OpenStreetMap contributors"
    }
  ).addTo(marketMap);

  // Add dialysis market locations
  marketPoints.forEach(point => {

    const color =
      priorityColors[point.priority] || "#60a5fa";

    const radius =
      point.priority === "Critical" ? 13 :
      point.priority === "High" ? 11 :
      point.priority === "Medium" ? 9 : 7;

    const marker = L.circleMarker(
      [point.lat, point.lng],
      {
        radius: radius,
        color: "#ffffff",
        weight: 2,
        fillColor: color,
        fillOpacity: 0.90
      }
    ).addTo(marketMap);

    marker.bindPopup(`
      <div class="map-popup">

        <div class="map-popup-title">
          ${point.city}, ${point.country}
        </div>

        <div class="map-popup-row">
          <b>HD Patients:</b>
          ${point.patients.toLocaleString()}
        </div>

        <div class="map-popup-row">
          <b>Priority:</b>
          ${point.priority}
        </div>

        <div class="map-popup-row">
          <b>Coordinates:</b>
          ${point.lat.toFixed(4)}, ${point.lng.toFixed(4)}
        </div>

      </div>
    `);
  });

  // Legend
  const legend = L.control({
    position: "bottomright"
  });

  legend.onAdd = function() {

    const div = L.DomUtil.create("div");

    div.style.background = "#0b1628";
    div.style.padding = "10px 12px";
    div.style.border = "1px solid #1e3d7a";
    div.style.borderRadius = "8px";
    div.style.color = "#e8edf5";
    div.style.fontSize = "11px";

    div.innerHTML = `
      <div style="
        font-weight:700;
        margin-bottom:7px;
        color:#c8d8f0;
      ">
        MARKET PRIORITY
      </div>

      <div>🔴 Critical</div>
      <div>🟠 High</div>
      <div>🟡 Medium</div>
      <div>🟢 Low</div>
    `;

    return div;
  };

  legend.addTo(marketMap);

  // Fix Leaflet size after opening hidden page
  setTimeout(() => {
    marketMap.invalidateSize();
  }, 300);
}


// ─────────────────────────────────────────────
// NAVIGATION
// ─────────────────────────────────────────────

function navigate(el, pageId) {

  document.querySelectorAll('.nav-item')
    .forEach(n => n.classList.remove('active'));

  el.classList.add('active');

  document.querySelectorAll('.page')
    .forEach(p => p.classList.remove('active'));

  document.getElementById('page-' + pageId)
    .classList.add('active');

  // Initialize map when Hot Areas opens
  if (pageId === "hotareas") {

    setTimeout(() => {

      createMarketMap();

      if (marketMap) {
        marketMap.invalidateSize();
      }

    }, 200);
  }
}

</script>
<script>
  function navigate(el, pageId) {

  document.querySelectorAll('.nav-item')
    .forEach(n => n.classList.remove('active'));

  el.classList.add('active');

  document.querySelectorAll('.page')
    .forEach(p => p.classList.remove('active'));

  document.getElementById('page-' + pageId)
    .classList.add('active');

  // Initialize map when Hot Areas is opened
  if (pageId === "hotareas") {

    setTimeout(() => {
      createMarketMap();

      if (marketMap) {
        marketMap.invalidateSize();
      }
    }, 150);
  }
}
 
</script>
</body>
</html>
"""

components.html(dashboard_html, height=800, scrolling=False)
