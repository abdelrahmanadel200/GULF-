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

/* Network intelligence pages */
.network-page{--net-primary:#2563eb;--net-accent:#60a5fa;--net-secondary:#ffffff;background:
  radial-gradient(circle at 85% 0%,color-mix(in srgb,var(--net-primary) 18%,transparent),transparent 34%),
  linear-gradient(180deg,color-mix(in srgb,var(--net-primary) 7%,transparent),transparent 40%);
  min-height:100vh;padding-bottom:28px;transition:background .35s ease}
.network-shell{margin:16px;overflow:hidden;border:1px solid color-mix(in srgb,var(--net-primary) 58%,#1e3d7a);
  border-radius:18px;background:#0a172b;box-shadow:0 18px 50px rgba(0,0,0,.32),0 0 45px color-mix(in srgb,var(--net-primary) 12%,transparent)}
.network-hero{position:relative;padding:22px 24px 20px;background:
  linear-gradient(135deg,color-mix(in srgb,var(--net-primary) 30%,#081321) 0%,
  #0d1e38 55%,color-mix(in srgb,var(--net-accent) 14%,#081321) 100%);
  border-bottom:1px solid color-mix(in srgb,var(--net-primary) 52%,#1e3d7a)}
.network-hero:after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;
  background:linear-gradient(90deg,var(--net-primary),var(--net-accent),transparent)}
.network-hero-top{display:flex;align-items:center;gap:12px}
.network-back{border:1px solid rgba(255,255,255,.18);background:rgba(3,12,24,.55);color:#e8edf5;
  padding:8px 12px;border-radius:9px;cursor:pointer;font-size:11px;font-weight:700}
.network-back:hover{border-color:var(--net-accent);background:rgba(3,12,24,.82)}
.network-flag{width:42px;height:29px;border-radius:6px;object-fit:cover;border:1px solid rgba(255,255,255,.25);box-shadow:0 3px 12px rgba(0,0,0,.3)}
.network-title{font-size:23px;font-weight:800;color:#fff;letter-spacing:.2px}
.network-subtitle{font-size:10px;color:#9db5d6;margin-top:3px}
.network-theme-chip{margin-left:auto;display:flex;align-items:center;gap:7px;padding:7px 10px;border-radius:999px;
  background:color-mix(in srgb,var(--net-primary) 18%,#081321);border:1px solid color-mix(in srgb,var(--net-primary) 65%,transparent);
  color:#fff;font-size:9px;font-weight:800;letter-spacing:.7px;text-transform:uppercase}
.network-theme-dot{width:8px;height:8px;border-radius:50%;background:var(--net-accent);box-shadow:0 0 12px var(--net-accent)}
.network-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:16px 20px;background:#081321}
.network-summary-card{background:rgba(255,255,255,.035);border:1px solid #183258;border-top:2px solid var(--net-primary);
  border-radius:12px;padding:12px 14px}
.network-summary-label{font-size:8px;color:#718db5;text-transform:uppercase;letter-spacing:1px;font-weight:800}
.network-summary-value{font-size:20px;font-weight:800;color:#fff;margin-top:5px}
.network-summary-sub{font-size:9px;color:var(--net-accent);margin-top:2px}
.network-toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 20px 14px}
.network-section-title{font-size:13px;font-weight:800;color:#dbeafe}
.network-section-sub{font-size:9px;color:#607a9f;margin-top:3px}
.network-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;padding:0 20px 20px}
.network-card{position:relative;background:#0f1f3d;border:1px solid #1b3a67;border-radius:14px;padding:16px;overflow:hidden;
  transition:.2s ease}
.network-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--net-primary)}
.network-card:hover{transform:translateY(-2px);border-color:var(--net-accent);box-shadow:0 10px 28px rgba(0,0,0,.24),0 0 22px color-mix(in srgb,var(--net-primary) 12%,transparent)}
.network-card-head{display:flex;align-items:flex-start;gap:10px}
.network-num{width:30px;height:30px;flex:0 0 30px;display:flex;align-items:center;justify-content:center;border-radius:9px;
  background:color-mix(in srgb,var(--net-primary) 18%,#081321);border:1px solid color-mix(in srgb,var(--net-primary) 55%,#1e3d7a);
  color:var(--net-accent);font-size:11px;font-weight:900}
.network-name{font-size:13px;font-weight:800;color:#fff;line-height:1.25}
.network-role{font-size:9px;color:#7f9ac1;line-height:1.4;margin-top:3px}
.network-priority{margin-left:auto;white-space:nowrap;font-size:9px;font-weight:800;padding:4px 7px;border-radius:7px}
.network-priority.high{color:#34d399;background:rgba(52,211,153,.10);border:1px solid rgba(52,211,153,.22)}
.network-priority.mid{color:#f59e0b;background:rgba(245,158,11,.10);border:1px solid rgba(245,158,11,.22)}
.network-details{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:13px}
.network-detail-box{background:#081321;border:1px solid #14284b;border-radius:9px;padding:9px}
.network-detail-label{font-size:8px;color:#607a9f;text-transform:uppercase;letter-spacing:.8px;font-weight:800;margin-bottom:4px}
.network-detail-value{font-size:10px;color:#e2e8f0;line-height:1.4;word-break:break-word}
.network-contact{grid-column:1/-1}
.network-footer{padding:0 20px 20px;color:#4e688d;font-size:9px}
.network-footer b{color:#7893b9}
@media(max-width:900px){.network-grid{grid-template-columns:1fr}.network-summary{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.network-hero{padding:18px}.network-title{font-size:19px}.network-theme-chip{display:none}.network-summary,.network-grid{padding-left:12px;padding-right:12px}.network-toolbar{padding-left:12px;padding-right:12px}.network-summary{grid-template-columns:1fr 1fr}.network-shell{margin:10px}.network-details{grid-template-columns:1fr}}
/* Stronger country theme on the country page */
#page-countries.country-theme{position:relative}
#page-countries.country-theme:before{content:"";position:absolute;inset:0 0 auto 0;height:210px;pointer-events:none;
  background:radial-gradient(circle at 50% 0%,color-mix(in srgb,var(--country-primary) 24%,transparent),transparent 68%)}
#page-countries.country-theme .section-title{color:#fff}
#page-countries.country-theme .section-header:after{content:"";height:3px;flex:1;max-width:160px;border-radius:999px;
  background:linear-gradient(90deg,var(--country-primary),var(--country-accent),transparent);box-shadow:0 0 18px color-mix(in srgb,var(--country-primary) 45%,transparent)}
#page-countries.country-theme .country-inline-detail{position:relative}
#page-countries.country-theme .cid-network-card{cursor:pointer}
#page-countries.country-theme .cid-network-card:hover{transform:translateY(-2px);border-color:var(--country-accent);box-shadow:0 0 22px color-mix(in srgb,var(--country-primary) 22%,transparent)}


/* FINAL COUNTRY KPI + NETWORK TABLE UI */
.cid-kpi-grid{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px!important}
.cid-kpi{background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.018))!important;border:1px solid color-mix(in srgb,var(--country-primary) 72%,#1264a3)!important;border-radius:14px!important;box-shadow:0 8px 22px rgba(0,0,0,.16);padding:16px!important;min-height:105px!important}
.cid-kpi-label{color:#78b7ea!important;font-size:9px!important;font-weight:800!important;letter-spacing:1px!important;text-transform:uppercase}
.cid-kpi-value{color:#fff!important;font-size:23px!important;font-weight:900!important;margin-top:8px!important}
.cid-kpi:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(0,0,0,.22),0 0 18px color-mix(in srgb,var(--country-primary) 15%,transparent)}
.network-table-wrap{margin:0 20px 20px;background:#0b1830;border:1px solid color-mix(in srgb,var(--net-primary) 45%,#1b3a67);border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.network-table-header{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 18px;background:linear-gradient(135deg,color-mix(in srgb,var(--net-primary) 13%,#0b1830),#0b1830);border-bottom:1px solid #1b3a67}
.network-table-title{font-size:14px;font-weight:900;color:#fff}.network-table-subtitle{font-size:9px;color:#6f89ad;margin-top:4px}
.network-search{width:320px;max-width:45%;padding:10px 12px;border-radius:9px;border:1px solid #294c7a;background:#071326;color:#e5edf8;outline:none;font-size:10px}
.network-search:focus{border-color:var(--net-accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--net-accent) 15%,transparent)}
.network-table-scroll{overflow-x:auto}.network-table{width:100%;min-width:980px;border-collapse:collapse}.network-table th{padding:11px 13px;background:#071326;color:#7893b9;border-bottom:1px solid #1b3a67;text-align:left;font-size:9px;text-transform:uppercase;letter-spacing:.7px;white-space:nowrap}.network-table td{padding:12px 13px;color:#dce6f4;border-bottom:1px solid #152c4d;vertical-align:top;font-size:10px;line-height:1.45}.network-table tr:hover{background:color-mix(in srgb,var(--net-primary) 7%,#0b1830)}.network-table tr:last-child td{border-bottom:0}.network-table-num{width:42px;color:var(--net-accent)!important;font-weight:900;text-align:center}.network-table-name{color:#fff;font-size:11px;font-weight:800;min-width:160px}.network-table-main{min-width:170px}.network-contact-cell{min-width:180px;color:#a9bdd6}.network-extra{min-width:220px;color:#c7d5e8}.network-priority{display:inline-flex;align-items:center;justify-content:center;padding:4px 9px;border-radius:7px;white-space:nowrap;font-size:9px;font-weight:900}.network-table-footer{display:flex;justify-content:space-between;padding:10px 15px;background:#071326;border-top:1px solid #152c4d;color:#536e92;font-size:9px}
.reg-detail-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:14px}.reg-detail-card{background:#0f1f3d;border:1px solid #1e3d7a;border-radius:13px;padding:15px}.reg-detail-card h4{margin:0 0 6px;color:#60a5fa;font-size:10px;text-transform:uppercase;letter-spacing:.8px}.reg-detail-card p{margin:0;color:#c8d8f0;font-size:10px;line-height:1.6}.reg-detail-wide{grid-column:1/-1}
.procurement-wrap{margin-top:16px;background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;overflow:hidden}.procurement-head{padding:15px 18px;border-bottom:1px solid #1e3d7a}.procurement-head-title{color:#e8edf5;font-size:13px;font-weight:800}.procurement-head-sub{color:#6a85b0;font-size:9px;margin-top:4px}.procurement-table{width:100%;border-collapse:collapse;min-width:1050px;font-size:10px}.procurement-table th{padding:11px 13px;background:#071326;color:#7893b9;text-align:left;text-transform:uppercase;font-size:9px;letter-spacing:.6px}.procurement-table td{padding:12px 13px;border-top:1px solid #152c4d;color:#cbd6e8;vertical-align:top;line-height:1.45}.exh-url{display:inline-flex;margin-top:8px;color:#60a5fa;text-decoration:none;font-size:9px}.exh-url:hover{text-decoration:underline}
@media(max-width:1000px){.cid-kpi-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important}.reg-detail-grid{grid-template-columns:1fr}}
@media(max-width:700px){.cid-kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.network-table-header{flex-direction:column;align-items:stretch}.network-search{max-width:none;width:100%}.network-table-wrap{margin-left:12px;margin-right:12px}}
@media(max-width:480px){.cid-kpi-grid{grid-template-columns:1fr!important}}

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
.sidebar { pointer-events:auto !important; position:relative; width: 200px; min-width: 200px; background: #070f1f; border-right: 1px solid #1e3d7a; display: flex; flex-direction: column; padding: 18px 0; top: 0; height: 100vh; z-index: 999999; align-self: flex-start; }
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
.c-card { height:150px; background:linear-gradient(145deg,#10223f,#0a172b); border:1px solid color-mix(in srgb,var(--cc,#2563eb) 48%,#1e3d7a); border-radius:16px; padding:0; cursor:pointer; transition:all .25s ease; display:flex; align-items:flex-end; position:relative; overflow:hidden; min-width:0; box-shadow:0 8px 24px rgba(0,0,0,.20); isolation:isolate; }
.c-card:after { content:""; position:absolute; inset:0; z-index:0; pointer-events:none; background:radial-gradient(circle at 88% 12%,color-mix(in srgb,var(--cc,#2563eb) 28%,transparent),transparent 45%); opacity:.7; transition:opacity .25s; }
.c-card:hover,.c-card:focus-visible { outline:none; transform:translateY(-5px) scale(1.015); border-color:var(--cc,#2563eb); box-shadow:0 14px 32px rgba(0,0,0,.35),0 0 0 2px color-mix(in srgb,var(--cc,#2563eb) 72%,transparent),0 0 34px color-mix(in srgb,var(--cc,#2563eb) 30%,transparent); }
.c-card.active { transform:translateY(-6px) scale(1.025); border:2px solid var(--cc,#2563eb); box-shadow:0 18px 38px rgba(0,0,0,.42),0 0 0 3px color-mix(in srgb,var(--cc,#2563eb) 30%,transparent),0 0 42px color-mix(in srgb,var(--cc,#2563eb) 42%,transparent); }
.c-card.active:after { opacity:1; }
.c-card.active .c-overlay { background:linear-gradient(to bottom,rgba(4,15,31,.00) 10%,rgba(4,15,31,.10) 42%,rgba(4,15,31,.94) 100%); }
.c-card.active .c-accent { height:5px; box-shadow:0 0 18px var(--cc,#2563eb),0 0 32px var(--cc,#2563eb); }
.c-card.active .c-flag img { transform:scale(1.08); border-color:rgba(255,255,255,.8); box-shadow:0 0 14px color-mix(in srgb,var(--cc,#2563eb) 55%,transparent); }
.c-landscape { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:center center; display:block; transform:scale(1.01); transition:transform .25s ease,filter .25s ease; }
.c-card:hover .c-landscape { transform:scale(1.04); filter:brightness(1.06); }
.c-card.active .c-landscape { transform:scale(1.06); filter:brightness(1.08) saturate(1.05); }
.c-overlay { position:absolute; inset:0; background:linear-gradient(to bottom,rgba(4,15,31,.05) 25%,rgba(4,15,31,.18) 48%,rgba(4,15,31,.92) 100%); z-index:1; }
.c-bottom { position:relative; z-index:4; width:100%; display:flex; align-items:center; gap:10px; padding:0 14px 13px; min-width:0; }
.c-flag { width:38px; height:27px; flex:0 0 38px; display:flex; align-items:center; justify-content:center; filter:drop-shadow(0 3px 7px rgba(0,0,0,.55)); }
.c-flag img { width:38px; height:27px; object-fit:cover; object-position:center; display:block; border-radius:5px; border:1px solid rgba(255,255,255,.28); transition:all .2s ease; }
.c-country-code { position:absolute; top:12px; right:12px; z-index:4; padding:4px 7px; border-radius:999px; font-size:8px; font-weight:900; letter-spacing:1px; color:#fff; background:rgba(3,12,24,.58); border:1px solid color-mix(in srgb,var(--cc,#2563eb) 70%,transparent); backdrop-filter:blur(6px); }
.c-card.active .c-country-code { background:var(--cc,#2563eb); border-color:rgba(255,255,255,.45); box-shadow:0 0 16px color-mix(in srgb,var(--cc,#2563eb) 55%,transparent); }
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
<script>window.sidebarNavigate=function(pageId){try{var page=document.getElementById("page-"+pageId);if(!page)return false;document.querySelectorAll(".page").forEach(function(p){p.classList.remove("active")});page.classList.add("active");document.querySelectorAll(".nav-item").forEach(function(n){n.classList.remove("active")});var nav=document.querySelector('.nav-item[data-page="'+pageId+'"]');if(nav)nav.classList.add("active");if(pageId!=="countries"&&typeof window.closeCountry==="function")window.closeCountry();if(pageId==="hotareas"&&typeof window.createMarketMap==="function")setTimeout(function(){try{window.createMarketMap();if(window.marketMap)window.marketMap.invalidateSize()}catch(e){}},200);return false}catch(e){console.error(e);return false}};</script>
<div class="dash">

<div class="sidebar">
  <div class="logo">
    <div class="logo-text">AMECATH</div>
    <div class="logo-sub">Market Intelligence</div>
  </div>
  <div class="nav-section-label">Main</div>
  <div class="nav-item active" data-page="overview" role="button" tabindex="0" onclick="return window.sidebarNavigate('overview');"><span class="nav-icon">🏠</span><span>Overview</span></div>
  <div class="nav-item" data-page="countries" role="button" tabindex="0" onclick="return window.sidebarNavigate('countries');"><span class="nav-icon">🌍</span><span>Country Analysis</span></div>
  <div class="nav-item" data-page="forecast" role="button" tabindex="0" onclick="return window.sidebarNavigate('forecast');"><span class="nav-icon">📈</span><span>Revenue Forecast</span></div>
  <div class="nav-section-label">Market</div>
  <div class="nav-item" data-page="pricing" role="button" tabindex="0" onclick="return window.sidebarNavigate('pricing');"><span class="nav-icon">💲</span><span>Pricing Intel</span></div>
  <div class="nav-item" data-page="tenders" role="button" tabindex="0" onclick="return window.sidebarNavigate('tenders');"><span class="nav-icon">📋</span><span>Tenders</span></div>
  <div class="nav-item" data-page="competitors" role="button" tabindex="0" onclick="return window.sidebarNavigate('competitors');"><span class="nav-icon">🏆</span><span>Competitors</span></div>
  <div class="nav-section-label">Field</div>
  <div class="nav-item" data-page="hotareas" role="button" tabindex="0" onclick="return window.sidebarNavigate('hotareas');"><span class="nav-icon">📍</span><span>Hot Areas</span></div>
  <div class="nav-item" data-page="exhibitions" role="button" tabindex="0" onclick="return window.sidebarNavigate('exhibitions');"><span class="nav-icon">📅</span><span>Exhibitions</span></div>
    <div class="nav-item" data-page="regulatory" role="button" tabindex="0" onclick="return window.sidebarNavigate('regulatory');"><span class="nav-icon">📜</span><span>Regulatory</span></div>
  <div class="nav-section-label">Info</div>
  <div class="nav-item" data-page="sources" role="button" tabindex="0" onclick="return window.sidebarNavigate('sources');"><span class="nav-icon">📚</span><span>Sources</span></div>
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
  <div class="c-card" data-country="sa" style="--cc:#10b981" role="listitem" tabindex="0" onclick="openCountry('sa')" onkeydown="if(event.key==='Enter')openCountry('sa')" aria-label="Saudi Arabia">
     <div class="c-country-code">KSA</div>
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/saudi_landscape.jpeg" alt="Saudi Arabia landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/saudi_arabia_flag.jpeg" alt="Saudi Arabia flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Saudi Arabia</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" data-country="ae" style="--cc:#f59e0b" role="listitem" tabindex="0" onclick="openCountry('ae')" onkeydown="if(event.key==='Enter')openCountry('ae')" aria-label="UAE">
     <div class="c-country-code">UAE</div>
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/uae_landscape.jpeg" alt="UAE landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/uae_flag.jpeg" alt="UAE flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">UAE</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" data-country="kw" style="--cc:#3b82f6" role="listitem" tabindex="0" onclick="openCountry('kw')" onkeydown="if(event.key==='Enter')openCountry('kw')" aria-label="Kuwait">
     <div class="c-country-code">KWT</div>
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/kuwait_landscape.jpeg" alt="Kuwait landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/kuwait_flag.jpeg" alt="Kuwait flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Kuwait</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" data-country="qa" style="--cc:#8b5cf6" role="listitem" tabindex="0" onclick="openCountry('qa')" onkeydown="if(event.key==='Enter')openCountry('qa')" aria-label="Qatar">
     <div class="c-country-code">QAT</div>
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/qatar_landscape.jpeg" alt="Qatar landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/qatar_flag.jpeg" alt="Qatar flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Qatar</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" data-country="om" style="--cc:#ef4444" role="listitem" tabindex="0" onclick="openCountry('om')" onkeydown="if(event.key==='Enter')openCountry('om')" aria-label="Oman">
     <div class="c-country-code">OMN</div>
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/oman_landscape.jpeg" alt="Oman landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/oman_flag.jpeg" alt="Oman flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Oman</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" data-country="bh" style="--cc:#ec4899" role="listitem" tabindex="0" onclick="openCountry('bh')" onkeydown="if(event.key==='Enter')openCountry('bh')" aria-label="Bahrain">
     <div class="c-country-code">BHR</div>
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/bahrain_landscape.jpg" alt="Bahrain landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/bahraien_flag.jpeg" alt="Bahrain flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Bahrain</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" data-country="jo" style="--cc:#06b6d4" role="listitem" tabindex="0" onclick="openCountry('jo')" onkeydown="if(event.key==='Enter')openCountry('jo')" aria-label="Jordan">
     <div class="c-country-code">JOR</div>
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/jordon_landscape.jpeg" alt="Jordan landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/jordon_flag.jpeg" alt="Jordan flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Jordan</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" data-country="lb" style="--cc:#a3e635" role="listitem" tabindex="0" onclick="openCountry('lb')" onkeydown="if(event.key==='Enter')openCountry('lb')" aria-label="Lebanon">
     <div class="c-country-code">LBN</div>
    <img class="c-landscape" src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/lebanon_landscape.jpeg" alt="Lebanon landscape" loading="lazy" onerror="this.style.display='none'">
    <div class="c-overlay"></div>
    <div class="c-bottom"><span class="c-flag"><img src="https://raw.githubusercontent.com/abdelrahmanadel200/GULF-/main/assets/landscapes/lebanon_flag.jpeg" alt="Lebanon flag" loading="lazy" onerror="this.style.display='none'"></span><div class="c-name">Lebanon</div><div class="c-arrow">›</div></div>
    <div class="c-accent"></div>
  </div>
  <div class="c-card" data-country="iq" style="--cc:#f97316" role="listitem" tabindex="0" onclick="openCountry('iq')" onkeydown="if(event.key==='Enter')openCountry('iq')" aria-label="Iraq">
     <div class="c-country-code">IRQ</div>
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

<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px;background:#0f1f3d;border:1px solid #1e3d7a;border-radius:12px;padding:12px 14px;">
    <div><div style="font-size:12px;font-weight:700;color:#e8edf5;">🌍 Forecast Focus</div><div style="font-size:9px;color:#6a85b0;margin-top:3px;">Select one country to isolate its base-case forecast</div></div>
    <select id="forecast-country-select" onchange="filterForecastCountry(this.value)" style="min-width:220px;background:#081321;color:#e8edf5;border:1px solid #1e3d7a;border-radius:8px;padding:8px 10px;font-size:11px;">
      <option value="all">All Countries</option>
      <option value="Saudi Arabia">🇸🇦 Saudi Arabia</option><option value="UAE">🇦🇪 UAE</option><option value="Qatar">🇶🇦 Qatar</option><option value="Kuwait">🇰🇼 Kuwait</option><option value="Oman">🇴🇲 Oman</option><option value="Bahrain">🇧🇭 Bahrain</option><option value="Jordan">🇯🇴 Jordan</option><option value="Lebanon">🇱🇧 Lebanon</option><option value="Iraq">🇮🇶 Iraq</option>
    </select>
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
      <td data-country="${r.name}" style="padding:12px 16px;color:#e8edf5;font-weight:600;">${r.flag} ${r.name}</td>
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
  window.filterForecastCountry=function(country){document.querySelectorAll('#country-forecast-body tr').forEach(function(tr,i){if(i===rows.length)return;var cell=tr.querySelector('td[data-country]');tr.style.display=(!country||country==='all'||(cell&&cell.getAttribute('data-country')===country))?'':'none';});};
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

<div class="procurement-wrap"><div class="procurement-head"><div class="procurement-head-title">🏛️ Procurement Body Intelligence</div><div class="procurement-head-sub">Who controls purchasing of HD catheters and dialysis consumables by market</div></div><div style="overflow-x:auto"><table class="procurement-table"><thead><tr><th>#</th><th>Country</th><th>Primary Procurement Body</th><th>Secondary / Parallel Buyers</th><th>Who Really Controls the Purchase</th></tr></thead><tbody><tr><td>1</td><td><b>🇸🇦 Saudi Arabia</b></td><td>NUPCO (National Unified Procurement Company) via Etimad portal</td><td>MOH hospital clusters, large private groups (Dr. Sulaiman Al‑Habib, Mouwasat, etc.)</td><td>NUPCO consolidates demand and runs national framework tenders for MOH hospitals and many government facilities; Etimad is the e‑procurement platform where tenders are published. moh+2</td></tr><tr><td>2</td><td><b>🇦🇪 UAE</b></td><td>MOHAP (federal), DoH Abu Dhabi (via SEHA / Rafed GPO), DHA (Dubai)</td><td>Large private groups (VPS, Mediclinic, Aster, NMC)</td><td>Federal procurement via MOHAP for northern emirates; Abu Dhabi via DoH/SEHA and Rafed GPO; Dubai via DHA eSupply; private groups run their own tenders. uaelegislation.gov+4</td></tr><tr><td>3</td><td><b>🇶🇦 Qatar</b></td><td>Hamad Medical Corporation (HMC) + MOH</td><td>Private hospitals (The View, Al Emadi, etc.)</td><td>HMC is the main public provider and runs centralized frameworks for dialysis consumables; MOH runs parallel tenders for primary care centers.</td></tr><tr><td>4</td><td><b>🇰🇼 Kuwait</b></td><td>MOH Kuwait (Central Procurement)</td><td>Private hospitals (Al‑Sabah, Al‑Razi, etc.)</td><td>MOH runs national consumable tenders; large public hospitals (Al‑Sabah, Al‑Razi) are key end‑users; private hospitals run separate tenders.</td></tr><tr><td>5</td><td><b>🇴🇲 Oman</b></td><td>MOH Oman (Central Procurement)</td><td>Private hospital groups (KIMSHEALTH, Burjeel, etc.)</td><td>MOH runs national frameworks for consumables; private groups procure separately.</td></tr><tr><td>6</td><td><b>🇯🇴 Jordan</b></td><td>MOH Jordan (Central Procurement) + Royal Medical Services (RMS)</td><td>Large private hospitals (Istiklal, Al‑Khalidi, etc.)</td><td>MOH runs annual tenders; RMS runs separate military hospital tenders; big private hospitals run their own.</td></tr><tr><td>7</td><td><b>🇱🇧 Lebanon</b></td><td>MOH Lebanon (Central Procurement) + public hospital networks</td><td>Private hospital groups (AUBMC, Hotel Dieu, Mount Lebanon, etc.)</td><td>Crisis context: MOH and public hospitals run tenders, often with NGO/donor support; private groups procure independently.</td></tr><tr><td>8</td><td><b>🇮🇶 Iraq</b></td><td>Kimadia (State Company for Marketing Drugs &amp; Medical Appliances, MOH)</td><td>Regional health directorates (Baghdad, Basra, KRI), private hospitals</td><td>Kimadia runs national tenders for consumables; regional directorates and large hospitals (Baghdad Medical City, etc.) also run project‑specific tenders.</td></tr><tr><td>9</td><td><b>🇧🇭 Bahrain</b></td><td>MOH Bahrain (Central Procurement) + BDF Hospital / RMS</td><td>Private hospitals (Royal Bahrain, Bahrain Specialist, etc.)</td><td>MOH runs central tenders; BDF/RMS runs separate military hospital tenders; private hospitals procure separately.</td></tr></tbody></table></div></div>

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
      {year:'2027',month:'01',date:'25–28 Jan 2027',name:'Arab Health (World Health Expo Dubai)',url:'https://www.worldhealthexpo.com/events/healthcare/dubai/',location:'Dubai, UAE',flag:'🇦🇪',focus:'General Healthcare + Dialysis',priority:'critical',icon:'🔴'},
      {year:'2027',month:'01',date:'Jan 2027',name:'SIRS 2027 — Saudi IR Society',location:'Riyadh, KSA',flag:'🇸🇦',focus:'IR + Dialysis Access',priority:'critical',icon:'🔴'},
      {year:'2027',month:'02',date:'Feb 2027',name:'Gulf Aorta Summit (GAS)',url:'https://www.gulfaorta.com/',location:'Dubai, UAE',flag:'🇦🇪',focus:'Vascular + Endovascular',priority:'high',icon:'🟠'},
      {year:'2027',month:'03',date:'29–30 Mar 2027',name:'Urology & Nephrology Conference',location:'Dubai, UAE',flag:'🇦🇪',focus:'Nephrology + Dialysis',priority:'high',icon:'🟠'},
      {year:'2027',month:'04',date:'1–4 Apr 2027',name:'World Congress of Nephrology (WCN)',location:'Kuala Lumpur, Malaysia',flag:'🇲🇾',focus:'Global Nephrology',priority:'high',icon:'🟠'},
      {year:'2027',month:'04',date:'Apr–May 2027',name:'PAIRS 2027 — Pan Arab IR Society',location:'Dubai, UAE',flag:'🇦🇪',focus:'IR + Vascular Access + Dialysis',priority:'critical',icon:'🔴'},
      {year:'2027',month:'09',date:'2027 TBA',name:'TCT Plus Middle East',location:'Dubai, UAE',flag:'🇦🇪',focus:'Cardiovascular + Vascular Access',priority:'high',icon:'🟠'},
      {year:'2027',month:'10',date:'26–29 Oct 2027',name:'Global Health Exhibition (GHE)',location:'Riyadh, KSA',flag:'🇸🇦',focus:'Medical Devices + MOH / NUPCO',priority:'critical',icon:'🔴'},
      {year:'2027',month:'12',date:'Dec 2027',name:'Qatar Nephrology Conference (QNC)',location:'Doha, Qatar',flag:'🇶🇦',focus:'Nephrology + Dialysis',priority:'critical',icon:'🔴'},
      {year:'2027',month:'12',date:'Dec 2027',name:'PAVSS Annual Meeting',location:'Rotating',flag:'🌍',focus:'Vascular Surgery + HD Access',priority:'high',icon:'🟠'},
      {year:'2028',month:'01',date:'Jan 2028',name:'Arab Health 2028',location:'Dubai, UAE',flag:'🇦🇪',focus:'Medical Devices',priority:'critical',icon:'🔴'},
      {year:'2028',month:'04',date:'27–30 Apr 2028',name:'World Congress of Nephrology (WCN) 2028',url:'https://www.theisn.org/wcn/',location:'Montreal, Canada',flag:'🇨🇦',focus:'Global Nephrology',priority:'medium',icon:'🟡'},
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
          ${e.url?`<a class="exh-url" href="${e.url}" target="_blank" rel="noopener">🌐 Official Website</a>`:''}
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
<div class="section-header" style="margin-top:18px"><span style="font-size:16px">🧾</span><span class="section-title">Detailed Registration Intelligence</span></div><div class="reg-detail-grid"><div class="reg-detail-card reg-detail-wide"><h4>Uae</h4><div class="reg-detail-grid" style="margin-top:8px"><div class="reg-detail-card"><h4>Regulatory Authority &amp; Portal</h4><p>Emirates Drug Establishment (EDE) – federal regulator. Online portal: EDE e‑services. kayrouzandassociates+2</p></div><div class="reg-detail-card"><h4>Device Classification for HD Catheters</h4><p>Class C / Class D (high‑risk intravascular; aligned with EU Class IIb/III). meddeviceguide</p></div><div class="reg-detail-card"><h4>Local Authorized Representative (AR) Mandate</h4><p>Mandatory. Must appoint a Local Authorized Representative (LAR) licensed by EDE. A distributor can serve as AR if it holds the appropriate EDE license and signs a formal LOA. meddeviceguide+1</p></div><div class="reg-detail-card"><h4>Key Legal &amp; Quality Documents</h4><p>- ISO 13485:2016 (valid, IAF‑accredited) – mandatory - Certificate of Free Sale (CFS) / Certificate of Conformity - CE MDR Certificate and/or FDA 510(k)/PMA letter - SFDA registration certificate (strong supporting document) - Health Canada MDL (supporting) - Technical Dossier in STED/CSDT format (device description, intended use, classification justification, risk management ISO 14971, biocompatibility ISO 10993, sterilization validation, clinical evaluation summary) - GMP / Manufacturing License - Letter of Authorization (LOA) to LAR (notarized + apostille or EDE‑accepted e‑verification)</p></div><div class="reg-detail-card"><h4>Legalization &amp; Attestation</h4><p>EDE increasingly accepts electronic verification and apostille; full embassy attestation often not required if documents are electronically verifiable. Notarization + apostille recommended for LOA and CFS. meddeviceguide</p></div><div class="reg-detail-card"><h4>Estimated Registration Timeline</h4><p>- Fast‑Track / Reliance: ~3–5 months (from complete dossier) - Standard: ~6–9 months Official published target: ~45 working days for marketing authorization, but real‑world timelines are longer for high‑risk devices. meddeviceguide+1</p></div><div class="reg-detail-card"><h4>Official Government Fees (USD approx.)</h4><p>- Classification request: ~USD 135 (AED 500) - Manufacturer site registration: ~USD 2,750 (AED 10,100) - Device registration (per product family): ~USD 1,360 (AED 5,000) - Renewal (every 5 years): ~USD 680 (AED 2,500)</p></div><div class="reg-detail-card"><h4>Registration License Validity</h4><p>5 years from date of committee approval. vanzbon</p></div><div class="reg-detail-card"><h4>Fast‑Track Leverage with ISO 13485</h4><p>ISO 13485 + CE MDR + SFDA + FDA creates a strong reliance case; EDE may waive certain QMS queries and focus on technical/clinical review. meddeviceguide+1</p></div></div></div><div class="reg-detail-card reg-detail-wide"><h4>Qatar</h4><div class="reg-detail-grid" style="margin-top:8px"><div class="reg-detail-card"><h4>Regulatory Authority &amp; Portal</h4><p>Ministry of Public Health (MOPH) – Pharmacy and Drug Control Department (PDCD). Online e‑system for registration.</p></div><div class="reg-detail-card"><h4>Device Classification for HD Catheters</h4><p>Class C / D (high‑risk implantable/intravascular). Aligned with EU Class IIb/III.</p></div><div class="reg-detail-card"><h4>Local Authorized Representative (AR) Mandate</h4><p>Mandatory. Must appoint a Qatar‑licensed local agent/distributor as AR. The AR submits via PDCD portal and is legally responsible.</p></div><div class="reg-detail-card"><h4>Key Legal &amp; Quality Documents</h4><p>- ISO 13485:2016 – mandatory - CFS / Certificate of Conformity - CE MDR Certificate and/or FDA clearance/approval - SFDA registration certificate (strong supporting document) - Health Canada MDL (supporting) - Technical Dossier (STED/CSDT): device description, intended use, classification, risk management, biocompatibility, sterilization, clinical evaluation - GMP / Manufacturing License - LOA to local AR (notarized + apostille or Qatar‑accepted e‑verification)</p></div><div class="reg-detail-card"><h4>Legalization &amp; Attestation</h4><p>MOPH accepts apostille and increasingly electronic verification; full embassy attestation often not required if documents are verifiable online.</p></div><div class="reg-detail-card"><h4>Estimated Registration Timeline</h4><p>- Abridged / Reliance: ~2–4 months - Standard: ~6–9 months Statutory review ~60 working days, but practical timelines vary.</p></div><div class="reg-detail-card"><h4>Official Government Fees (USD approx.)</h4><p>Fees not always published transparently; typical range for high‑risk device registration: USD 1,000–2,500 per product family (agent‑dependent). Renewal every 5 years at similar level.</p></div><div class="reg-detail-card"><h4>Registration License Validity</h4><p>5 years (standard for medical devices).</p></div><div class="reg-detail-card"><h4>Fast‑Track Leverage with ISO 13485</h4><p>ISO 13485 + CE/FDA/SFDA allows MOPH to rely on QMS audits performed by notified bodies/FDA; reduces QMS queries and accelerates review.</p></div></div></div><div class="reg-detail-card reg-detail-wide"><h4>Kuwait</h4><div class="reg-detail-grid" style="margin-top:8px"><div class="reg-detail-card"><h4>Regulatory Authority &amp; Portal</h4><p>Ministry of Health (MOH) – Drug Control Department (DCD). Online portal for medical device registration.</p></div><div class="reg-detail-card"><h4>Device Classification for HD Catheters</h4><p>Class C / D (high‑risk intravascular). Aligned with EU Class IIb/III.</p></div><div class="reg-detail-card"><h4>Local Authorized Representative (AR) Mandate</h4><p>Mandatory. Must appoint a Kuwait‑licensed local agent (distributor) as AR. Foreign manufacturers cannot apply directly.</p></div><div class="reg-detail-card"><h4>Key Legal &amp; Quality Documents</h4><p>- ISO 13485:2016 – mandatory - CFS / Certificate of Free Sale - CE MDR Certificate and/or FDA clearance/approval - SFDA registration certificate (highly valued) - Health Canada MDL (supporting) - Technical Dossier (STED/CSDT): device description, intended use, classification justification, risk management, biocompatibility, sterilization, clinical evaluation - GMP / Manufacturing License - LOA to local AR (notarized + apostille or Kuwait‑accepted e‑verification)</p></div><div class="reg-detail-card"><h4>Legalization &amp; Attestation</h4><p>Under Decree 387/2025, electronic certificates and e‑verification are accepted; apostille generally sufficient; embassy attestation often not required if documents are verifiable.</p></div><div class="reg-detail-card"><h4>Estimated Registration Timeline</h4><p>- Abridged / Fast‑Track: ~2–4 months - Standard: ~6–9 months</p></div><div class="reg-detail-card"><h4>Official Government Fees (USD approx.)</h4><p>Fees not fully public; typical high‑risk device registration: USD 1,000–2,000 per product family. Renewal every 5 years.</p></div><div class="reg-detail-card"><h4>Registration License Validity</h4><p>5 years (standard).</p></div><div class="reg-detail-card"><h4>Fast‑Track Leverage with ISO 13485</h4><p>ISO 13485 + CE/FDA/SFDA is explicitly recognized under Decree 387/2025 for abridged review; QMS documentation often accepted without additional audit.</p></div></div></div><div class="reg-detail-card reg-detail-wide"><h4>Oman</h4><div class="reg-detail-grid" style="margin-top:8px"><div class="reg-detail-card"><h4>Regulatory Authority &amp; Portal</h4><p>Ministry of Health (MOH) – Drug Safety Center (DSC). E‑portal: eportal.moh.gov.om.</p></div><div class="reg-detail-card"><h4>Device Classification for HD Catheters</h4><p>Class C / D (high‑risk intravascular). Aligned with EU Class IIb/III.</p></div><div class="reg-detail-card"><h4>Local Authorized Representative (AR) Mandate</h4><p>Mandatory. Must appoint an Oman‑licensed local agent/distributor as AR. AR submits via e‑portal and is legally responsible.</p></div><div class="reg-detail-card"><h4>Key Legal &amp; Quality Documents</h4><p>- ISO 13485:2016 – mandatory - CFS / Certificate of Free Sale - CE MDR Certificate and/or FDA clearance/approval - SFDA registration certificate (strong supporting document) - Health Canada MDL (supporting) - Technical Dossier (GD3 / CSDT): device description, intended use, classification, risk management, biocompatibility, sterilization, clinical evaluation - GMP / Manufacturing License - LOA to local AR (notarized + apostille or Oman‑accepted e‑verification)</p></div><div class="reg-detail-card"><h4>Legalization &amp; Attestation</h4><p>MOH accepts apostille and increasingly electronic verification; full embassy attestation generally not required if documents are verifiable.</p></div><div class="reg-detail-card"><h4>Estimated Registration Timeline</h4><p>- Reliance / Abridged: ~2–3 months (within 60 working days statutory window) - Standard: ~3–5 months</p></div><div class="reg-detail-card"><h4>Official Government Fees (USD approx.)</h4><p>- Class C/D product registration: ~USD 520 (200 OMR) per product family. - Manufacturer registration: additional fee (varies).</p></div><div class="reg-detail-card"><h4>Registration License Validity</h4><p>5 years (standard for high‑risk devices).</p></div><div class="reg-detail-card"><h4>Fast‑Track Leverage with ISO 13485</h4><p>ISO 13485 + CE/FDA/SFDA is explicitly accepted under Circular 161/2025 for Class C/D devices; QMS review is streamlined.</p></div></div></div><div class="reg-detail-card reg-detail-wide"><h4>Bahrain</h4><div class="reg-detail-grid" style="margin-top:8px"><div class="reg-detail-card"><h4>Regulatory Authority &amp; Portal</h4><p>National Health Regulatory Authority (NHRA) – Medical Devices Registration via Ajheza / MADR e‑portal.</p></div><div class="reg-detail-card"><h4>Device Classification for HD Catheters</h4><p>Class C / D (high‑risk intravascular; aligned with EU Class IIb/III).</p></div><div class="reg-detail-card"><h4>Local Authorized Representative (AR) Mandate</h4><p>Mandatory. Must appoint a Bahrain‑licensed Local Authorized Representative (LAR) registered with NHRA. A distributor can serve as AR if it holds the appropriate NHRA license and signs a formal LOA.</p></div><div class="reg-detail-card"><h4>Key Legal &amp; Quality Documents</h4><p>- ISO 13485:2016 – mandatory - CE MDR Certificate and/or FDA clearance/approval - SFDA registration certificate (strong supporting document; GCC recognition) - Health Canada MDL (supporting) - Certificate of Free Sale (CFS) / Certificate of Conformity - Technical Dossier (STED/CSDT): device description, intended use, classification, risk management, biocompatibility, sterilization, clinical evaluation - GMP / Manufacturing License - LOA to local AR (notarized + apostille or NHRA‑accepted e‑verification)</p></div><div class="reg-detail-card"><h4>Legalization &amp; Attestation</h4><p>NHRA accepts apostille and increasingly electronic verification; full embassy attestation generally not required if documents are verifiable.</p></div><div class="reg-detail-card"><h4>Estimated Registration Timeline</h4><p>- Reliance / Abridged (with CE/FDA/SFDA): ~2–4 months - Standard: ~4–6 months NHRA Circular 19/2026 extends deadlines but prioritizes high‑risk devices; your catheters should be in the high‑risk monthly quota.</p></div><div class="reg-detail-card"><h4>Official Government Fees (USD approx.)</h4><p>- High‑risk (Class C/D) first registration: ~USD 2,650 (BHD 1,000) - Annual renewal (high‑risk): ~USD 530 (BHD 200) - Submission fee: ~USD 13 (BHD 5) per device.</p></div><div class="reg-detail-card"><h4>Registration License Validity</h4><p>1 year (annual renewal required).</p></div><div class="reg-detail-card"><h4>Fast‑Track Leverage with ISO 13485 + CE/FDA/SFDA</h4><p>ISO 13485 + CE/FDA/SFDA enables reliance pathway; NHRA may accept GCC/SFDA approval as primary technical basis, reducing review time.</p></div><div class="reg-detail-card"><h4>Post‑Market &amp; Labelling</h4><p>- UDI / GS1 DataMatrix: NHRA is implementing a traceability programme; UDI strongly recommended for high‑risk devices. - Arabic labelling &amp; IFU: Mandatory bilingual (Arabic + English) labelling; Arabic must have equal or greater prominence. IFU in Arabic required for high‑risk devices.</p></div></div></div></div>
</div>

<div class="page network-page" id="page-distributors-sa" data-network-type="distributors" data-network-country="sa"></div>
<div class="page network-page" id="page-distributors-ae" data-network-type="distributors" data-network-country="ae"></div>
<div class="page network-page" id="page-distributors-kw" data-network-type="distributors" data-network-country="kw"></div>
<div class="page network-page" id="page-distributors-qa" data-network-type="distributors" data-network-country="qa"></div>
<div class="page network-page" id="page-distributors-om" data-network-type="distributors" data-network-country="om"></div>
<div class="page network-page" id="page-distributors-bh" data-network-type="distributors" data-network-country="bh"></div>
<div class="page network-page" id="page-distributors-jo" data-network-type="distributors" data-network-country="jo"></div>
<div class="page network-page" id="page-distributors-lb" data-network-type="distributors" data-network-country="lb"></div>
<div class="page network-page" id="page-distributors-iq" data-network-type="distributors" data-network-country="iq"></div>
<div class="page network-page" id="page-kols-sa" data-network-type="kols" data-network-country="sa"></div>
<div class="page network-page" id="page-kols-ae" data-network-type="kols" data-network-country="ae"></div>
<div class="page network-page" id="page-kols-kw" data-network-type="kols" data-network-country="kw"></div>
<div class="page network-page" id="page-kols-qa" data-network-type="kols" data-network-country="qa"></div>
<div class="page network-page" id="page-kols-om" data-network-type="kols" data-network-country="om"></div>
<div class="page network-page" id="page-kols-bh" data-network-type="kols" data-network-country="bh"></div>
<div class="page network-page" id="page-kols-jo" data-network-type="kols" data-network-country="jo"></div>
<div class="page network-page" id="page-kols-lb" data-network-type="kols" data-network-country="lb"></div>
<div class="page network-page" id="page-kols-iq" data-network-type="kols" data-network-country="iq"></div>

</div><!-- end .main -->
<!-- SOURCES -->
<div class="page" id="page-sources">
  <div style="padding:0 16px 32px;">

    <div style="margin-bottom:18px;">
      <div style="font-size:15px;font-weight:600;color:#c8d8f0;display:flex;align-items:center;gap:8px;margin-bottom:4px;">
        <span>📚</span> Data Sources &amp; Methodology
      </div>
      <div style="font-size:11px;color:#3a5278;">AMECATH Market Intelligence — 2026 Edition · Gulf &amp; Middle East</div>
    </div>

    <!-- Source category cards -->
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;">
      <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #60a5fa;border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:20px;margin-bottom:6px;">🏛️</div>
        <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">Official Bodies</div>
        <div style="font-size:22px;font-weight:700;color:#60a5fa;margin-top:6px;">9</div>
        <div style="font-size:10px;color:#3b82f6;margin-top:3px;">Ministries & authorities</div>
      </div>
      <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #34d399;border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:20px;margin-bottom:6px;">📊</div>
        <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">Market Reports</div>
        <div style="font-size:22px;font-weight:700;color:#34d399;margin-top:6px;">12</div>
        <div style="font-size:10px;color:#34d399;margin-top:3px;">Research & analytics firms</div>
      </div>
      <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #f59e0b;border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:20px;margin-bottom:6px;">🏥</div>
        <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">Clinical Data</div>
        <div style="font-size:22px;font-weight:700;color:#f59e0b;margin-top:6px;">7</div>
        <div style="font-size:10px;color:#f59e0b;margin-top:3px;">Hospital & registry data</div>
      </div>
      <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-top:3px solid #a78bfa;border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:20px;margin-bottom:6px;">📋</div>
        <div style="font-size:9px;letter-spacing:1px;color:#6a85b0;text-transform:uppercase;font-weight:600;">Procurement Portals</div>
        <div style="font-size:22px;font-weight:700;color:#a78bfa;margin-top:6px;">6</div>
        <div style="font-size:10px;color:#a78bfa;margin-top:3px;">Tender & GPO platforms</div>
      </div>
    </div>

    <!-- Sources table -->
    <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;overflow:hidden;margin-bottom:16px;">
      <div style="padding:14px 18px;border-bottom:1px solid #1e3d7a;display:flex;align-items:center;gap:8px;">
        <span style="font-size:14px;">🏛️</span>
        <div style="font-size:13px;font-weight:600;color:#c8d8f0;">Official Health Authorities & Ministries</div>
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead><tr style="background:#070f1f;">
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Country</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Authority</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Data Used</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Portal / Reference</th>
        </tr></thead>
        <tbody id="src-official-body"></tbody>
      </table>
    </div>

    <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;overflow:hidden;margin-bottom:16px;">
      <div style="padding:14px 18px;border-bottom:1px solid #1e3d7a;display:flex;align-items:center;gap:8px;">
        <span style="font-size:14px;">📊</span>
        <div style="font-size:13px;font-weight:600;color:#c8d8f0;">Market Research & Analytics Sources</div>
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead><tr style="background:#070f1f;">
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Source</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Report / Dataset</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Data Applied To</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Year</th>
        </tr></thead>
        <tbody id="src-market-body"></tbody>
      </table>
    </div>

    <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;overflow:hidden;margin-bottom:16px;">
      <div style="padding:14px 18px;border-bottom:1px solid #1e3d7a;display:flex;align-items:center;gap:8px;">
        <span style="font-size:14px;">📋</span>
        <div style="font-size:13px;font-weight:600;color:#c8d8f0;">Procurement Portals & Tender Platforms</div>
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead><tr style="background:#070f1f;">
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Platform</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Country</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">Use in Dashboard</th>
          <th style="padding:10px 16px;color:#6a85b0;font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:left;font-weight:600;">URL</th>
        </tr></thead>
        <tbody id="src-portal-body"></tbody>
      </table>
    </div>

    <!-- Methodology note -->
    <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-left:3px solid #60a5fa;border-radius:12px;padding:18px 20px;">
      <div style="font-size:12px;font-weight:700;color:#c8d8f0;margin-bottom:10px;">📐 Methodology Notes</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
        <div style="background:#081321;border-radius:8px;padding:12px;">
          <div style="font-size:10px;font-weight:700;color:#60a5fa;margin-bottom:6px;">HD PATIENT ESTIMATES</div>
          <div style="font-size:11px;color:#8fa8cf;line-height:1.6;">Country patient figures are derived from MOH annual reports, nephrological society registries, and cross-validated against USRDS/ERA-EDTA international benchmarks. Where official counts were unavailable, dialysis facility capacity × average utilization rate was applied.</div>
        </div>
        <div style="background:#081321;border-radius:8px;padding:12px;">
          <div style="font-size:10px;font-weight:700;color:#34d399;margin-bottom:6px;">CATHETER DEMAND FORMULA</div>
          <div style="font-size:11px;color:#8fa8cf;line-height:1.6;">Annual catheter demand = HD patients × 2.6 catheters/year (industry standard for tunneled + non-tunneled, including replacements). PD catheter demand calculated separately at 1 catheter/patient/2 years.</div>
        </div>
        <div style="background:#081321;border-radius:8px;padding:12px;">
          <div style="font-size:10px;font-weight:700;color:#f59e0b;margin-bottom:6px;">MARKET VALUE CALCULATION</div>
          <div style="font-size:11px;color:#8fa8cf;line-height:1.6;">Market value (USD) = Annual catheter demand × blended average selling price per unit. Average unit price $110–$130 USD across tunneled HD catheters (non-tunneled weighted lower). Country-specific pricing premiums applied for UAE, Qatar, Kuwait.</div>
        </div>
        <div style="background:#081321;border-radius:8px;padding:12px;">
          <div style="font-size:10px;font-weight:700;color:#a78bfa;margin-bottom:6px;">REVENUE FORECAST MODEL</div>
          <div style="font-size:11px;color:#8fa8cf;line-height:1.6;">Bottom-up forecast built from country-level market share targets. Conservative scenario assumes 2–3% initial share. Base case 3–5%. Upside 6–8%. Growth rates reflect HD patient growth (CAGR ~4–6% GCC) plus new facility openings and catheter replacement cycles.</div>
        </div>
      </div>
    </div>

    <div style="text-align:center;padding:16px 0 8px;font-size:10px;color:#2a4060;">
      AMECATH Market Intelligence · 2026 Edition · Data compiled from public registries, government portals, and proprietary field research · Last updated: 2026
    </div>
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


const networkData = {"distributors":{"sa":[{"num":1,"name":"AMHSCO – Arabian Medical Hospital Supply","relevance":"Very High — medical devices, life-sciences, specifically has a renal division","contact":"☎️ +966 11 462 1188 · ✉️ sales@amhsco.com","website":"AMHSCO","latestTender":"Aug 2026 (NUPCO NDP0788/26 dialysis framework) nupco","competitors":"Fresenius KSA, B. Braun KSA, multiple HD catheter brands","priority":"🔴 5/5"},{"num":2,"name":"AlwanMed","relevance":"Very High — licensed medical-device distributor; serves major government/private hospitals; tender submissions","contact":"Contact through website","website":"AlwanMed","latestTender":"Jul 2026 (NUPCO medical device tenders)","competitors":"Medtronic KSA, BD KSA, vascular access brands","priority":"🔴 5/5"},{"num":3,"name":"Aman Medical","relevance":"Very High — explicitly supplies dialysis systems and medical devices","contact":"☎️ +966 54 882 1508 · ✉️ info@amanmedical.com","website":"Aman Medical","latestTender":"Aug 2026 (NUPCO dialysis consumables) nupco","competitors":"Fresenius, Baxter, B. Braun dialysis portfolio","priority":"🔴 5/5"},{"num":4,"name":"FUMEDCO / MNAF3 Arabia","relevance":"High — medical equipment, devices & disposables; supplies large government hospitals","contact":"☎️ +966 11 400 3493 · ✉️ info@mnaf3arabia.com","website":"FUMEDCO","latestTender":"Jun 2026 (NUPCO medical device tenders)","competitors":"Multiple international HD catheter brands","priority":"🟠 4/5"},{"num":5,"name":"House of Rays Medical","relevance":"High — 350+ healthcare clients; medical consumables; nationwide coverage","contact":"Website / WhatsApp","website":"House of Rays Medical","latestTender":"Jul 2026 (NUPCO open framework for dialysis supplies) nupco","competitors":"Authorized distributor for global medical manufacturers since 2005","priority":"🟠 4/5"},{"num":6,"name":"Nipras AlSalhiya Medical","relevance":"High — medical equipment/devices/accessories; branches Dammam, Riyadh, Jeddah, Tabuk, Khamis","contact":"Website contact","website":"Nipras Medical","latestTender":"Aug 2026 (NUPCO dialysis framework) nupco","competitors":"Multiple HD catheter brands; vascular access devices","priority":"🟠 4/5"},{"num":7,"name":"Jama Medical","relevance":"High — nationwide logistics; Riyadh/Jeddah/Dammam/Qassim facilities","contact":"Website contact","website":"Jama Medical","latestTender":"Jul 2026 (NUPCO medical equipment tenders)","competitors":"Comprehensive medical equipment portfolio; HD catheters","priority":"🟠 4/5"},{"num":8,"name":"Watan Medical Company","relevance":"High — medical devices, supplies & equipment across KSA","contact":"☎️ +966 13 833 3606 · ✉️ info@watanmedical.com","website":"Watan Medical","latestTender":"Jun 2026 (NUPCO dialysis consumables) nupco","competitors":"Fresenius KSA, multiple dialysis consumable brands","priority":"🟠 4/5"},{"num":9,"name":"Healthcare Systems Saudi","relevance":"Medium–High — medical consumables, hospital supplies; serves MOH, military, National Guard and private hospitals","contact":"☎️ +966 92 000 4438 · ✉️ sales@hs-saudi.com","website":"Healthcare Systems Saudi","latestTender":"Aug 2026 (NUPCO medical device tenders)","competitors":"Multiple HD catheter brands; hospital supplies","priority":"🟡 3/5"},{"num":10,"name":"Raqwani Medicals","relevance":"Medium–High — medical devices, equipment, surgical supplies and hospital products","contact":"☎️ +966 56 393 3574 / +966 50 124 3758 · ✉️ info@raqwanimedicals.com","website":"Raqwani Medicals","latestTender":"Jul 2026 (NUPCO framework participation) nupco","competitors":"Multiple international HD catheter brands","priority":"🟡 3/5"}],"ae":[{"num":1,"name":"GulfDrug LLC","relevance":"Very High — one of UAE’s largest healthcare distributors; explicit dialysis-equipment portfolio and long-standing hospital supply relationships.","contact":"☎️ +971 4 501 4000 · ✉️ info@gulfdrug.com","website":"GulfDrug","latestTender":"Aug 2026 (MOHAP/SEHA consumables frameworks; GulfDrug routinely bids on national dialysis-consumable tenders)","competitors":"Fresenius Medical Care (dialysis systems & consumables), B. Braun, multiple international HD catheter brands","priority":"🔴 5/5"},{"num":2,"name":"TTSA Medical Group FZCO","relevance":"Very High — official UAE distributor for B. Braun and Nipro dialysis systems/consumables; strong renal focus.","contact":"✉️ info@ttsa-group.com (Dubai Silicon Oasis, IFZA)","website":"TTSA Medical","latestTender":"Jul 2026 (SEHA/MOHAP dialysis-consumable frameworks)","competitors":"B. Braun, Nipro; full dialysis consumables line (tubing, needles, catheters, concentrates)","priority":"🔴 5/5"},{"num":3,"name":"One Health (PureHealth)","relevance":"Very High — authorized distributor for top global medical-device brands; dedicated renal-care division serving 300+ providers.","contact":"Contact via website (PureHealth/One Health portal)","website":"One Health","latestTender":"Aug 2026 (SEHA/MOHAP device frameworks)","competitors":"Medtronic, Siemens Healthineers, GE HealthCare, Philips; renal-care portfolios from major OEMs","priority":"🔴 5/5"},{"num":4,"name":"Zahrawi Group (Al Zahrawi Medical Supplies)","relevance":"High — GCC-wide medical/surgical distributor with UAE HQ; lists catheters and dialysis solutions in portfolio.","contact":"Contact via website (Dubai HQ)","website":"Zahrawi Group","latestTender":"Jun 2026 (MOHAP/SEHA surgical & consumable tenders)","competitors":"Multiple international catheter brands; surgical/ICU consumables; dialysis solutions","priority":"🟠 4/5"},{"num":5,"name":"Emirates & World Medical Supplies (EWMS)","relevance":"High — broad medical-disposables and equipment distributor; serves hospitals, authorities, and defense; strong supply-chain capability.","contact":"☎️ +971 4 447-0098 · ✉️ support@ewms.ae","website":"EWMS","latestTender":"Jul 2026 (MOHAP/SEHA consumables frameworks)","competitors":"Infection-control, ICU, anesthesia/nerve-block (Pajunk), multi-brand disposables; hospital supply networks","priority":"🟠 4/5"},{"num":6,"name":"Medeon Medical Equipment Trading LLC","relevance":"High — explicit dialysis-equipment supplier in UAE; lists hemodialysis catheters among core products.","contact":"☎️ +971 4 572 2034 / +971 52 994 5833 · ✉️ info@medeonmed.com","website":"Medeon","latestTender":"Jun 2026 (private-hospital and clinic dialysis procurements)","competitors":"Multiple HD catheter brands; dialysis machines, tubing, dialyzers, concentrates","priority":"🟠 4/5"},{"num":7,"name":"Winray Medical Equipment Trading LLC","relevance":"High — dialysis-equipment supplier in Dubai; serves hospitals/clinics with dialysis machines and accessories.","contact":"☎️ +971 4 282 3307 / +971 52 352 2291 · ✉️ info@winraymed.com","website":"Winray","latestTender":"Jun 2026 (private-sector dialysis procurements)","competitors":"Multiple HD catheter brands; dialysis machines and consumables","priority":"🟠 4/5"},{"num":8,"name":"Majestic Medical","relevance":"High — vascular-access reseller with dedicated long-term and short-term hemodialysis catheters.","contact":"Contact via website","website":"Majestic Medical","latestTender":"Jul 2026 (private hospital vascular-access tenders)","competitors":"International vascular-access brands; HD catheters (long/short term)","priority":"🟠 4/5"},{"num":9,"name":"Al-Futtaim Health (HealthHub)","relevance":"Medium–High — integrated healthcare operator with clinic network; procures consumables and devices across UAE.","contact":"☎️ +971 4 596 7000 · ✉️ info.healthhub@alfuttaim.com","website":"Al-Futtaim Health","latestTender":"Aug 2026 (internal framework renewals for clinic consumables)","competitors":"Multi-brand medical consumables; works with global OEMs via group procurement","priority":"🟡 3/5"},{"num":10,"name":"Royal Care Medical Equipment Trading LLC","relevance":"Medium–High — supplier of disposable medical products and surgical supplies to hospitals/clinics across UAE.","contact":"☎️ +971 52 641 9796 · ✉️ sapana@royalcaremedicalsuae.com","website":"Royal Care","latestTender":"Jun 2026 (private hospital consumable tenders)","competitors":"Romsons, AP Medical; catheters & tubing, IV sets, surgical gloves, PPE","priority":"🟡 3/5"}],"qa":[{"num":1,"name":"Fayn Al Tbyh / Fayn Medical","relevance":"Vascular access + medical consumables; explicitly offers vascular-access products and partnership/distribution services","contact":"☎️ +974 4491 9296 / +974 4431 0911 · ✉️ info@fayn.qa","website":"Fayn Medical","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Multi-brand vascular-access and dialysis consumables; international catheter OEMs","priority":"🔴 5/5"},{"num":2,"name":"Barzan Medical Supplies","relevance":"Major Qatar healthcare distributor; medical equipment, hospital disposables & consumables; strong Hamad Medical Corp ties","contact":"☎️ +974 4441 0270 · ✉️ info@barzanmedical.com","website":"Barzan Medical","latestTender":"Jul 2026 (HMC/MOH consumable frameworks)","competitors":"Global OEMs across surgical, ICU, and vascular access; multi-brand catheters","priority":"🔴 5/5"},{"num":3,"name":"Gulf Engineering & Technical Services (GENTECH)","relevance":"One of Qatar’s largest biomedical/medical-equipment groups; supplies hospitals/clinics nationwide","contact":"☎️ +974 4486 8100 · ✉️ gentech@gentechqa.com","website":"GENTECH","latestTender":"Aug 2026 (MOHAP/SEHA-style consumable frameworks)","competitors":"Multiple international HD catheter brands; dialysis machines and consumables","priority":"🔴 5/5"},{"num":4,"name":"Care Medical Trading","relevance":"Established medical-equipment distributor serving healthcare, diagnostics & life sciences","contact":"Website/contact form","website":"Care Medical","latestTender":"Jun 2026 (private-hospital procurements)","competitors":"International medical-device brands; catheters and disposables","priority":"🔴 5/5"},{"num":5,"name":"Universal Trade Line (UTL)","relevance":"20+ years distributing medical equipment, consumables & laboratory products to government/private sectors","contact":"Website/contact","website":"UTL Qatar","latestTender":"Jul 2026 (MOH consumable frameworks)","competitors":"Global manufacturers; vascular access and catheters","priority":"🔴 5/5"},{"num":6,"name":"Origin Trading & Contracting WLL","relevance":"Medical equipment + consumables + procurement/logistics; 13+ years","contact":"☎️ +974 4002 0246 · ✉️ info@originqatar.com","website":"Origin Qatar","latestTender":"Jun 2026 (private-sector consumable tenders)","competitors":"Multi-brand disposables; catheters, IV sets, surgical supplies","priority":"🟠 4/5"},{"num":7,"name":"Khalid Scientific Company","relevance":"Long-standing medical-equipment supplier with dialysis and hospital-supply portfolios","contact":"☎️ +974 4441 7371 / +974 4432 5198","website":"Khalid Scientific","latestTender":"Jun 2026 (private-hospital dialysis procurements)","competitors":"Multiple HD catheter brands; dialysis consumables and machines","priority":"🟠 4/5"},{"num":8,"name":"Ibn Al Haytham Centre","relevance":"Medical devices/equipment + consumables + surgical instruments","contact":"☎️ +974 4431 2283 · ✉️ sales@ibncentre.com","website":"Ibn Al Haytham","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"International medical-equipment brands; catheters and disposables","priority":"🟠 4/5"},{"num":9,"name":"Gulfmed Medical Supplies","relevance":"Medical-supply company in Doha; broad consumables range","contact":"☎️ +974 4486 6216","website":"—","latestTender":"Jun 2026 (private-sector consumable tenders)","competitors":"Multi-brand medical consumables; catheters and surgical supplies","priority":"🟠 4/5"},{"num":10,"name":"Novel Medical Solutions W.L.L.","relevance":"Healthcare supply & distribution company; wholesale medical supplies","contact":"☎️ +974 4467 5151 · ✉️ info@novelmedsolution.com","website":"Novel Medical","latestTender":"Jul 2026 (MOH consumable frameworks)","competitors":"International medical consumables; vascular access and catheters","priority":"🟠 4/5"}],"kw":[{"num":1,"name":"Advanced Technology Company (ATC)","relevance":"~90% market share in dialysis systems; strong government-hospital relationships","contact":"☎️ +965 2224 7444 · ✉️ info@atc.com.kw","website":"ATC Kuwait","latestTender":"Aug 2026 (MOH dialysis-system/consumable frameworks)","competitors":"Fresenius, Baxter, B. Braun dialysis portfolios; HD catheters","priority":"🔴 5/5"},{"num":2,"name":"Arabi Medical & Scientific Equipment","relevance":"Major healthcare supplier; explicitly supplies dialysis equipment + consumables","contact":"Arabi Holding contact","website":"Arabi Holding","latestTender":"Jul 2026 (MOH dialysis/consumable frameworks)","competitors":"Global dialysis and medical-device OEMs; catheters and consumables","priority":"🔴 5/5"},{"num":3,"name":"DMC Trading Co.","relevance":"25+ years; supplies MOH, Ministry of Defense & private hospitals","contact":"☎️ +965 6515 0700 · ✉️ info@dmc-kw.com","website":"DMC Kuwait","latestTender":"Jul 2026 (MOH surgical/consumable tenders)","competitors":"International medical manufacturers; catheters and disposables","priority":"🔴 5/5"},{"num":4,"name":"United Medical Commodities (UMC)","relevance":"20+ years; represents international medical manufacturers","contact":"☎️ +965 2245 0815/6 · ✉️ info@medcom.com.kw","website":"UMC Kuwait","latestTender":"Jun 2026 (private-hospital dialysis procurements)","competitors":"Multiple international HD catheter brands; vascular access","priority":"🔴 5/5"},{"num":5,"name":"Medical Means Co. / Al Redwan Group","relevance":"Major GCC dialysis/medical-supply organization","contact":"Regional contact","website":"Redwan Medical","latestTender":"Jun 2026 (private-hospital dialysis procurements)","competitors":"Fresenius, Baxter, B. Braun dialysis portfolios; HD catheters","priority":"🔴 5/5"},{"num":6,"name":"Medvision for Medical Services","relevance":"Top-5 medical distributor in Kuwait; dedicated disposable division supplying hospitals daily","contact":"☎️ +965 2202 2228 · ✉️ info@medvision-kw.com","website":"Medvision Kuwait","latestTender":"Jul 2026 (MOH surgical/consumable tenders)","competitors":"Multiple international HD catheter brands; broad disposables portfolio","priority":"🔴 5/5"},{"num":7,"name":"Leader Medical Company","relevance":"Medical equipment + supplies; hospital/clinic distribution","contact":"☎️ +965 2246 1967","website":"—","latestTender":"Jun 2026 (private-sector consumable tenders)","competitors":"Multi-brand catheters and surgical consumables","priority":"🟠 4/5"},{"num":8,"name":"Warba Medical Supplies Co","relevance":"Medical supplies; broad consumables portfolio","contact":"☎️ +965 2232 3850","website":"—","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"International consumables; catheters and IV sets","priority":"🟠 4/5"},{"num":9,"name":"Ahmed Company for Wholesale","relevance":"30+ years; clinical disposables, surgical tools & medical consumables; handles tenders","contact":"Sales team / website","website":"Ahmed Company","latestTender":"Jul 2026 (MOH consumable frameworks)","competitors":"Clinical disposables, surgical tools; multi-brand catheters","priority":"🟠 4/5"},{"num":10,"name":"New Star Company WLL","relevance":"High-tech medical-equipment distributor with exclusive international partnerships","contact":"☎️ +965 5515 0547 · ✉️ info@starmedicalkw.com","website":"New Star Kuwait","latestTender":"Jun 2026 (private-hospital dialysis procurements)","competitors":"Global manufacturers; vascular access and catheters","priority":"🟠 4/5"}],"om":[{"num":1,"name":"Taiba Medserv (Taiba Medical Services)","relevance":"Leading medical-equipment distributor; strong MOH relationships and service capability","contact":"☎️ +968 2459 3395 / +968 2459 6695 · ✉️ medical@omanmed.com","website":"Taiba Medserv","latestTender":"Aug 2026 (MOH renal-dialysis device/consumable tenders)","competitors":"Fresenius, B. Braun, multiple HD catheter brands","priority":"🔴 5/5"},{"num":2,"name":"Oman Medical Supplies & Services (OMANMED / Suhail Bahwan)","relevance":"Major medical/laboratory distributor; nationwide hospital coverage","contact":"☎️ +968 2465 0750 / +968 2465 9778 · ✉️ bhc@suhailbahwangroup.com","website":"Suhail Bahwan Medical","latestTender":"Jul 2026 (MOH consumable frameworks)","competitors":"Global OEMs; dialysis consumables and catheters","priority":"🔴 5/5"},{"num":3,"name":"Medical & Scientific Supplies LLC","relevance":"Imports/markets hospital equipment, surgical products, pharmaceuticals & consumables","contact":"☎️ +968 2449 7844","website":"—","latestTender":"Jul 2026 (MOH device/consumable tenders)","competitors":"International medical-device brands; catheters and disposables","priority":"🔴 5/5"},{"num":4,"name":"Al Farsi Medical Supplies (AFMS)","relevance":"Established importer/distributor; surgical consumables + medical equipment","contact":"☎️ +968 2448 5625 · WhatsApp +968 9225 8225","website":"—","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Multi-brand surgical consumables; catheters","priority":"🔴 5/5"},{"num":5,"name":"Niemath Al Noor Trading LLC (NieMed)","relevance":"Nationwide medical equipment + consumables; hospital/clinic supply","contact":"☎️ +968 7928 3733 / +968 7952 7382 · ✉️ info@niemathalnoor.com","website":"NieMed Oman","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Global manufacturers; catheters and disposables","priority":"🔴 5/5"},{"num":6,"name":"MSTE LLC","relevance":"Medical devices, consumables & disposables; large Muscat warehouse","contact":"☎️ +968 2423 8417 · ✉️ info@msteoman.com","website":"MSTE Oman","latestTender":"Jul 2026 (MOH consumable frameworks)","competitors":"Multiple international HD catheter brands; hospital supplies","priority":"🔴 5/5"},{"num":7,"name":"Mazoon Medical Supplies","relevance":"Public/private healthcare supply; consumables including catheters","contact":"☎️ +968 9644 2500 · ✉️ info@mazoonmedical.com","website":"Mazoon Medical","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Certified global manufacturers; catheters and surgical disposables","priority":"🟠 4/5"},{"num":8,"name":"Seha Medical Supplies","relevance":"Medical equipment; cardiac & vascular solutions","contact":"☎️ +968 2411 2944 · ✉️ info@seha.om","website":"Seha Oman","latestTender":"Jun 2026 (private-hospital vascular-access tenders)","competitors":"International cardiac/vascular brands; catheters","priority":"🟠 4/5"},{"num":9,"name":"MuscatMed / HUI Medical Supplies","relevance":"Importer/distributor of medical equipment & surgical disposables","contact":"☎️ +968 7909 8973 / +968 9257 5465","website":"—","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Multi-brand medical equipment; catheters and disposables","priority":"🟠 4/5"},{"num":10,"name":"Advanced Medical Instruments Co. (AMICO)","relevance":"Medical equipment, medical supplies & consumables","contact":"Oman Yellow Pages / company contact","website":"—","latestTender":"Jun 2026 (private-sector procurements)","competitors":"International medical consumables; catheters","priority":"🟠 4/5"}],"jo":[{"num":1,"name":"Micromed Medical Supplies Co.","relevance":"One of Jordan's largest interventional/surgical/medical-product suppliers; 15+ years' experience","contact":"☎️ +962 6 553 3389 · ✉️ info@micromedjo.com","website":"Micromed Jordan","latestTender":"Aug 2026 (MOH/UNRWA consumable frameworks)","competitors":"Global corporations; interventional and vascular-access portfolios","priority":"🔴 5/5"},{"num":2,"name":"Greenland Medical","relevance":"Vascular Access + Interventional Radiology specifically listed","contact":"☎️ +962 6 515 6480 · +962 79 588 7422","website":"—","latestTender":"Jul 2026 (private-hospital interventional tenders)","competitors":"International vascular-access and IR brands; catheters","priority":"🔴 5/5"},{"num":3,"name":"Hijazi Medical Supplies (HMS)","relevance":"Catheters + vascular/interventional products","contact":"☎️ +962 6 515 4826 · ✉️ info@hijazibros.com","website":"Hijazi Bros","latestTender":"Jun 2026 (private-hospital vascular-access tenders)","competitors":"Multi-brand catheters; vascular/interventional products","priority":"🔴 5/5"},{"num":4,"name":"NAJD Medical","relevance":"Interventional products; supplies major public/private hospitals","contact":"☎️ +962 79 621 7161 · ✉️ elayan@najdmed.com","website":"Najd Medical","latestTender":"Jul 2026 (private-hospital interventional tenders)","competitors":"Well-known international brands; catheters and interventional devices","priority":"🔴 5/5"},{"num":5,"name":"RAMANA Medical Supplies","relevance":"Vascular + interventional radiology; distributor for international companies","contact":"Contact via website","website":"RAMANA Jordan","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"International companies; vascular and IR portfolios","priority":"🔴 5/5"},{"num":6,"name":"World Medical Supplies (WMS)","relevance":"Supplies Jordan MOH + Royal Medical Services","contact":"☎️ +962 79 914 0755","website":"—","latestTender":"Jul 2026 (MOH consumable frameworks)","competitors":"Multi-brand medical consumables; catheters","priority":"🔴 5/5"},{"num":7,"name":"United for Marketing","relevance":"Works directly with Jordan MOH and public/private hospitals","contact":"Website contact","website":"—","latestTender":"Jul 2026 (MOH consumable frameworks)","competitors":"Global medical-device brands; catheters and disposables","priority":"🔴 5/5"},{"num":8,"name":"Al-Ahlia Company","relevance":"Medical-device distributor since 1987; strong local infrastructure","contact":"☎️ +962 6 465 0951 · +962 77 736 8181 · ✉️ info@ahliamed.com","website":"Ahlia Medical","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"International medical-device brands; catheters","priority":"🟠 4/5"},{"num":9,"name":"Redwan Medical Group","relevance":"Regional distributor (KSA/UAE/Kuwait/Jordan) of dialysis equipment and hospital consumables","contact":"Contact via website","website":"Redwan Medical","latestTender":"Jun 2026 (private-hospital dialysis procurements)","competitors":"Fresenius, Baxter, B. Braun dialysis portfolios; HD catheters","priority":"🟠 4/5"},{"num":10,"name":"Surur Medical","relevance":"Medical equipment + surgical consumables; hospital/medical-center distribution","contact":"Website contact","website":"Surur Medical","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Multi-brand surgical consumables; catheters","priority":"🟠 4/5"}],"lb":[{"num":1,"name":"Medical & Technical Services (MTS)","relevance":"Explicit dialysis-catheter portfolio; serves hospitals nationwide","contact":"☎️ +961 5 811 027 / +961 5 811 028","website":"MTS Lebanon","latestTender":"Aug 2026 (private-hospital dialysis-consumable tenders)","competitors":"Multiple international HD catheter brands; PICC and CVC lines","priority":"🔴 5/5"},{"num":2,"name":"MedTrust Solutions","relevance":"Vascular access + hemodialysis + endovascular","contact":"☎️ +961 3 293 893 · contact via website","website":"MedTrust","latestTender":"Jul 2026 (private-hospital vascular-access tenders)","competitors":"Global vascular-access and endovascular brands; catheters","priority":"🔴 5/5"},{"num":3,"name":"Fattal Group (Healthcare Division)","relevance":"Major healthcare distributor with aesthetic/medical-devices division; broad hospital network","contact":"☎️ +961 1 485 250 · ✉️ Elie.Moubarak@fattal.com.lb","website":"Fattal Healthcare","latestTender":"Jul 2026 (private-hospital device/consumable frameworks)","competitors":"Global medical-device brands; vascular access and catheters","priority":"🔴 5/5"},{"num":4,"name":"Allied Medical Group (AMG)","relevance":"Vascular/peripheral intervention + medical devices","contact":"☎️/email via website","website":"AMG Lebanon","latestTender":"Jun 2026 (private-hospital interventional tenders)","competitors":"International vascular/peripheral intervention brands; catheters","priority":"🔴 5/5"},{"num":5,"name":"Promedz Lebanon","relevance":"Interventional radiology + peripheral vascular + venous therapy","contact":"☎️ +961 70 827 807 · +961 1 364 659/60 · ✉️ promedz@promedz.com","website":"Promedz","latestTender":"Jun 2026 (private-hospital interventional tenders)","competitors":"Global IR and peripheral vascular brands; venous therapy","priority":"🔴 5/5"},{"num":6,"name":"Intelmed S.A.R.L.","relevance":"Vascular + interventional radiology + cardiothoracic surgery","contact":"☎️ +961 1 425 724","website":"—","latestTender":"Jun 2026 (private-hospital interventional tenders)","competitors":"International vascular/IR/cardiothoracic brands; catheters","priority":"🔴 5/5"},{"num":7,"name":"REMED Medical Equipment","relevance":"Trusted supplier of medical equipment/accessories/supplies in Beirut; dedicated sales/technical services","contact":"☎️ +961 70 701 696 / +961 3 124 790 · ✉️ info@remed-lb.com","website":"REMED Lebanon","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"International medical-equipment brands; catheters and disposables","priority":"🟠 4/5"},{"num":8,"name":"Biofield Medical","relevance":"Specialized medical consumables for interventional fields","contact":"Website contact","website":"Biofield Medical","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Specialized interventional consumables; catheters","priority":"🟠 4/5"},{"num":9,"name":"Hayek Investment / HayekInv Medical","relevance":"Disposable devices for IR + vascular surgery","contact":"☎️ +961 1 87 33 81 · +961 3 66 22 72","website":"—","latestTender":"Jun 2026 (private-hospital interventional tenders)","competitors":"Disposable IR/vascular devices; multi-brand catheters","priority":"🟠 4/5"},{"num":10,"name":"Serum Product Co. Sarl","relevance":"Retailers of dialysis apparatus; long-standing presence in Metn/Beirut","contact":"☎️ +961 5 480 207 / +961 5 480 208","website":"Serum Product","latestTender":"Jun 2026 (private-clinic dialysis procurements)","competitors":"Dialysis apparatus and consumables; HD catheters","priority":"🟠 4/5"}],"iq":[{"num":1,"name":"SIDRAL S.A.R.L","relevance":"Fresenius Medical Care partner; operates 6 MOH-authorized dialysis centers; distributes dialysis machines/consumables nationwide","contact":"☎️ +964 780 377 0000 / +964 780 788 9918 · ✉️ info@sidral.com","website":"SIDRAL","latestTender":"Sep 2026 (KIMADIA hemodialysis national-project tenders)","competitors":"Fresenius Medical Care (dialysis systems & consumables); HD catheters","priority":"🔴 5/5"},{"num":2,"name":"Jadarah Scientific Bureau","relevance":"Leading medical-devices distributor since 2004; explicitly lists long-term & short-term hemodialysis catheters","contact":"☎️ +964 770 456 42 16 · ✉️ info@jadarah-iq.com","website":"Jadarah Iraq","latestTender":"Sep 2026 (KIMADIA medical-supplies frameworks)","competitors":"Multiple international HD catheter brands; dialysis consumables","priority":"🔴 5/5"},{"num":3,"name":"Al-Hayat Company (Hayat IQ)","relevance":"Laboratory & medical-appliance distributor; broad hospital-supply network; vascular-access consumables","contact":"☎️ +964 773 825 5919 · ✉️ info@hayatiq.com","website":"Hayat IQ","latestTender":"Aug 2026 (MOH/private-hospital consumable tenders)","competitors":"Multi-brand medical consumables; catheters and disposables","priority":"🔴 5/5"},{"num":4,"name":"Noor AlAdeeb Scientific Bureau","relevance":"MOH-approved medical-supplies distributor; serves hospitals, clinics, government institutions; certified disposables","contact":"Website/contact form","website":"Noor AlAdeeb","latestTender":"Aug 2026 (MOH consumable frameworks)","competitors":"International medical disposables; catheters","priority":"🔴 5/5"},{"num":5,"name":"KIMADIA (State Company for Marketing Drugs & Medical Appliances)","relevance":"Central MOH procurement entity; runs national hemodialysis and medical-appliance tenders","contact":"✉️ dg@kimadia.gov.iq · ☎️ +964 1 415 7667","website":"KIMADIA","latestTender":"Sep 2026 (Hemodialysis National Project Service/Expansion tenders)","competitors":"Multiple international HD catheter brands via tender awards","priority":"🔴 5/5"},{"num":6,"name":"Al-Rayan Medical","relevance":"Medical-equipment and consumables distributor; serves public/private hospitals","contact":"Contact via website","website":"—","latestTender":"Aug 2026 (private-hospital consumable tenders)","competitors":"Multi-brand medical equipment; catheters","priority":"🟠 4/5"},{"num":7,"name":"Zahraa Medical Supplies","relevance":"Surgical and medical consumables; hospital/clinic distribution","contact":"Contact via website","website":"—","latestTender":"Jul 2026 (private-hospital consumable tenders)","competitors":"International surgical consumables; catheters","priority":"🟠 4/5"},{"num":8,"name":"Tigris Medical","relevance":"Medical devices and equipment; broad consumables portfolio","contact":"Contact via website","website":"—","latestTender":"Jul 2026 (private-hospital consumable tenders)","competitors":"Global medical-device brands; catheters","priority":"🟠 4/5"},{"num":9,"name":"Mesopotamia Medical Trading","relevance":"Medical-equipment trading; hospital-supply networks","contact":"Contact via website","website":"—","latestTender":"Jun 2026 (private-sector procurements)","competitors":"Multi-brand medical consumables; catheters","priority":"🟡 3/5"},{"num":10,"name":"Baghdad Medical Supplies","relevance":"General medical supplies; serves clinics and smaller hospitals","contact":"Contact via website","website":"—","latestTender":"Jun 2026 (private-clinic consumable tenders)","competitors":"International medical supplies; catheters","priority":"🟡 3/5"},{"num":1,"name":"Yousuf Mahmood Hussain Co. W.L.L (YMH)","relevance":"75+ years; NHRA-licensed importer/distributor; portfolio includes dialysis, cardiology, urology, surgical","contact":"☎️ +973 1717 5555 · ✉️ ae.reporting@ymh.com.bh","website":"YMH Bahrain","latestTender":"Aug 2026 (MOH/NGHA consumable frameworks)","competitors":"Global dialysis, cardiology, urology OEMs; HD catheters","priority":"🔴 5/5"},{"num":2,"name":"Sahha Tech Medical","relevance":"NHRA-accredited; supplies hospitals/clinics/labs across Bahrain & KSA; premium medical-equipment distributor","contact":"Contact via website","website":"Sahha Tech","latestTender":"Jul 2026 (private-hospital consumable tenders)","competitors":"International medical-equipment brands; catheters","priority":"🔴 5/5"},{"num":3,"name":"Glidden Medical Technologies W.L.L","relevance":"Trusted medical-equipment and healthcare-solutions provider; advanced medical/diagnostic technologies","contact":"☎️ +973 1776 4696 · ✉️ info@gliddenmedtech.com","website":"Glidden MedTech","latestTender":"Jun 2026 (private-hospital device/consumable tenders)","competitors":"Advanced medical/diagnostic technologies; catheters","priority":"🔴 5/5"},{"num":4,"name":"Manama Medical","relevance":"Medical-equipment supplier; broad hospital/clinic network","contact":"☎️ +973 1721 7078 · ✉️ sales@manamamedical.com","website":"Manama Medical","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Multi-brand medical equipment; catheters","priority":"🔴 5/5"},{"num":5,"name":"MedTreq","relevance":"NHRA-authorized to import/register/distribute medical devices and supplies; regional Gulf office in Bahrain","contact":"Contact via website","website":"MedTreq","latestTender":"Jul 2026 (MOH/NGHA consumable frameworks)","competitors":"NHRA-authorized international brands; catheters","priority":"🔴 5/5"},{"num":6,"name":"Gulf House Medical System","relevance":"Medical systems and equipment; hospital/clinic supply","contact":"☎️ +973 1741 1037 · ✉️ info@gulfhousemedical.com","website":"Gulf House Medical","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Global medical systems; catheters","priority":"🟠 4/5"},{"num":7,"name":"Wael Pharmacy Co. W.L.L","relevance":"Surgical & medical disposables; Umm Al Hassam base; serves hospitals and clinics","contact":"☎️ +973 1737 7000 · ✉️ sales@waelpharmacy.com","website":"Wael Pharmacy","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Surgical & medical disposables; multi-brand catheters","priority":"🟠 4/5"},{"num":8,"name":"Al Rabee Medical Equipment","relevance":"Medical-equipment distributor; broad consumables portfolio","contact":"✉️ info@alrabeemedical.com · ☎️ +973 1768 2710","website":"Al Rabee Medical","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"International medical-equipment brands; catheters","priority":"🟠 4/5"},{"num":9,"name":"Nova Med Bahrain","relevance":"Medical devices and consumables; hospital/clinic distribution","contact":"☎️ +973 1747 3310","website":"Nova Med BH","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"Multi-brand medical devices; catheters","priority":"🟠 4/5"},{"num":10,"name":"Inospire Medical","relevance":"Medical-equipment and healthcare solutions; serves private hospitals and clinics","contact":"☎️ +973 3833 7330","website":"Inospire Medical","latestTender":"Jun 2026 (private-hospital consumable tenders)","competitors":"International healthcare solutions; catheters","priority":"🟡 3/5"}]},"kols":{"sa":[{"num":1,"name":"Prof. Faissal A. M. Shaheen","relevance":"⭐⭐⭐⭐⭐ Nephrology / transplantation","specialty":"⭐⭐⭐⭐⭐ Nephrology / transplantation","institution":"Dr. Soliman Fakeeh Hospital / SCOT","contact":"✉️ famshaheen@gmail.com","extra":"—","extra_label":"Priority"},{"num":2,"name":"Prof. Abdullah Al-Hwiesh","relevance":"⭐⭐⭐⭐⭐ Nephrology / dialysis / vascular access","specialty":"⭐⭐⭐⭐⭐ Nephrology / dialysis / vascular access","institution":"King Fahd Hospital of the University / IAU","contact":"✉️ ahwiesh@iau.edu.sa","extra":"—","extra_label":"Priority"},{"num":3,"name":"Dr. Abdullah Al Sayyari","relevance":"⭐⭐⭐⭐⭐ Nephrology / dialysis","specialty":"⭐⭐⭐⭐⭐ Nephrology / dialysis","institution":"MNGHA / King Abdulaziz Medical City","contact":"MNGHA Nephrology Department","extra":"—","extra_label":"Priority"},{"num":4,"name":"Dr. Ali Alharbi","relevance":"⭐⭐⭐⭐⭐ Nephrology / dialysis","specialty":"⭐⭐⭐⭐⭐ Nephrology / dialysis","institution":"Diaverum Saudi Arabia","contact":"Professional profile","extra":"—","extra_label":"Priority"},{"num":5,"name":"Dr. Dujanah Hassan Mousa","relevance":"⭐⭐⭐⭐ Nephrology / dialysis","specialty":"⭐⭐⭐⭐ Nephrology / dialysis","institution":"Diaverum Saudi Arabia","contact":"Diaverum Saudi Arabia","extra":"—","extra_label":"Priority"},{"num":6,"name":"Dr. Mohammed Alhomrany","relevance":"⭐⭐⭐⭐ Nephrology / dialysis","specialty":"⭐⭐⭐⭐ Nephrology / dialysis","institution":"Diaverum Saudi Arabia","contact":"Diaverum Saudi Arabia","extra":"—","extra_label":"Priority"},{"num":7,"name":"Dr. Fayez Alhejaili","relevance":"⭐⭐⭐⭐ Nephrology / dialysis","specialty":"⭐⭐⭐⭐ Nephrology / dialysis","institution":"Diaverum Saudi Arabia","contact":"Diaverum Saudi Arabia","extra":"—","extra_label":"Priority"},{"num":8,"name":"Dr. Hassan Alshehri","relevance":"⭐⭐⭐⭐ Interventional Radiology","specialty":"⭐⭐⭐⭐ Interventional Radiology","institution":"Prince Sultan Military Medical City, Riyadh","contact":"Saudi Interventional Radiology Society","extra":"—","extra_label":"Priority"},{"num":9,"name":"Dr. Shaker Alshehri","relevance":"⭐⭐⭐⭐ Vascular & Interventional Radiology","specialty":"⭐⭐⭐⭐ Vascular & Interventional Radiology","institution":"King Abdulaziz Medical City, Riyadh","contact":"Saudi Interventional Radiology Society","extra":"—","extra_label":"Priority"},{"num":10,"name":"Dr. Shagran Binkhamis","relevance":"⭐⭐⭐⭐ Vascular & Interventional Radiology","specialty":"⭐⭐⭐⭐ Vascular & Interventional Radiology","institution":"King Faisal Specialist Hospital & Research Centre","contact":"Saudi Interventional Radiology Society","extra":"—","extra_label":"Priority"}],"ae":[{"num":1,"name":"Dr. Ayman Kamal Almadani","relevance":"Nephrology / dialysis leadership","specialty":"Nephrology / dialysis leadership","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":"—","extra_label":"Priority"},{"num":2,"name":"Dr. Wasim Ahmed","relevance":"Nephrology / advanced HD","specialty":"Nephrology / advanced HD","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":"—","extra_label":"Priority"},{"num":3,"name":"Dr. Salaheldin Khalil Issa","relevance":"Nephrology / advanced HD","specialty":"Nephrology / advanced HD","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":"—","extra_label":"Priority"},{"num":4,"name":"Dr. Hormaz Dara Dastoor","relevance":"Nephrology / advanced HD","specialty":"Nephrology / advanced HD","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":"—","extra_label":"Priority"},{"num":5,"name":"Dr. Mohammad Raafat Al Hakim","relevance":"Nephrology / dialysis / RRT","specialty":"Nephrology / dialysis / RRT","institution":"SEHA Kidney Care – Al Ain / Tawam","contact":"SEHA appointment/contact","extra":"—","extra_label":"Priority"},{"num":6,"name":"Dr. Anvar Hussain Hamid Khan","relevance":"Nephrology / vascular disease / HD","specialty":"Nephrology / vascular disease / HD","institution":"SEHA Kidney Care","contact":"☎️ 80050 / SEHA appointment","extra":"—","extra_label":"Priority"},{"num":7,"name":"Dr. Mohamed Hassan","relevance":"Nephrology / HD / PD / transplant","specialty":"Nephrology / HD / PD / transplant","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":"—","extra_label":"Priority"},{"num":8,"name":"Dr. Abraham George","relevance":"Nephrology / HD / vascular disease","specialty":"Nephrology / HD / vascular disease","institution":"SEHA Kidney Care – Al Ain","contact":"SEHA appointment/contact","extra":"—","extra_label":"Priority"},{"num":9,"name":"Dr. Hefsa Al Shamsi","relevance":"Nephrology / HD / transplantation","specialty":"Nephrology / HD / transplantation","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":"—","extra_label":"Priority"},{"num":10,"name":"Dr. Fadi Hijazi","relevance":"Nephrology","specialty":"Nephrology","institution":"Cleveland Clinic Abu Dhabi","contact":"Cleveland Clinic Abu Dhabi appointment","extra":"—","extra_label":"Priority"}],"qa":[{"num":1,"name":"Dr. Hassan Al-Malki","relevance":"⭐ Nephrology / dialysis leadership","specialty":"⭐ Nephrology / dialysis leadership","institution":"HMC","contact":"HMC +974 4439 5777","extra":"—","extra_label":"Priority"},{"num":2,"name":"Dr. Omar Fituri","relevance":"⭐ Nephrology / transplant / RRT","specialty":"⭐ Nephrology / transplant / RRT","institution":"HMC + Weill Cornell Medicine-Qatar","contact":"HMC / WCM-Q","extra":"—","extra_label":"Priority"},{"num":3,"name":"Dr. Muhammad Asim","relevance":"⭐ Senior nephrology / dialysis / CRRT","specialty":"⭐ Senior nephrology / dialysis / CRRT","institution":"HMC","contact":"HMC +974 4439 5777","extra":"—","extra_label":"Priority"},{"num":4,"name":"Dr. Ihab T. M. Elmadhoun","relevance":"⭐ Nephrology / CRRT / dialysis","specialty":"⭐ Nephrology / CRRT / dialysis","institution":"HMC","contact":"HMC +974 4439 5777","extra":"—","extra_label":"Priority"},{"num":5,"name":"Dr. Abdullah Ibrahim Hamad","relevance":"⭐ Nephrology / dialysis","specialty":"⭐ Nephrology / dialysis","institution":"HMC","contact":"HMC +974 4439 5777","extra":"—","extra_label":"Priority"},{"num":6,"name":"Dr. Muftah Othman","relevance":"⭐ Senior nephrology / dialysis","specialty":"⭐ Senior nephrology / dialysis","institution":"HMC","contact":"HMC +974 4439 5777","extra":"—","extra_label":"Priority"},{"num":7,"name":"Dr. Khaled Mahmoud","relevance":"⭐ Nephrology / dialysis","specialty":"⭐ Nephrology / dialysis","institution":"HMC","contact":"HMC +974 4439 5777","extra":"—","extra_label":"Priority"},{"num":8,"name":"Dr. Alaedine Shurrab","relevance":"⭐ Nephrology / renal replacement therapy","specialty":"⭐ Nephrology / renal replacement therapy","institution":"HMC / Al Khor Hospital","contact":"HMC +974 4439 5777","extra":"—","extra_label":"Priority"},{"num":9,"name":"Dr. Awais Nauman","relevance":"Nephrology / renal medicine","specialty":"Nephrology / renal medicine","institution":"HMC","contact":"HMC +974 4439 5777","extra":"—","extra_label":"Priority"},{"num":10,"name":"Dr. Ali A. Haydar","relevance":"⭐ Interventional radiology / vascular intervention","specialty":"⭐ Interventional radiology / vascular intervention","institution":"Aman Hospital","contact":"☎️ +974 4400 4400 · ✉️ [email protected]","extra":"—","extra_label":"Priority"}],"kw":[{"num":1,"name":"Prof. Hamed Al-Essa","relevance":"⭐ Nephrology / transplant / dialysis","specialty":"⭐ Nephrology / transplant / dialysis","institution":"Kuwait renal network","contact":"MOH / hospital","extra":"—","extra_label":"Priority"},{"num":2,"name":"Dr. Hamad Behbehani","relevance":"⭐ Nephrology / renal medicine","specialty":"⭐ Nephrology / renal medicine","institution":"Kuwait MOH","contact":"MOH / hospital","extra":"—","extra_label":"Priority"},{"num":3,"name":"Dr. Omar Al-Hunidi","relevance":"⭐ Nephrology / renal medicine","specialty":"⭐ Nephrology / renal medicine","institution":"Kuwait","contact":"Hospital / clinic","extra":"—","extra_label":"Priority"},{"num":4,"name":"Dr. Ahmed Ramadan","relevance":"Nephrology / renal medicine","specialty":"Nephrology / renal medicine","institution":"Amiri Hospital","contact":"MOH / Amiri","extra":"—","extra_label":"Priority"},{"num":5,"name":"Dr. Hisham Al-Sabah","relevance":"Nephrology / renal medicine","specialty":"Nephrology / renal medicine","institution":"Kuwait MOH","contact":"MOH","extra":"—","extra_label":"Priority"},{"num":6,"name":"Dr. Abdulaziz Al-Mousawi","relevance":"Nephrology / dialysis","specialty":"Nephrology / dialysis","institution":"Kuwait MOH","contact":"MOH / hospital","extra":"—","extra_label":"Priority"},{"num":7,"name":"Dr. Mohammed Al-Mousawi","relevance":"Nephrology / renal medicine","specialty":"Nephrology / renal medicine","institution":"Kuwait","contact":"MOH / hospital","extra":"—","extra_label":"Priority"},{"num":8,"name":"Dr. Khaled Al-Sabah","relevance":"Nephrology / renal medicine","specialty":"Nephrology / renal medicine","institution":"Kuwait","contact":"MOH / hospital","extra":"—","extra_label":"Priority"},{"num":9,"name":"Dr. Faisal Al-Rashidi","relevance":"Nephrology / dialysis","specialty":"Nephrology / dialysis","institution":"Kuwait","contact":"MOH / hospital","extra":"—","extra_label":"Priority"},{"num":10,"name":"Dr. Ahmed Al-Sabah","relevance":"Renal medicine / transplantation","specialty":"Renal medicine / transplantation","institution":"Kuwait","contact":"MOH / hospital","extra":"—","extra_label":"Priority"}],"om":[{"num":1,"name":"Dr. Dawood Al-Riyami","relevance":"⭐ Nephrology / dialysis","specialty":"⭐ Nephrology / dialysis","institution":"Sultan Qaboos University Hospital","contact":"✉️ dawood@squ.edu.om","extra":"—","extra_label":"Priority"},{"num":2,"name":"Dr. Ali Al Lawati","relevance":"⭐ Nephrology / dialysis","specialty":"⭐ Nephrology / dialysis","institution":"Sultan Qaboos University Hospital","contact":"✉️ aallawati@squ.edu.om","extra":"—","extra_label":"Priority"},{"num":3,"name":"Dr. Sadiq Al Lawati","relevance":"⭐ Senior Consultant Nephrologist","specialty":"⭐ Senior Consultant Nephrologist","institution":"Royal Hospital","contact":"Royal Hospital / MOH","extra":"—","extra_label":"Priority"},{"num":4,"name":"Dr. Issa Al Salmi","relevance":"⭐ Senior Consultant Nephrologist","specialty":"⭐ Senior Consultant Nephrologist","institution":"Royal Hospital","contact":"Royal Hospital / MOH","extra":"—","extra_label":"Priority"},{"num":5,"name":"Dr. Alan Hola","relevance":"⭐ Senior Consultant Nephrologist","specialty":"⭐ Senior Consultant Nephrologist","institution":"Royal Hospital","contact":"Royal Hospital / MOH","extra":"—","extra_label":"Priority"},{"num":6,"name":"Dr. Mahmood Nasser Al Hajiry","relevance":"⭐ IR / dialysis access / PermCath / PD catheter","specialty":"⭐ IR / dialysis access / PermCath / PD catheter","institution":"Royal Hospital","contact":"Aster / Royal Hospital","extra":"—","extra_label":"Priority"},{"num":7,"name":"Dr. Tamer Sayed Fouad","relevance":"⭐ Vascular & endovascular surgery / HD access","specialty":"⭐ Vascular & endovascular surgery / HD access","institution":"Burjeel Hospital Oman","contact":"Burjeel Hospital","extra":"—","extra_label":"Priority"},{"num":8,"name":"Dr. Said Al-Lamki","relevance":"⭐ Interventional Radiology / central venous catheter insertion","specialty":"⭐ Interventional Radiology / central venous catheter insertion","institution":"Burjeel Hospital Muscat","contact":"Burjeel Hospital","extra":"—","extra_label":"Priority"},{"num":9,"name":"Dr. Faisal Al Balushi","relevance":"Interventional Radiology","specialty":"Interventional Radiology","institution":"Royal Hospital","contact":"Oman Vascular Society / Royal Hospital","extra":"—","extra_label":"Priority"},{"num":10,"name":"Dr. Suliman Al Shamsi","relevance":"⭐ Senior Consultant Vascular Surgeon","specialty":"⭐ Senior Consultant Vascular Surgeon","institution":"Royal Hospital","contact":"Royal Hospital / MOH","extra":"—","extra_label":"Priority"}],"jo":[{"num":1,"name":"Prof. Riyad Abdel Raouf Saeed","relevance":"⭐ Nephrology / kidney transplantation","specialty":"⭐ Nephrology / kidney transplantation","institution":"Jordan Hospital","contact":"☎️ +962 6 560 8080","extra":"—","extra_label":"Priority"},{"num":2,"name":"Dr. Fouad Riad Saeed","relevance":"⭐ Nephrology / transplantation","specialty":"⭐ Nephrology / transplantation","institution":"Jordan Hospital","contact":"☎️ +962 6 560 8080 · ✉️ info@jordan-hospital.com","extra":"—","extra_label":"Priority"},{"num":3,"name":"Dr. Bisher Kawar","relevance":"⭐ Nephrology / dialysis / transplantation","specialty":"⭐ Nephrology / dialysis / transplantation","institution":"Abdali Hospital","contact":"☎️ +962 6 510 9999","extra":"—","extra_label":"Priority"},{"num":4,"name":"Dr. Hiba Barghouthi","relevance":"⭐ Nephrology","specialty":"⭐ Nephrology","institution":"Abdali Hospital","contact":"☎️ +962 6 510 9999","extra":"—","extra_label":"Priority"},{"num":5,"name":"Dr. Jawad Syouri","relevance":"⭐ Nephrology / kidney transplant","specialty":"⭐ Nephrology / kidney transplant","institution":"Ibn Al-Haytham Hospital","contact":"Hospital: +962 6 569 4420","extra":"—","extra_label":"Priority"},{"num":6,"name":"Dr. Ahmed Rashid","relevance":"⭐ Nephrology / internal medicine","specialty":"⭐ Nephrology / internal medicine","institution":"Al Khalidi Hospital","contact":"☎️ +962 6 464 4281","extra":"—","extra_label":"Priority"},{"num":7,"name":"Dr. Bashar Zuhair Ghosheh","relevance":"⭐ Vascular Surgery","specialty":"⭐ Vascular Surgery","institution":"Jordan Hospital","contact":"☎️ +962 6 560 8080","extra":"—","extra_label":"Priority"},{"num":8,"name":"Dr. Omar Nader Hamdallah","relevance":"⭐ Vascular surgery + catheterization + kidney transplant","specialty":"⭐ Vascular surgery + catheterization + kidney transplant","institution":"Jordan Hospital / Jordan Vascular Clinic","contact":"☎️ Hospital +962 6 560 8080","extra":"—","extra_label":"Priority"},{"num":9,"name":"Dr. Sizeph Haddad","relevance":"⭐ Vascular & Interventional Radiology","specialty":"⭐ Vascular & Interventional Radiology","institution":"Abdali Hospital","contact":"☎️ +962 6 510 9999","extra":"—","extra_label":"Priority"},{"num":10,"name":"Dr. Farid Al-Adham","relevance":"⭐ Interventional radiology / vascular catheter procedures","specialty":"⭐ Interventional radiology / vascular catheter procedures","institution":"Amman","contact":"Vezeeta / clinic","extra":"—","extra_label":"Priority"}],"lb":[{"num":1,"name":"Dr. Hicham Cheikh Hassan","relevance":"⭐ Nephrology / dialysis / renal vascular services","specialty":"⭐ Nephrology / dialysis / renal vascular services","institution":"LAU Medical Center","contact":"LAU Medicine","extra":"—","extra_label":"Priority"},{"num":2,"name":"Prof. Dania Chelala","relevance":"⭐ Nephrology / HD / transplantation","specialty":"⭐ Nephrology / HD / transplantation","institution":"Hôtel-Dieu de France","contact":"HDF","extra":"—","extra_label":"Priority"},{"num":3,"name":"Dr. Hiba Azar","relevance":"Nephrology / dialysis","specialty":"Nephrology / dialysis","institution":"Hôtel-Dieu de France","contact":"HDF","extra":"—","extra_label":"Priority"},{"num":4,"name":"Dr. Kassem Bdeiri","relevance":"Nephrology / dialysis","specialty":"Nephrology / dialysis","institution":"Hôtel-Dieu de France","contact":"HDF","extra":"—","extra_label":"Priority"},{"num":5,"name":"Dr. Majdi Hamedeh","relevance":"⭐ Nephrology + dialysis","specialty":"⭐ Nephrology + dialysis","institution":"Al Zahraa Hospital UMC","contact":"✉️ majdi.hmedeh@zhumc.org.lb · ☎️ +961 1 851040","extra":"—","extra_label":"Priority"},{"num":6,"name":"Dr. Lynn Bou Khalil","relevance":"⭐ Nephrology & Hypertension","specialty":"⭐ Nephrology & Hypertension","institution":"Mount Lebanon Hospital UMC","contact":"☎️ +961 25 957 000","extra":"—","extra_label":"Priority"},{"num":7,"name":"Prof. Jamal Hoballah","relevance":"⭐ Vascular surgery","specialty":"⭐ Vascular surgery","institution":"AUB Medical Center","contact":"AUB","extra":"—","extra_label":"Priority"},{"num":8,"name":"Dr. Fady Haddad","relevance":"⭐ Vascular Surgery","specialty":"⭐ Vascular Surgery","institution":"Mount Lebanon Hospital UMC","contact":"☎️ +961 25 957 000","extra":"—","extra_label":"Priority"},{"num":9,"name":"Dr. Abdallah Noufaily","relevance":"⭐ Interventional vascular/nonvascular radiology","specialty":"⭐ Interventional vascular/nonvascular radiology","institution":"LAU Medical Center","contact":"☎️ +961 1 200800 ext. 6979","extra":"—","extra_label":"Priority"},{"num":10,"name":"Dr. Hadi Khoury","relevance":"⭐ Interventional Radiology / vascular intervention","specialty":"⭐ Interventional Radiology / vascular intervention","institution":"Khoury Vascular Clinic","contact":"KVC","extra":"—","extra_label":"Priority"}],"iq":[{"num":1,"name":"Prof. Arif Sami Malik","relevance":"⭐ Nephrology / HD + PD","specialty":"⭐ Nephrology / HD + PD","institution":"Al-Nahrain University / Iraq","contact":"✉️ dr.arifsami@nahrainuniv.edu.iq","extra":"—","extra_label":"Priority"},{"num":2,"name":"Dr. Zaid Ali","relevance":"⭐ Vascular surgery / angiography / angioplasty","specialty":"⭐ Vascular surgery / angiography / angioplasty","institution":"Ministry of Health, Al-Muthanna","contact":"PAIRS physician directory","extra":"—","extra_label":"Priority"},{"num":3,"name":"Dr. Fadhil Al-Ammar","relevance":"Medical/academic leadership","specialty":"Medical/academic leadership","institution":"Founder, Nova Scientific Bureau","contact":"Nova Scientific Bureau","extra":"—","extra_label":"Priority"},{"num":4,"name":"Dr. Abdul-Hadi Al-Hassan","relevance":"Nephrology / renal medicine","specialty":"Nephrology / renal medicine","institution":"Iraqi nephrology network","contact":"Hospital/professional route","extra":"—","extra_label":"Priority"},{"num":5,"name":"Dr. Ahmed Al-Jubouri","relevance":"Nephrology / dialysis","specialty":"Nephrology / dialysis","institution":"Iraqi renal-care network","contact":"Hospital/professional route","extra":"—","extra_label":"Priority"},{"num":6,"name":"Dr. Ali Al-Mashhadani","relevance":"Nephrology / dialysis","specialty":"Nephrology / dialysis","institution":"Baghdad","contact":"Hospital/professional route","extra":"—","extra_label":"Priority"},{"num":7,"name":"Dr. Raad Al-Khafaji","relevance":"Vascular surgery","specialty":"Vascular surgery","institution":"Baghdad / MOH","contact":"Hospital/professional route","extra":"—","extra_label":"Priority"},{"num":8,"name":"Dr. Haider Al-Saadi","relevance":"Interventional radiology","specialty":"Interventional radiology","institution":"Baghdad","contact":"Hospital/professional route","extra":"—","extra_label":"Priority"},{"num":9,"name":"Dr. Mohammed Al-Taie","relevance":"Interventional radiology / vascular intervention","specialty":"Interventional radiology / vascular intervention","institution":"Baghdad","contact":"Hospital/professional route","extra":"—","extra_label":"Priority"},{"num":10,"name":"Dr. Ahmed Al-Bayati","relevance":"Vascular / endovascular surgery","specialty":"Vascular / endovascular surgery","institution":"Iraq","contact":"Hospital/professional route","extra":"—","extra_label":"Priority"}],"bh":[{"num":1,"name":"Dr. Issa Kawalit","relevance":"⭐ Nephrology + dialysis + transplant","specialty":"⭐ Nephrology + dialysis + transplant","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"—","extra_label":"Priority"},{"num":2,"name":"Dr. Abdulraqeeb Alomari","relevance":"⭐ Nephrologist + kidney transplant","specialty":"⭐ Nephrologist + kidney transplant","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"—","extra_label":"Priority"},{"num":3,"name":"Dr. Muhand Salemah Raji Eltwal","relevance":"⭐ Nephrology","specialty":"⭐ Nephrology","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"—","extra_label":"Priority"},{"num":4,"name":"Dr. Ahmed Mordi","relevance":"⭐ Interventional Radiology + dialysis access","specialty":"⭐ Interventional Radiology + dialysis access","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800 · WhatsApp +973 3218 1810","extra":"—","extra_label":"Priority"},{"num":5,"name":"Dr. Wadie Yousif","relevance":"⭐ Vascular & Interventional Radiology","specialty":"⭐ Vascular & Interventional Radiology","institution":"Ibn Al-Nafees Hospital","contact":"☎️ +973 1782 8282 / 1782 8253","extra":"—","extra_label":"Priority"},{"num":6,"name":"Dr. Sharif Abdulsalam Hamza Khashaba","relevance":"⭐ Vascular Surgery","specialty":"⭐ Vascular Surgery","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"—","extra_label":"Priority"},{"num":7,"name":"Dr. Sawsan Kadhem","relevance":"Interventional Radiology","specialty":"Interventional Radiology","institution":"Dawali Clinics / Salmaniya","contact":"Hospital/clinic route","extra":"—","extra_label":"Priority"},{"num":8,"name":"Dr. Jinane Khaled","relevance":"Radiology","specialty":"Radiology","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"—","extra_label":"Priority"},{"num":9,"name":"Dr. Suzanne Abbas","relevance":"Radiology","specialty":"Radiology","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"—","extra_label":"Priority"},{"num":10,"name":"Dr. Fatema Abdulrahman","relevance":"Radiology","specialty":"Radiology","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"—","extra_label":"Priority"}]}}

const networkCountryMeta = {
  sa:{name:'Saudi Arabia',flag:'🇸🇦'}, ae:{name:'UAE',flag:'🇦🇪'}, qa:{name:'Qatar',flag:'🇶🇦'},
  kw:{name:'Kuwait',flag:'🇰🇼'}, om:{name:'Oman',flag:'🇴🇲'}, bh:{name:'Bahrain',flag:'🇧🇭'},
  jo:{name:'Jordan',flag:'🇯🇴'}, lb:{name:'Lebanon',flag:'🇱🇧'}, iq:{name:'Iraq',flag:'🇮🇶'}
};

function networkPriorityClass(v){
  const s=String(v||'');
  if(!s) return 'mid';
  return (s.includes('5/5')||s.includes('5'))?'high':'mid';
}

function openNetwork(type,code){
  const meta=networkCountryMeta[code], d=countryData[code];
  const page=document.getElementById('page-'+type+'-'+code);
  if(!meta||!d||!page)return;
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  page.classList.add('active');
  page.style.setProperty('--net-primary',d.colors.primary);
  page.style.setProperty('--net-accent',d.colors.accent);
  page.style.setProperty('--net-secondary',d.colors.secondary);
  const rows=(networkData[type]&&networkData[type][code])||[];
  const isDist=type==='distributors';
  const label=isDist?'Distributors':'KOLs';
  const icon=isDist?'🤝':'⭐';
  const searchId='network-search-'+type+'-'+code;
  const tableId='network-table-'+type+'-'+code;
  page.innerHTML=`
    <div class="network-shell network-table-only">
      <div class="network-table-wrap">
        <div class="network-table-header">
          <div><div class="network-table-title">${icon} ${label} — ${meta.name}</div><div class="network-table-subtitle">${rows.length} records from the workbook · ${isDist?'Distributors':'KOL_Catalog'} sheet</div></div>
          <input id="${searchId}" class="network-search" type="text" placeholder="🔎 Search ${isDist?'distributor, relevance, supplier or tender':'KOL, specialty, institution or contact'}..." oninput="filterNetworkTable('${type}','${code}')">
        </div>
        <div class="network-table-scroll">
          <table class="network-table" id="${tableId}">
            <thead><tr>
              <th>#</th><th>${isDist?'Distributor':'KOL'}</th><th>${isDist?'AMECATH Relevance':'Specialty'}</th>
              ${isDist?'<th>Latest Tender Date</th><th>Competitors / Suppliers</th><th>Website</th><th>Priority</th><th>Contact</th>':'<th>Institution</th><th>Priority</th><th>Contact</th>'}
            </tr></thead>
            <tbody>
            ${rows.map(r=>{
              const priority=String(r.priority||r.extra||'—');
              const search=[r.name,r.relevance,r.specialty,r.institution,r.contact,r.website,r.latestTender,r.competitors,priority].filter(Boolean).join(' ').toLowerCase();
              return `<tr data-search="${search.replace(/"/g,'&quot;')}">
                <td class="network-table-num">${r.num||'—'}</td>
                <td><div class="network-table-name">${r.name||'—'}</div></td>
                <td><div class="network-table-main">${isDist?(r.relevance||'—'):(r.specialty||'—')}</div></td>
                ${isDist?`<td><div class="network-table-main">${r.latestTender||'—'}</div></td><td><div class="network-extra">${r.competitors||'—'}</div></td><td><div class="network-table-main">${r.website||'—'}</div></td><td><span class="network-priority ${networkPriorityClass(priority)}">${priority}</span></td><td><div class="network-contact-cell">${r.contact||'—'}</div></td>`:`<td><div class="network-table-main">${r.institution||'—'}</div></td><td><span class="network-priority ${networkPriorityClass(priority)}">${priority}</span></td><td><div class="network-contact-cell">${r.contact||'—'}</div></td>`}
              </tr>`;
            }).join('')||`<tr><td colspan="${isDist?8:6}" class="network-empty">No records available for this country.</td></tr>`}
            </tbody>
          </table>
        </div>
        <div class="network-table-footer"><span>Showing ${rows.length} ${label.toLowerCase()}</span><span>Source: ${isDist?'Distributors':'KOL_Catalog'} sheet</span></div>
      </div>
    </div>`;
  window.scrollTo({top:0,behavior:'smooth'});
}
window.openNetwork=openNetwork;
function filterNetworkTable(type,code){const input=document.getElementById(`network-search-${type}-${code}`);const table=document.getElementById(`network-table-${type}-${code}`);if(!input||!table)return;const q=input.value.trim().toLowerCase();table.querySelectorAll('tbody tr').forEach(tr=>{const t=(tr.getAttribute('data-search')||'').toLowerCase();tr.style.display=!q||t.includes(q)?'':'none';});}
window.filterNetworkTable=filterNetworkTable;

function openCountry(code){
  const d = countryData[code];
  const page = document.getElementById('page-countries');
  if(!d || !page) return;

  const old = document.getElementById('country-inline-detail');
  if(old) old.remove();

  // Apply the selected country's flag colors to the Country Analysis page.
  page.classList.add('country-theme');
  page.dataset.selectedCountry = code;
  page.style.setProperty('--country-primary', d.colors.primary);
  page.style.setProperty('--country-secondary', d.colors.secondary);
  page.style.setProperty('--country-accent', d.colors.accent);

  // Make the selected country card visibly active.
  document.querySelectorAll('#page-countries .c-card').forEach(function(card){
    card.classList.toggle('active', card.getAttribute('data-country') === code);
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
        ${d.kpi.map(k=>`
          <div class="cid-kpi">
            <div class="cid-kpi-label">${k.l}</div>
            <div class="cid-kpi-value">${k.v}</div>
          </div>
        `).join('')}
      </div>

      <div class="cid-network">
        <div class="cid-network-card" role="button" tabindex="0"
             onclick="openNetwork('distributors','${code}')"
             onkeydown="if(event.key==='Enter'||event.key===' ') {event.preventDefault();openNetwork('distributors','${code}')}">
          <div>
            <div class="cid-network-label">🤝 Distributors</div>
            <div class="cid-network-sub">Click to open ${d.name} distributor intelligence</div>
          </div>
          <div class="cid-network-value">${distributors} <span style="font-size:16px;opacity:.7">›</span></div>
        </div>
        <div class="cid-network-card" role="button" tabindex="0"
             onclick="openNetwork('kols','${code}')"
             onkeydown="if(event.key==='Enter'||event.key===' ') {event.preventDefault();openNetwork('kols','${code}')}">
          <div>
            <div class="cid-network-label">⭐ KOLs</div>
            <div class="cid-network-sub">Click to open ${d.name} KOL intelligence</div>
          </div>
          <div class="cid-network-value">${kols} <span style="font-size:16px;opacity:.7">›</span></div>
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
    delete page.dataset.selectedCountry;
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
function renderCompetitors(){const country=competitorCountries[selectedCompetitorCountry],header=document.getElementById('competitor-country-header'),grid=document.getElementById('comp-grid');if(!header||!grid)return;const list=competitorData[selectedCompetitorCountry]||[];header.innerHTML=`<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3"><div><div class="comp-country-title">${country.flag} ${country.name}</div><div class="comp-country-sub">${country.market} · Source: Competitor_Matrix</div></div><div class="comp-summary"><div class="comp-summary-pill">🏢 ${list.length} Competitors</div><div class="comp-summary-pill">👥 HD ${country.hd.toLocaleString()}</div><div class="comp-summary-pill">💉 Demand ${country.demand.toLocaleString()}</div><div class="comp-summary-pill">💰 Market $${country.marketValue}M</div></div></div>`;grid.innerHTML=list.map((c,i)=>{const id='comp-detail-'+selectedCompetitorCountry+'-'+i;return `<div class="comp-card-new"><div class="comp-card-topline" style="background:#3b82f6;"></div><div class="flex justify-between items-start gap-3"><div><div class="comp-card-company">${c.name}</div><div class="comp-card-origin">${c.coverage}</div></div></div><div class="comp-mini-grid"><div class="comp-mini-box"><span class="comp-mini-label">Main Advantage</span><span class="comp-mini-text">${c.advantage}</span></div><div class="comp-mini-box"><span class="comp-mini-label">Weakness / Gap</span><span class="comp-mini-text">${c.weakness}</span></div></div><div class="comp-edge"><b>Specializes in:</b> ${c.specializes}</div><button class="comp-details-btn" onclick="toggleCompetitorDetails('${id}',this)">View Details ↓</button><div class="comp-details-panel" id="${id}"><div class="comp-detail-row"><span class="comp-detail-label">Company</span><span class="comp-detail-value">${c.name}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Market Share*</span><span class="comp-detail-value">${c.share}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Coverage</span><span class="comp-detail-value">${c.coverage}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Main Advantage</span><span class="comp-detail-value">${c.advantage}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Specializes in</span><span class="comp-detail-value">${c.specializes}</span></div><div style="margin-top:8px;color:#34d399;font-size:10px;line-height:1.45;"><b>AMECATH Competitive Advantage:</b> ${c.edge}</div></div></div>`;}).join('')||'<div class="placeholder-page">No competitor data available for this country.</div>'; }
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

// ROBUST SIDEBAR NAVIGATION
// Use delegated events + explicit pointer handling so the sidebar keeps working
// even when other dashboard components are dynamically re-rendered.
window.navigate = navigate;
window.openCountry = openCountry;
window.closeCountry = closeCountry;

function initSidebarNavigation(){
  var sidebar = document.querySelector('.sidebar');
  if(!sidebar || sidebar.dataset.navReady === '1') return;
  sidebar.dataset.navReady = '1';
  sidebar.style.pointerEvents = 'auto';
  sidebar.style.position = 'sticky';
  sidebar.style.zIndex = '99999';

  sidebar.addEventListener('click', function(e){
    var item = e.target.closest('.nav-item[data-page]');
    if(!item) return;
    e.preventDefault();
    e.stopPropagation();
    navigate(item, item.getAttribute('data-page'));
  }, true);

  sidebar.addEventListener('keydown', function(e){
    var item = e.target.closest('.nav-item[data-page]');
    if(!item) return;
    if(e.key === 'Enter' || e.key === ' '){
      e.preventDefault();
      e.stopPropagation();
      navigate(item, item.getAttribute('data-page'));
    }
  }, true);
}

if(document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initSidebarNavigation);
} else {
  initSidebarNavigation();
}

// Also expose a simple direct handler for debugging / future buttons.
window.sidebarGo = function(pageId){
  var item = document.querySelector('.nav-item[data-page="'+pageId+'"]');
  if(item) navigate(item, pageId);
};
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
/* ─── SOURCES PAGE ─── */
(function(){
  var officialRows=[
    {country:'🇸🇦 Saudi Arabia', authority:'Ministry of Health (MOH) KSA + SFDA',              data:'HD patient count, facility numbers, HD machines, market authorization', portal:'moh.gov.sa / sfda.gov.sa'},
    {country:'🇸🇦 Saudi Arabia', authority:'NUPCO (National Unified Procurement Company)',       data:'Tender framework data, procurement volumes, tender pipeline',             portal:'nupco.com / etimad.sa'},
    {country:'🇦🇪 UAE',          authority:'MOHAP + DHA + DOH Abu Dhabi',                        data:'HD facility count, patient registry, Rafed GPO procurement data',        portal:'mohap.gov.ae / dha.gov.ae'},
    {country:'🇶🇦 Qatar',        authority:'Hamad Medical Corporation (HMC) + MOH Qatar',        data:'Patient volumes, dialysis capacity, HMC annual report 2024–2025',        portal:'hamad.qa / moph.gov.qa'},
    {country:'🇰🇼 Kuwait',       authority:'MOH Kuwait — Central Procurement',                   data:'Dialysis facility count, patient estimates, tender data',                 portal:'moh.gov.kw'},
    {country:'🇴🇲 Oman',         authority:'MOH Oman (Medical Store — Central)',                  data:'HD patient registry, dialysis centers, annual consumables procurement',   portal:'moh.gov.om'},
    {country:'🇧🇭 Bahrain',       authority:'NHRA (National Health Regulatory Authority) + MOH', data:'Medical device registration, HD facility data, BDF hospital data',        portal:'nhra.bh / moh.gov.bh'},
    {country:'🇯🇴 Jordan',        authority:'MOH Jordan + Royal Medical Services (RMS)',          data:'HD patient count, dialysis centers, public procurement',                  portal:'moh.gov.jo / rms.gov.jo'},
    {country:'🇱🇧 Lebanon',       authority:'MOH Lebanon',                                        data:'Hospital catheter supply, public dialysis network data',                  portal:'moph.gov.lb'},
    {country:'🇮🇶 Iraq',          authority:'Kimadia (MOH Iraq) + Regional Health Directorates',  data:'Bulk catheter demand, dialysis center count, tender volumes',             portal:'kimadia.gov.iq'},
  ];

  var marketRows=[
    {source:'Grand View Research',          report:'Hemodialysis Catheter Market — GCC & Middle East',         applied:'Market size, competitor share estimates, CAGR projections', year:'2024–2025'},
    {source:'BusinessWire / PR Newswire',   report:'Fresenius, B. Braun, Baxter GCC market announcements',     applied:'Competitor market share cross-validation (KSA)',              year:'2024–2026'},
    {source:'USRDS (US Renal Data System)', report:'International Comparisons of ESRD Care',                   applied:'HD patient prevalence benchmarking per 1M population',        year:'2023–2024'},
    {source:'ERA-EDTA Registry',            report:'European & Global Dialysis Report',                        applied:'PD/HD patient ratio benchmarks; facility utilization rates',  year:'2023'},
    {source:'GlobalTenders / TenderImpulse',report:'GCC & MENA dialysis tender database',                     applied:'Pipeline tender discovery (Qatar, Oman, Jordan)',             year:'2025–2026'},
    {source:'Scribd / NUPCO Portal',        report:'NPT0048-22 Medtronic NUPCO tender award documentation',   applied:'KSA competitor tender win intelligence',                      year:'2026'},
    {source:'Saudi Healthcare Consulting',  report:'SEHA dialysis market analysis',                            applied:'UAE HD machines + consumables market sizing',                 year:'2024'},
    {source:'Diaverum Annual Report',       report:'Diaverum GCC Dialysis Network 2025',                       applied:'KSA HD patient count cross-validation (30,000)',              year:'2025'},
    {source:'IDA (International Dialysis)', report:'Global Dialysis Market Outlook — Middle East',             applied:'Country-level growth rates, new center projections',           year:'2024'},
    {source:'World Bank / UN Data',         report:'Population projections 2026 — MENA region',               applied:'Population 2026 figures for all 9 markets',                   year:'2026'},
    {source:'AMECATH Internal Research',    report:'Field Survey — Distributor & KOL Mapping 2026',           applied:'Distributor lists, KOL profiles, contact data',               year:'2026'},
    {source:'AMECATH Internal Research',    report:'Competitor Intelligence Matrix 2026',                      applied:'Competitor strengths, weaknesses, market share estimates',    year:'2026'},
  ];

  var portalRows=[
    {platform:'NUPCO Etimad Portal',           country:'🇸🇦 Saudi Arabia', use:'Active tender monitoring, framework awards, emergency lots',                       url:'etimad.sa'},
    {platform:'INUPCO e-Marketplace',          country:'🇸🇦 Saudi Arabia', use:'Rolling general medical supplies tenders (weekly updates)',                        url:'nupco.com/inupco'},
    {platform:'HMC Procurement Portal',        country:'🇶🇦 Qatar',        use:'Annual consumables framework, quotation invitations, award notices',              url:'hamad.qa/procurement'},
    {platform:'DAHC / Dubai Academic Health',  country:'🇦🇪 UAE',          use:'5-year blanket renewal tracking, rolling RFQ monitoring',                         url:'dahc.ae'},
    {platform:'Monaqasat (MOH Qatar)',         country:'🇶🇦 Qatar',        use:'MOH Qatar periodic medical supply tenders',                                        url:'monaqasat.moph.gov.qa'},
    {platform:'Kimadia MOH Iraq',              country:'🇮🇶 Iraq',         use:'Bulk CVC/dialysis catheter procurement; rolling framework tenders',               url:'kimadia.gov.iq'},
  ];

  function srcRow(cells, alt){
    var tr=document.createElement('tr');
    tr.style.cssText='border-bottom:1px solid #14284b;transition:background .15s;';
    tr.onmouseenter=function(){tr.style.background='#13274c';};
    tr.onmouseleave=function(){tr.style.background='';};
    tr.innerHTML=cells.map(function(c,i){
      return '<td style="padding:11px 16px;color:'+(i===0?'#e8edf5':'#94a8c4')+';font-size:11px;'+(i===0?'font-weight:600;':'')+'">' + c + '</td>';
    }).join('');
    return tr;
  }

  var ob=document.getElementById('src-official-body');
  if(ob) officialRows.forEach(function(r){
    ob.appendChild(srcRow([r.country, r.authority, r.data,
      '<span style="color:#60a5fa;font-size:10px;">'+r.portal+'</span>']));
  });

  var mb=document.getElementById('src-market-body');
  if(mb) marketRows.forEach(function(r){
    mb.appendChild(srcRow([r.source, r.report, r.applied,
      '<span style="color:#a78bfa;font-size:10px;">'+r.year+'</span>']));
  });

  var pb=document.getElementById('src-portal-body');
  if(pb) portalRows.forEach(function(r){
    pb.appendChild(srcRow([r.platform, r.country, r.use,
      '<span style="color:#34d399;font-size:10px;">'+r.url+'</span>']));
  });
})();
/* ─── END SOURCES ─── */
</script>
</body>
</html>
"""
components.html(dashboard_html, height=1080, scrolling=True)
