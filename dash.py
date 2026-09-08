import streamlit as st
import streamlit.components.v1 as components

import json
import re
from pathlib import Path
import openpyxl

WORKBOOK_CANDIDATES = ["Amecath Dash.xlsx","Amecath Dash.xlsx","Amecath Dash.xlsx"]
WORKBOOK_PATH = next((Path(__file__).with_name(name) for name in WORKBOOK_CANDIDATES if Path(__file__).with_name(name).exists()), None)
if WORKBOOK_PATH is None:
    st.error("Workbook not found. Add the Amecath Dash Excel file next to dash.py.")
    st.stop()

_wb = openpyxl.load_workbook(WORKBOOK_PATH, data_only=True)

def _country_code(label):
    s = re.sub(r"^[^\\w]+", "", str(label or ""))
    return {"Saudi Arabia":"sa","UAE":"ae","Qatar":"qa","Kuwait":"kw","Oman":"om",
            "Jordan":"jo","Lebanon":"lb","Iraq":"iq","Bahrain":"bh"}.get(s)

_macro = {}
for row in _wb["Macro_Summary"].iter_rows(min_row=2, max_row=10, values_only=True):
    code = _country_code(row[1])
    if code:
        _macro[code] = {"country":row[1],"population":row[2],"hd":row[3],"pd":row[4],
            "annual_growth":row[5],"facilities":row[6],"hospital_growth":row[7],"unit_growth":row[8],
            "nephrologists":row[9],"vascular_surgeons":row[10],"radiologists":row[11],"machines":row[12],
            "demand":row[13],"market_value":row[14],"coverage":row[15],"oop":row[16],
            "distributors":row[17],"kols":row[18]}

_cmap={"SAUDI ARABIA":"sa","UAE":"ae","QATAR":"qa","KUWAIT":"kw","OMAN":"om",
       "JORDAN":"jo","LEBANON":"lb","IRAQ":"iq","BAHRAIEN":"bh","BAHRAIN":"bh"}
_comp={}
_cr=list(_wb["Competitor_Matrix"].iter_rows(values_only=True))
for i,row in enumerate(_cr):
    key=str(row[0]).strip().upper() if row[0] else ""
    if key in _cmap:
        arr=[]
        for rr in _cr[i+2:]:
            k=str(rr[0]).strip().upper() if rr[0] else ""
            if not rr[0] or k in _cmap or k=="#": break
            share = str(rr[1] or "")
            nums = re.findall(r"(\d+(?:\.\d+)?)", share.replace("–","-"))
            share_mid = ((float(nums[0]) + float(nums[1])) / 2) if len(nums) >= 2 else (float(nums[0]) if len(nums)==1 and "%" in share else None)
            arr.append({"name":rr[0],"share":rr[1],"share_mid":share_mid,"coverage":rr[2],"weakness":rr[3],
                        "advantage":rr[4],"specializes":rr[5],"edge":rr[6]})
        _comp[_cmap[key]]=arr

_tenders=[]
for row in _wb["Financials_Tenders"].iter_rows(min_row=2,max_row=21,values_only=True):
    if row[0]:
        pub=row[5].strftime("%d-%b-%Y") if hasattr(row[5],"strftime") else str(row[5])
        _tenders.append({"id":row[0],"country":row[1],"name":row[2],"ref":str(row[3]),
            "authority":row[4],"published":pub,"deadline":str(row[6]),"status":row[7],
            "value":row[8],"notes":row[9],"priority":row[10]})

_hot=[]
_hw=_wb["Hot_Areas"]; _hh=[str(x) for x in next(_hw.iter_rows(values_only=True))]
for row in _hw.iter_rows(min_row=2,max_row=11,values_only=True):
    for idx,cell in enumerate(row[1:],1):
        if cell and str(cell).strip()!="–": _hot.append({"rank":row[0],"country":_hh[idx],"area":str(cell)})

_our_asp=[]
for row in _wb["our ASP"].iter_rows(min_row=2,max_row=10,values_only=True):
    if row[0]: _our_asp.append({"country":row[0],"short":row[1],"mid":row[2],"long":row[3]})
_comp_asp=[]
for row in _wb["Competitor_Aspiration"].iter_rows(min_row=2,values_only=True):
    if row[0]: _comp_asp.append({"company":row[0],"region":row[1],"short":row[2],"long":row[3],"notes":row[4]})
# Forecast data from Forecast_Data sheet (country-level Base Case revenue).
# The country rows in the workbook provide the 2026/2027/2028 Base Case revenue
# used by the filterable chart below.
_forecast_base_case = {
    "Saudi Arabia": (85361, 149466, 219841),
    "Iraq": (26801, 47612, 71049),
    "Jordan": (16788, 29395, 43236),
    "Lebanon": (12380, 21573, 31576),
    "Bahrain": (13085, 23024, 34029),
    "Oman": (6903, 12146, 17951),
    "UAE": (8914, 15759, 23404),
    "Kuwait": (6470, 11329, 16663),
    "Qatar": (3743, 6617, 9827),
}
_forecast_countries = [
    {"country":_name, "code":_country_code(_name),
     "revenue_2026":_vals[0], "revenue_2027":_vals[1], "revenue_2028":_vals[2]}
    for _name,_vals in _forecast_base_case.items()
]

WORKBOOK_DATA={"macro":_macro,"competitors":_comp,"tenders":_tenders,"hotAreas":_hot,
               "ourASP":_our_asp,"competitorASP":_comp_asp,"forecast":{"countries":_forecast_countries}}


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


/* Country detail: macro intelligence + competitor share chart */
.cid-macro-section{margin-top:18px}.cid-section-head{display:flex;align-items:end;justify-content:space-between;gap:12px;margin-bottom:10px}.cid-section-title{font-size:14px;font-weight:900;color:#eef5ff}.cid-section-sub{font-size:10px;color:#7890b1;margin-top:3px}.cid-macro-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.cid-macro-card{position:relative;background:linear-gradient(145deg,#102443,#0b1a31);border:1px solid #254d82;border-top:3px solid var(--country-accent,#60a5fa);border-radius:12px;padding:14px 13px;min-height:82px;box-shadow:0 8px 18px rgba(0,0,0,.14);transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}.cid-macro-card:hover{transform:translateY(-2px);border-color:var(--country-accent,#60a5fa);box-shadow:0 0 22px color-mix(in srgb,var(--country-primary,#3b82f6) 20%,transparent)}.cid-macro-card .cid-kpi-label{font-size:9px;color:#7f9cc2;text-transform:uppercase;letter-spacing:.07em;font-weight:700}.cid-macro-card .cid-kpi-value{font-size:19px;font-weight:900;color:#f2f7ff;margin-top:7px;word-break:break-word;line-height:1.15}.cid-chart-row{display:grid;grid-template-columns:minmax(130px,220px) 1fr 58px;gap:10px;align-items:center;margin:9px 0}.cid-chart-name{font-size:10px;color:#dce8f8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.cid-chart-track{height:9px;background:#142946;border-radius:999px;overflow:hidden}.cid-chart-bar{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--country-primary,#3b82f6),var(--country-accent,#60a5fa));min-width:2px}.cid-chart-value{text-align:right;font-size:10px;font-weight:900;color:#8fc0ff}.cid-chart-note{font-size:9px;color:#657d9e;margin-top:10px}.cid-chart-empty{padding:18px;color:#7187a7;font-size:11px;text-align:center}@media(max-width:900px){.cid-macro-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.cid-chart-row{grid-template-columns:105px 1fr 50px}}@media(max-width:520px){.cid-macro-grid{grid-template-columns:1fr 1fr}.cid-macro-card{padding:11px;min-height:72px}.cid-macro-card .cid-kpi-value{font-size:15px}.cid-chart-row{grid-template-columns:88px 1fr 46px;gap:6px}.cid-chart-name,.cid-chart-value{font-size:9px}}

/* Distributors / KOLs table */
.network-table-wrap{margin:0 20px 20px;background:#0b1830;border:1px solid #1b3a67;border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.network-table-header{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:16px 18px;background:linear-gradient(135deg,color-mix(in srgb,var(--net-primary) 14%,#0b1830),#0b1830);border-bottom:1px solid #1b3a67}
.network-table-title{color:#f1f5f9;font-size:14px;font-weight:800}.network-table-subtitle{color:#6f89ad;font-size:9px;margin-top:4px}
.network-search{width:310px;max-width:42%;padding:10px 13px;border-radius:9px;border:1px solid #294c7a;background:#071326;color:#e5edf8;outline:none;font-size:10px}.network-search::placeholder{color:#587292}.network-search:focus{border-color:var(--net-accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--net-accent) 15%,transparent)}
.network-table-scroll{width:100%;overflow-x:auto}.network-table{width:100%;border-collapse:collapse;min-width:850px}.network-table thead th{padding:11px 13px;background:#071326;color:#7893b9;border-bottom:1px solid #1b3a67;text-align:left;font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:.7px;white-space:nowrap}.network-table tbody td{padding:13px;color:#dce6f4;border-bottom:1px solid #152c4d;vertical-align:middle;font-size:10px}.network-table tbody tr{transition:.15s ease}.network-table tbody tr:hover{background:color-mix(in srgb,var(--net-primary) 7%,#0b1830)}.network-table tbody tr:last-child td{border-bottom:none}.network-table-num{width:45px;color:var(--net-accent)!important;font-weight:800;text-align:center}.network-table-name{color:#fff;font-size:11px;font-weight:800;min-width:150px}.network-table-main{color:#c7d5e8;line-height:1.5;min-width:170px}.network-contact-cell{color:#9eb2cc;line-height:1.5;min-width:190px;word-break:break-word}.network-priority{display:inline-flex;align-items:center;justify-content:center;padding:4px 9px;border-radius:7px;white-space:nowrap;font-size:9px;font-weight:800;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.10)}.network-empty{text-align:center!important;padding:35px!important;color:#607a9f!important}.network-table-footer{display:flex;align-items:center;justify-content:space-between;padding:10px 15px;background:#071326;border-top:1px solid #152c4d;color:#536e92;font-size:9px}@media(max-width:700px){.network-table-header{align-items:stretch;flex-direction:column}.network-search{width:100%;max-width:none}.network-table-wrap{margin-left:12px;margin-right:12px}.network-table-footer{flex-direction:column;align-items:flex-start;gap:5px}}
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
 .cid-macro-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}.cid-kpi-grid + .cid-macro-grid{margin-top:14px}@media (max-width:1000px){.cid-macro-grid{grid-template-columns:repeat(2,1fr)}}@media (max-width:600px){.cid-macro-grid{grid-template-columns:1fr}}
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
.hot-label { background:#0b1628 !important; border:1px solid #2d5a91 !important; color:#e8edf5 !important; font-size:10px; font-weight:700; padding:3px 6px !important; border-radius:6px; box-shadow:0 3px 10px rgba(0,0,0,.25); }
.hot-label:before { border-top-color:#2d5a91 !important; }
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

/* FINAL UI OVERRIDES */
.cid-kpi-grid-final{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:10px!important;width:100%!important;margin:0!important;padding:0!important;}
.cid-kpi-card-final{display:flex!important;align-items:center!important;gap:12px!important;min-width:0!important;min-height:96px!important;padding:13px 14px!important;background:linear-gradient(145deg,#0d2a4d,#071a33)!important;border:1px solid color-mix(in srgb,var(--country-primary,#1683ff) 75%,#24517d)!important;border-radius:13px!important;box-shadow:0 7px 18px rgba(0,0,0,.22)!important;transition:.18s ease!important;}
.cid-kpi-card-final:hover{transform:translateY(-2px)!important;border-color:var(--country-accent,#22d3ee)!important;}
.cid-kpi-icon-final{width:46px!important;height:46px!important;min-width:46px!important;display:flex!important;align-items:center!important;justify-content:center!important;border-radius:50%!important;font-size:21px!important;background:radial-gradient(circle at 35% 30%,color-mix(in srgb,var(--country-primary,#1683ff) 92%,#fff),color-mix(in srgb,var(--country-primary,#1683ff) 45%,#06172c))!important;border:1px solid color-mix(in srgb,var(--country-accent,#60a5fa) 60%,transparent)!important;}
.cid-kpi-content-final{min-width:0!important;flex:1!important;}
.cid-kpi-label-final{color:#55c7ff!important;font-size:9px!important;font-weight:800!important;text-transform:uppercase!important;letter-spacing:.055em!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;}
.cid-kpi-value-final{color:#f7fbff!important;font-size:20px!important;font-weight:900!important;line-height:1.05!important;margin-top:6px!important;white-space:nowrap!important;}
.network-table-only{padding:18px 20px 30px!important;}
.network-table-only .network-table-wrap{margin:0!important;width:100%!important;}
@media(max-width:1100px){.cid-kpi-grid-final{grid-template-columns:repeat(3,minmax(0,1fr))!important;}}
@media(max-width:780px){.cid-kpi-grid-final{grid-template-columns:repeat(2,minmax(0,1fr))!important;}}
@media(max-width:500px){.cid-kpi-grid-final{grid-template-columns:1fr!important;}}
</style>
</head>
<body>
<script>const workbookData = {"macro":{"sa":{"country":"🇸🇦 Saudi Arabia","population":35165787,"hd":30000,"pd":2200,"annual_growth":0.09,"facilities":360,"hospital_growth":0.03,"unit_growth":0.03,"nephrologists":"~1,279","vascular_surgeons":"~175","radiologists":"~5,150","machines":18000,"demand":77530,"market_value":9.3,"coverage":"~96% covered","oop":"~11% OOP","distributors":10,"kols":10},"ae":{"country":"🇦🇪 UAE","population":11574682,"hd":3000,"pd":120,"annual_growth":0.08,"facilities":60,"hospital_growth":0.035,"unit_growth":0.04,"nephrologists":"~275","vascular_surgeons":"~100","radiologists":"~1,200","machines":4500,"demand":7638,"market_value":0.99,"coverage":"~95–100% covered","oop":"~15–20% OOP","distributors":10,"kols":10},"qa":{"country":"🇶🇦 Qatar","population":3173559,"hd":1200,"pd":180,"annual_growth":0.056,"facilities":18,"hospital_growth":0.03,"unit_growth":0.04,"nephrologists":"~45","vascular_surgeons":"~25","radiologists":"~300","machines":1100,"demand":3207,"market_value":0.42,"coverage":"~95–100% covered","oop":"~10–15% OOP","distributors":10,"kols":10},"kw":{"country":"🇰🇼 Kuwait","population":5102773,"hd":2156,"pd":294,"annual_growth":0.06,"facilities":25,"hospital_growth":0.025,"unit_growth":0.03,"nephrologists":"~100","vascular_surgeons":"~38","radiologists":"~425","machines":3000,"demand":5728,"market_value":0.72,"coverage":"~100% access/coverage","oop":"~9% OOP","distributors":10,"kols":10},"om":{"country":"🇴🇲 Oman","population":5494691,"hd":2500,"pd":100,"annual_growth":0.07,"facilities":20,"hospital_growth":0.03,"unit_growth":0.035,"nephrologists":"~105","vascular_surgeons":"~20","radiologists":"~300","machines":2200,"demand":6365,"market_value":0.76,"coverage":"~90–100% covered","oop":"~5% OOP","distributors":10,"kols":10},"jo":{"country":"🇯🇴 Jordan","population":11589532,"hd":6400,"pd":110,"annual_growth":0.05,"facilities":50,"hospital_growth":0.025,"unit_growth":0.03,"nephrologists":"~45","vascular_surgeons":"~30","radiologists":"~650","machines":2500,"demand":16127,"market_value":1.61,"coverage":"~75–80% covered","oop":"~36% OOP","distributors":10,"kols":10},"lb":{"country":"🇱🇧 Lebanon","population":5897467,"hd":4730,"pd":210,"annual_growth":0.03,"facilities":85,"hospital_growth":0.02,"unit_growth":0.025,"nephrologists":"~175","vascular_surgeons":"~25","radiologists":"~600","machines":3000,"demand":12067,"market_value":1.21,"coverage":"~45–50% covered","oop":">85% OOP","distributors":10,"kols":10},"iq":{"country":"🇮🇶 Iraq","population":48007437,"hd":10721,"pd":450,"annual_growth":0.05,"facilities":130,"hospital_growth":0.04,"unit_growth":0.045,"nephrologists":"~175","vascular_surgeons":"~40","radiologists":"~650","machines":9000,"demand":27320,"market_value":2.46,"coverage":"~20–30% covered","oop":"~70% OOP","distributors":10,"kols":10},"bh":{"country":"🇧🇭 Bahrain","population":1675572,"hd":4547,"pd":450,"annual_growth":0.05,"facilities":14,"hospital_growth":0.03,"unit_growth":0.035,"nephrologists":"~32","vascular_surgeons":"~13","radiologists":"~63","machines":750,"demand":11885,"market_value":1.43,"coverage":"~90–100% covered","oop":"~10–15% OOP","distributors":10,"kols":10}},"hotAreas":[{"rank":1,"country":"🇸🇦 Saudi Arabia","area":"Riyadh (39 centers; ~19% of KSA centers; national dialysis PPP hub) [Expert Judgment]"},{"rank":1,"country":"🇦🇪 UAE","area":"Dubai (~7+ centers; ~28%+ of UAE centers; largest private market) [Expert Judgment]"},{"rank":1,"country":"🇶🇦 Qatar","area":"Doha – Fahad Bin Jassim Kidney Center + Hamad General (majority of Qatar's ~1,300 HD patients) [Sourced: HMC, Jul‑2026] hamad"},{"rank":1,"country":"🇰🇼 Kuwait","area":"Kuwait City – Al‑Sabah medical area (Al‑Nafisi Dialysis Center + MOH hubs) [Expert Judgment]"},{"rank":1,"country":"🇴🇲 Oman","area":"Muscat (~4 centers; ~20% of Oman centers; Seeb, Al Amerat, Bousher) [Expert Judgment; Total: 20 centers, POI Data, Aug‑2026] poidata"},{"rank":1,"country":"🇯🇴 Jordan","area":"Amman (~5 centers; ~50% of Jordan centers; Yarmouk, Al‑Basheer, King Abdullah Univ. Hospital) [Expert Judgment]"},{"rank":1,"country":"🇱🇧 Lebanon","area":"Greater Beirut (majority of ~4,730 HD patients; AUBMC, Hotel Dieu, Mount Lebanon Hospital) [Expert Judgment; Total: 78 centers, WHO/EMRO, 2025]"},{"rank":1,"country":"🇮🇶 Iraq","area":"Baghdad (~11 centers; ~37% of Iraq centers; Baghdad Medical City, Marina, Sidral network) [Expert Judgment; Total: 10,721 HD patients, Iraqi Natl J Med, Jan‑2025]"},{"rank":1,"country":"🇧🇭 Bahrain","area":"Manama / Riffa (H.H. Shaikh Abdullah Center, Royal Bahrain Hospital, Bahrain Specialist Hospital) [Expert Judgment; Total: 4,547 dialysis patients, Daily Tribune Bahrain, Jan‑2026]"},{"rank":2,"country":"🇸🇦 Saudi Arabia","area":"Jeddah (12 centers; ~5.9%; major western hub; Diaverum + DaVita) [Expert Judgment]"},{"rank":2,"country":"🇦🇪 UAE","area":"Abu Dhabi (~5 centers; ~20%; SEHA Kidney Care network; Cleveland Clinic) [Expert Judgment]"},{"rank":2,"country":"🇶🇦 Qatar","area":"Doha – Al Wakrah / Al Shamal / Al Khor (HMC satellite units) [Expert Judgment]"},{"rank":2,"country":"🇰🇼 Kuwait","area":"Ahmadi (new 83‑unit Jaber Al‑Ahmad Kidney Dialysis Center, opened Aug‑2026) [Expert Judgment; Total: 2,450 dialysis patients, Arab Times, Mar‑2025]"},{"rank":2,"country":"🇴🇲 Oman","area":"Salalah (secondary southern hub; regional hospitals) [Expert Judgment]"},{"rank":2,"country":"🇯🇴 Jordan","area":"Irbid (Yarmouk Hospital dialysis unit; northern Jordan hub) [Expert Judgment]"},{"rank":2,"country":"🇱🇧 Lebanon","area":"Tripoli (secondary northern hub; public hospital dialysis) [Expert Judgment]"},{"rank":2,"country":"🇮🇶 Iraq","area":"Basra (3+ centers; southern Iraq hub; major MOH hospitals) [Expert Judgment]"},{"rank":2,"country":"🇧🇭 Bahrain","area":"A'Ali (King Hamad American Mission Hospital – large catchment) [Expert Judgment]"},{"rank":3,"country":"🇸🇦 Saudi Arabia","area":"Makkah (12 centers; ~5.9%; high seasonal patient flow) [Expert Judgment]"},{"rank":3,"country":"🇦🇪 UAE","area":"Sharjah (~3 centers; ~12%; public + private mix) [Expert Judgment]"},{"rank":3,"country":"🇶🇦 Qatar","area":"Doha – Al Shahania (HMC unit) [Expert Judgment]"},{"rank":3,"country":"🇰🇼 Kuwait","area":"Hawalli (established MOH dialysis units) [Expert Judgment]"},{"rank":3,"country":"🇴🇲 Oman","area":"Ibri (2 centers; ~10%; Ibri Referral Hospital PD unit) [Expert Judgment]"},{"rank":3,"country":"🇯🇴 Jordan","area":"Zarqa (growing urban center; private hospitals) [Expert Judgment]"},{"rank":3,"country":"🇱🇧 Lebanon","area":"Sidon (southern Lebanon hub; government hospital dialysis) [Expert Judgment]"},{"rank":3,"country":"🇮🇶 Iraq","area":"Erbil (Kurdistan; >3,000 dialysis patients in KRI; private + public centers) [Expert Judgment]"},{"rank":3,"country":"🇧🇭 Bahrain","area":"Muharraq (secondary urban cluster; private hospitals) [Expert Judgment]"},{"rank":4,"country":"🇸🇦 Saudi Arabia","area":"Dammam / Khobar (6+ centers; Eastern Province industrial hub) [Expert Judgment]"},{"rank":4,"country":"🇦🇪 UAE","area":"Al Ain (SEHA Kidney Care – Al Ain Hospital) [Expert Judgment]"},{"rank":4,"country":"🇶🇦 Qatar","area":"Doha – Hamad General (central tertiary hub) [Sourced: HMC, Jul‑2026] hamad"},{"rank":4,"country":"🇰🇼 Kuwait","area":"Farwaniya (MOH dialysis units) [Expert Judgment]"},{"rank":4,"country":"🇴🇲 Oman","area":"Sohar (2 centers; ~10%; northern Oman hub) [Expert Judgment]"},{"rank":4,"country":"🇯🇴 Jordan","area":"Salt (secondary Amman metro; private hospitals) [Expert Judgment]"},{"rank":4,"country":"🇱🇧 Lebanon","area":"Zahle (eastern Lebanon hub; private hospitals) [Expert Judgment]"},{"rank":4,"country":"🇮🇶 Iraq","area":"Sulaymaniyah (Kurdistan; major tertiary hospitals) [Expert Judgment]"},{"rank":4,"country":"🇧🇭 Bahrain","area":"Saar (American Mission Hospital branch) [Expert Judgment]"},{"rank":5,"country":"🇸🇦 Saudi Arabia","area":"Madinah (5 centers; ~2.5%; western region hub) [Expert Judgment]"},{"rank":5,"country":"🇦🇪 UAE","area":"Ajman (~2 centers; ~8%; growing private sector) [Expert Judgment]"},{"rank":5,"country":"🇶🇦 Qatar","area":"Lusail / Al Daayen (new urban growth; future clinics) [Expert Judgment]"},{"rank":5,"country":"🇰🇼 Kuwait","area":"Jahra (new medical city with dialysis component) [Expert Judgment]"},{"rank":5,"country":"🇴🇲 Oman","area":"Barka / Seeb (new MOH units) [Expert Judgment]"},{"rank":5,"country":"🇯🇴 Jordan","area":"Karak (southern Jordan; regional hospital) [Expert Judgment]"},{"rank":5,"country":"🇱🇧 Lebanon","area":"Nabatieh (southern Lebanon; regional hospital) [Expert Judgment]"},{"rank":5,"country":"🇮🇶 Iraq","area":"Kirkuk (Al‑Amal Center – ~463 patients) [Expert Judgment]"},{"rank":5,"country":"🇧🇭 Bahrain","area":"Riffa (additional private clinics) [Expert Judgment]"},{"rank":6,"country":"🇸🇦 Saudi Arabia","area":"Buraydah (7 centers; ~3.4%; Qassim region hub) [Expert Judgment]"},{"rank":6,"country":"🇦🇪 UAE","area":"Fujairah / Ras Al Khaimah (emerging northern emirates) [Expert Judgment]"},{"rank":6,"country":"🇶🇦 Qatar","area":"Mesaieed / Al Wukair (industrial areas; future clinics) [Expert Judgment]"},{"rank":6,"country":"🇰🇼 Kuwait","area":"Sabah Al‑Ahmad Health Center (Sector E dialysis unit) [Expert Judgment]"},{"rank":6,"country":"🇴🇲 Oman","area":"Al Khaburah / Al Suwayq (new MOH units) [Expert Judgment]"},{"rank":6,"country":"🇯🇴 Jordan","area":"Irbid outskirts (private clinics) [Expert Judgment]"},{"rank":6,"country":"🇱🇧 Lebanon","area":"Jounieh (coastal private hospitals) [Expert Judgment]"},{"rank":6,"country":"🇮🇶 Iraq","area":"Najaf (religious tourism hub; growing private hospitals) [Expert Judgment]"},{"rank":7,"country":"🇸🇦 Saudi Arabia","area":"Hail (6 centers; ~2.9%; northern region hub) [Expert Judgment]"},{"rank":7,"country":"🇴🇲 Oman","area":"Izki / Ibra / Sinaw (interior hubs) [Expert Judgment]"},{"rank":7,"country":"🇮🇶 Iraq","area":"Diwaniyah / Amarah (regional MOH hospitals) [Expert Judgment]"},{"rank":8,"country":"🇸🇦 Saudi Arabia","area":"Taif / Al Hofuf / Samtah (4 centers each; secondary western/eastern hubs) [Expert Judgment]"},{"rank":8,"country":"🇴🇲 Oman","area":"Muladdah / Saham / حي عاصم (smaller towns) [Expert Judgment]"},{"rank":8,"country":"🇮🇶 Iraq","area":"Tikrit / Fallouja / Ramadi (Sidral network centers) [Expert Judgment]"},{"rank":9,"country":"🇸🇦 Saudi Arabia","area":"Abha / Khamis Mushait / Al Jubail / Al Mubarraz / Ar Rass / Arar / Tabuk (3 centers each) [Expert Judgment]"},{"rank":9,"country":"🇮🇶 Iraq","area":"Mosul / Baqubah / Hilla (regional teaching hospitals) [Expert Judgment]"},{"rank":10,"country":"🇸🇦 Saudi Arabia","area":"Secondary cities (1–2 centers each: Dhahran, Hafar Al Batin, Khulais, etc.) [Expert Judgment]"},{"rank":10,"country":"🇮🇶 Iraq","area":"Secondary governorates (Diyala, Wasit, Maysan, etc.) [Expert Judgment]"}],"tenders":[{"id":1,"country":"🇸🇦 Saudi Arabia","name":"Medical Supplies – Direct Purchase","ref":"NDP0802/26","authority":"NUPCO (MOH)","published":"01-Sep-2026","deadline":"06‑Sep‑2026","status":"Closed","value":"$50K–$200K (est.)","notes":"General medical supplies; may include catheters via INUPCO platform nupco+1","priority":"Medium"},{"id":2,"country":"🇸🇦 Saudi Arabia","name":"Respiratory Therapy & Anesthesia Supplies","ref":"NDP0803/26","authority":"NUPCO (SRM)","published":"01-Sep-2026","deadline":"07‑Sep‑2026","status":"Closed","value":"$100K–$300K (est.)","notes":"Respiratory/anesthesia consumables; dialysis catheters not primary focus nupco","priority":"Low"},{"id":3,"country":"🇸🇦 Saudi Arabia","name":"General Medical Supplies","ref":"NDP0801/26","authority":"NUPCO","published":"01-Sep-2026","deadline":"03‑Sep‑2026","status":"Closed","value":"$50K–$150K (est.)","notes":"General consumables; catheters possible but not specified nupco","priority":"Medium"},{"id":4,"country":"🇸🇦 Saudi Arabia","name":"Medical Supplies – Jazan Health Cluster","ref":"NDP0798/26","authority":"NUPCO (Jazan)","published":"01-Sep-2026","deadline":"10‑Sep‑2026","status":"Open","value":"$100K–$400K (est.)","notes":"Medical devices & supplies; potential catheter inclusion nupco","priority":"High"},{"id":5,"country":"🇸🇦 Saudi Arabia","name":"Open Framework – Dialysis & Artificial Kidney Supplies","ref":"NPT0043/26 (est.)","authority":"NUPCO","published":"01-Aug-2026","deadline":"04‑Aug‑2026","status":"Closed","value":"$2M–$5M (est.)","notes":"Direct dialysis consumables tender; framework agreement for HD/PD supplies nupco+1","priority":"Critical"},{"id":6,"country":"🇶🇦 Qatar","name":"Medical Supplies – HMC/MTCS/9120/2026","ref":"133503238","authority":"Hamad Medical Corp","published":"01-Jan-2026","deadline":"10‑Feb‑2026","status":"Closed","value":"$200K–$600K","notes":"General medical supplies; dialysis items likely included hamad+1","priority":"Medium"},{"id":7,"country":"🇶🇦 Qatar","name":"Medical Consumables – HMC/TCS/9464/2026","ref":"135633622","authority":"Hamad Medical Corp","published":"01-Feb-2026","deadline":"16‑Mar‑2026","status":"Closed","value":"$300K–$800K","notes":"Consumables blanket; catheters probable tendersontime","priority":"High"},{"id":8,"country":"🇶🇦 Qatar","name":"Medical Supplies – HMC/MTCS/9140/2026","ref":"135634706","authority":"Hamad Medical Corp","published":"01-Feb-2026","deadline":"02‑Mar‑2026","status":"Closed","value":"$200K–$500K","notes":"General medical supplies tendersontime","priority":"Medium"},{"id":9,"country":"🇴🇲 Oman","name":"Medical Accessories 00047 (Re-tender)","ref":"2026/2358/و ص/م ع م س م -212","authority":"MOH Oman","published":"10‑Aug‑2026","deadline":"29‑Aug‑2026","status":"Closed","value":"$100K–$300K","notes":"Medical accessories; may include catheters qatarrfp","priority":"High"},{"id":10,"country":"🇴🇲 Oman","name":"Supply of Renal Dialysis Consumables","ref":"105094963","authority":"MOH Oman","published":"2024","deadline":"14‑Aug‑2024","status":"Closed","value":"$500K–$1.5M","notes":"Direct dialysis consumables; catheters included","priority":"Critical"},{"id":11,"country":"🇴🇲 Oman","name":"Medical Equipment for Dialysis Center (Re-tender)","ref":"13733280","authority":"MOH Oman","published":"08‑Jul‑2026","deadline":"22‑Jul‑2026","status":"Closed","value":"$300K–$800K","notes":"Dialysis center equipment & consumables","priority":"High"},{"id":12,"country":"🇦🇪 UAE","name":"Medical Consumables – AJCH (5-Year Blanket)","ref":"Various (TOT Ref.)","authority":"Dubai Academic Health Corp","published":"2026","deadline":"Rolling","status":"Active","value":"$1M–$3M/year","notes":"5-year blanket agreement; catheters included","priority":"Critical"},{"id":13,"country":"🇦🇪 UAE","name":"Hemodialysis Machine & Consumables","ref":"112579009","authority":"Health Entity (SEHA/DAHC)","published":"2026","deadline":"07‑May‑2026","status":"Closed","value":"$500K–$1.5M","notes":"HD machines + consumables; catheters implied","priority":"High"},{"id":14,"country":"🇧🇭 Bahrain","name":"Supply of Dialysis Items (AKU & PDU)","ref":"281/2024/BTB","authority":"MOH Bahrain","published":"27‑Mar‑2024","deadline":"22‑May‑2024","status":"Closed","value":"$200K–$600K","notes":"Dialysis consumables for government centers","priority":"High"},{"id":15,"country":"🇯🇴 Jordan","name":"Peritoneal Dialysis Consumables & Solutions","ref":"103874338","authority":"MOH Jordan","published":"2025","deadline":"18‑Nov‑2025","status":"Closed","value":"$150K–$400K","notes":"PD consumables & solutions","priority":"Medium"},{"id":16,"country":"🇯🇴 Jordan","name":"Dialysis Machines – Yarmouk Hospital","ref":"2026002412‑01","authority":"MOH Jordan","published":"06‑Aug‑2026","deadline":"See notice","status":"Open","value":"$300K–$700K","notes":"HD machines for Yarmouk Hospital","priority":"High"},{"id":17,"country":"🇱🇧 Lebanon","name":"Permanent & Single-Use Catheters (Re-Offer)","ref":"133538485","authority":"MOH / Public Hospitals","published":"2026","deadline":"16‑Jan‑2026","status":"Closed","value":"$100K–$300K","notes":"Direct catheter tender; permanent + single-use","priority":"Critical"},{"id":18,"country":"🇱🇧 Lebanon","name":"Life-Saving Materials incl. Catheters","ref":"132476287","authority":"MOH / Public Hospitals","published":"2025","deadline":"09‑Jan‑2026","status":"Closed","value":"$200K–$500K","notes":"Permanent + single-use catheters, urine bags, gauze","priority":"High"},{"id":19,"country":"🇮🇶 Iraq","name":"CVC & Other Catheters (Tender List)","ref":"Various","authority":"Kimadia / MOH Iraq","published":"2025–2026","deadline":"Rolling","status":"Active","value":"$500K–$2M/year","notes":"Direct CVC/dialysis catheter tenders; Kimadia platform","priority":"Critical"},{"id":20,"country":"🇰🇼 Kuwait","name":"Dialysis Consumables & Equipment","ref":"Various","authority":"MOH Kuwait","published":"2025–2026","deadline":"Rolling","status":"Active","value":"$400K–$1.2M/year","notes":"Dialysis consumables; listed on GCC aggregators","priority":"High"}],"ourASP":[{"country":"🇸🇦 Saudi Arabia","short":19,"mid":25,"long":85},{"country":"🇦🇪 UAE","short":20,"mid":27,"long":90},{"country":"🇶🇦 Qatar","short":20,"mid":27,"long":90},{"country":"🇰🇼 Kuwait","short":19,"mid":26,"long":88},{"country":"🇴🇲 Oman","short":18,"mid":25,"long":85},{"country":"🇯🇴 Jordan","short":18,"mid":24,"long":80},{"country":"🇱🇧 Lebanon","short":18,"mid":24,"long":78},{"country":"🇮🇶 Iraq","short":17,"mid":23,"long":75},{"country":"🇧🇭 Bahrain","short":19,"mid":25,"long":85}],"competitorASP":[{"company":"BD (Bard)","region":"GCC (KSA, UAE, Qatar, Kuwait, Oman, Bahrain)","short":"~90–130","long":"~180–260","notes":"Premium; antimicrobial‑coated tunneled catheters at top of range. Anchored to US list $395 for coated tunneled, but realized GCC tender prices lower. indexbox"},{"company":"BD (Bard)","region":"Levant (Jordan, Lebanon)","short":"~70–110","long":"~140–220","notes":"Premium, discounted vs GCC due to tender pressure."},{"company":"BD (Bard)","region":"Iraq","short":"~60–100","long":"~120–200","notes":"Premium, heavily discounted in Kimadia/MOH tenders."},{"company":"Medtronic","region":"GCC","short":"~80–120","long":"~160–240","notes":"Premium to mid‑premium; strong in private tertiary centers."},{"company":"Medtronic","region":"Levant","short":"~65–100","long":"~130–200","notes":"Mid‑premium."},{"company":"Medtronic","region":"Iraq","short":"~55–90","long":"~110–180","notes":"Mid‑premium."},{"company":"Merit Medical","region":"GCC","short":"~70–110","long":"~140–220","notes":"Mid‑premium; competitive in GCC tenders."},{"company":"Merit Medical","region":"Levant","short":"~60–95","long":"~120–190","notes":"Mid‑premium."},{"company":"Merit Medical","region":"Iraq","short":"~50–85","long":"~100–170","notes":"Mid‑premium."},{"company":"Vygon","region":"GCC","short":"~60–100","long":"~120–200","notes":"Value‑premium; often priced below BD/Medtronic."},{"company":"Vygon","region":"Levant","short":"~50–85","long":"~100–170","notes":"Value‑premium."},{"company":"Vygon","region":"Iraq","short":"~45–80","long":"~90–160","notes":"Value‑premium."},{"company":"B. Braun","region":"GCC","short":"~70–110","long":"~140–220","notes":"Mid‑premium; strong in EU, growing in GCC."},{"company":"B. Braun","region":"Levant","short":"~60–95","long":"~120–190","notes":"Mid‑premium."},{"company":"B. Braun","region":"Iraq","short":"~50–85","long":"~100–170","notes":"Mid‑premium."},{"company":"Teleflex / Arrow","region":"GCC","short":"~80–120","long":"~160–240","notes":"Premium; similar to Medtronic in positioning."},{"company":"Teleflex / Arrow","region":"Levant","short":"~65–100","long":"~130–200","notes":"Mid‑premium."},{"company":"Teleflex / Arrow","region":"Iraq","short":"~55–90","long":"~110–180","notes":"Mid‑premium."},{"company":"Baxter","region":"GCC","short":"~70–110","long":"~140–220","notes":"Mid‑premium; more known for dialysis machines & disposables, but catheters in similar tier."},{"company":"Baxter","region":"Levant","short":"~60–95","long":"~120–190","notes":"Mid‑premium."},{"company":"Baxter","region":"Iraq","short":"~50–85","long":"~100–170","notes":"Mid‑premium."},{"company":"Cook Medical","region":"GCC","short":"~80–120","long":"~160–240","notes":"Premium; specialty catheters."},{"company":"Cook Medical","region":"Levant","short":"~65–100","long":"~130–200","notes":"Mid‑premium."},{"company":"Cook Medical","region":"Iraq","short":"~55–90","long":"~110–180","notes":"Mid‑premium."},{"company":"Advin","region":"GCC","short":"~50–90","long":"~100–180","notes":"Value tier; Indian OEM, price‑competitive."},{"company":"Advin","region":"Levant","short":"~40–75","long":"~80–150","notes":"Value tier."},{"company":"Advin","region":"Iraq","short":"~35–70","long":"~70–140","notes":"Value tier; competitive in Iraq."},{"company":"Polymedicure","region":"GCC","short":"~45–85","long":"~90–170","notes":"Value tier; Indian OEM."},{"company":"Polymedicure","region":"Levant","short":"~35–70","long":"~70–140","notes":"Value tier."},{"company":"Polymedicure","region":"Iraq","short":"~30–65","long":"~60–130","notes":"Value tier."},{"company":"Medcomp","region":"GCC","short":"~60–100","long":"~120–200","notes":"Mid‑tier; US brand, less premium than BD/Medtronic in GCC."},{"company":"Medcomp","region":"Levant","short":"~50–85","long":"~100–170","notes":"Mid‑tier."},{"company":"Medcomp","region":"Iraq","short":"~40–75","long":"~80–150","notes":"Mid‑tier."},{"company":"Chinese manufacturers","region":"GCC","short":"~35–70","long":"~70–140","notes":"Budget tier; mostly private/NGO tenders, some GCC price‑sensitive accounts."},{"company":"Chinese manufacturers","region":"Levant","short":"~30–60","long":"~60–120","notes":"Budget tier; more common in public/NGO tenders."},{"company":"Chinese manufacturers","region":"Iraq","short":"~25–55","long":"~50–110","notes":"Budget tier; significant share in Iraq public tenders."}],"competitors":{"sa":[{"name":"Fresenius Medical Care","share":"~18–20% KSA HD catheter market businesswire+2","share_mid":19.0,"coverage":"⭐⭐⭐⭐⭐ (Nationwide via NUPCO + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance; NUPCO framework winner","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster supply"},{"name":"B. Braun Melsungen","share":"~12–14% KSA HD catheter market businesswire+1","share_mid":13.0,"coverage":"⭐⭐⭐⭐⭐ (NUPCO framework + SFDA distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + Aesculap brand; NUPCO presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Medtronic (Covidien)","share":"~10–12% KSA HD catheter market grandviewresearch","share_mid":11.0,"coverage":"⭐⭐⭐⭐⭐ (NUPCO winner NPT0048-22, Apr 2026) scribd","weakness":"Premium pricing; peritoneal catheters stronger than HD","advantage":"Technology + clinical evidence + NUPCO tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~8–10% KSA HD catheter market grandviewresearch","share_mid":9.0,"coverage":"⭐⭐⭐⭐⭐ (SFDA-licensed, major NUPCO supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + GCC manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~6–8% KSA HD catheter market","share_mid":7.0,"coverage":"⭐⭐⭐⭐ (NUPCO participant, SFDA-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Baxter International","share":"~10–12% KSA HD catheter market businesswire+1","share_mid":11.0,"coverage":"⭐⭐⭐⭐⭐ (NUPCO framework, SFDA-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus","advantage":"Renal-care ecosystem (PD + HD catheters)","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility"},{"name":"Merit Medical","share":"~4–6% KSA HD catheter market","share_mid":5.0,"coverage":"⭐⭐⭐⭐ (SFDA-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited KSA distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow)","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + GCC credibility"},{"name":"Nipro Corporation","share":"~5–7% KSA HD catheter market grandviewresearch+1","share_mid":6.0,"coverage":"⭐⭐⭐⭐ (SFDA-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~2–3% KSA HD catheter market","share_mid":2.5,"coverage":"⭐⭐⭐ (Limited KSA distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader KSA distribution"},{"name":"Medcomp","share":"~1–2% KSA HD catheter market","share_mid":1.5,"coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + GCC manufacturing + regional support"}],"ae":[{"name":"Fresenius Medical Care","share":"~20–22% UAE HD catheter market kenresearch+2","share_mid":21.0,"coverage":"⭐⭐⭐⭐⭐ (Nationwide via MOHAP/SEHA tenders + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance (SEHA Kidney Care partner); centralized tender wins","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster UAE supply (Egypt vs. Germany/Switzerland)"},{"name":"B. Braun Melsungen","share":"~14–16% UAE HD catheter market kenresearch+1","share_mid":15.0,"coverage":"⭐⭐⭐⭐⭐ (MOHAP/SEHA framework + MOHAP-licensed distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + vascular access portfolio; MOHAP presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Baxter International","share":"~12–14% UAE HD catheter market kenresearch+1","share_mid":13.0,"coverage":"⭐⭐⭐⭐⭐ (MOHAP/SEHA framework, MOHAP-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus (PD solutions dominant)","advantage":"Renal-care ecosystem (PD + HD catheters); home therapy systems","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility (Egypt vs. US/Ireland)"},{"name":"Medtronic (Covidien)","share":"~10–12% UAE HD catheter market kenresearch+1","share_mid":11.0,"coverage":"⭐⭐⭐⭐⭐ (MOHAP/SEHA tender participant)","weakness":"Premium pricing; cardiovascular focus stronger than renal","advantage":"Technology + clinical evidence + MOHAP/SEHA tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~8–10% UAE HD catheter market kenresearch+1","share_mid":9.0,"coverage":"⭐⭐⭐⭐⭐ (MOHAP-licensed, major SEHA supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + GCC manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~6–8% UAE HD catheter market indexbox","share_mid":7.0,"coverage":"⭐⭐⭐⭐ (MOHAP participant, MOHAP-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Merit Medical","share":"~4–6% UAE HD catheter market indexbox","share_mid":5.0,"coverage":"⭐⭐⭐⭐ (MOHAP-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited UAE distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow)","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + GCC credibility"},{"name":"Nipro Corporation","share":"~5–7% UAE HD catheter market kenresearch+1","share_mid":6.0,"coverage":"⭐⭐⭐⭐ (MOHAP-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~2–3% UAE HD catheter market indexbox","share_mid":2.5,"coverage":"⭐⭐⭐ (Limited UAE distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader UAE distribution"},{"name":"Medcomp","share":"~1–2% UAE HD catheter market indexbox","share_mid":1.5,"coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + GCC manufacturing + regional support"},{"name":"Advin Healthcare","share":"~1–2% UAE HD catheter market indexbox","share_mid":1.5,"coverage":"⭐⭐⭐ (MOHAP-licensed distributors)","weakness":"Cost-focused; limited brand recognition; India-based","advantage":"Competitive pricing (India manufacturing)","specializes":"HD catheters, dialysis disposables, machines","edge":"AMECATH: Quality + GCC credibility + regional proximity (Egypt vs. India)"},{"name":"Local UAE Assemblers (e.g., Gulf Drug, Emitac)","share":"Emerging (no HD catheter manufacturing yet) scribd+1","share_mid":null,"coverage":"⭐⭐⭐ (MOHAP-licensed, local assembly)","weakness":"New entrants; trading companies, no HD catheter production yet","advantage":"Locally assembled/traded (MOHAP preference for local suppliers)","specializes":"Medical equipment trading, disposables, some assembly","edge":"AMECATH: Established HD catheter portfolio + international credibility + broader range"}],"qa":[{"name":"Fresenius Medical Care","share":"~22–24% Qatar HD catheter market indexbox+1","share_mid":23.0,"coverage":"⭐⭐⭐⭐⭐ (Nationwide via HMC/PHCC tenders + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance (HMC partner); centralized tender wins","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster Qatar supply (Egypt vs. Germany/Switzerland)"},{"name":"B. Braun Melsungen","share":"~15–17% Qatar HD catheter market indexbox+1","share_mid":16.0,"coverage":"⭐⭐⭐⭐⭐ (HMC/PHCC framework + QH-licensed distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + vascular access portfolio; HMC presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Baxter International","share":"~13–15% Qatar HD catheter market indexbox","share_mid":14.0,"coverage":"⭐⭐⭐⭐⭐ (HMC/PHCC framework, QH-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus (PD solutions dominant)","advantage":"Renal-care ecosystem (PD + HD catheters); home therapy systems","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility (Egypt vs. US/Ireland)"},{"name":"Medtronic (Covidien)","share":"~11–13% Qatar HD catheter market indexbox+1","share_mid":12.0,"coverage":"⭐⭐⭐⭐⭐ (HMC tender participant HMC/TCS/9464/2026) tendersontime","weakness":"Premium pricing; cardiovascular focus stronger than renal","advantage":"Technology + clinical evidence + HMC tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~9–11% Qatar HD catheter market indexbox","share_mid":10.0,"coverage":"⭐⭐⭐⭐⭐ (QH-licensed, major HMC supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + GCC manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~7–9% Qatar HD catheter market indexbox","share_mid":8.0,"coverage":"⭐⭐⭐⭐ (HMC participant, QH-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Merit Medical","share":"~5–7% Qatar HD catheter market indexbox","share_mid":6.0,"coverage":"⭐⭐⭐⭐ (QH-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited Qatar distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow)","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + GCC credibility"},{"name":"Nipro Corporation","share":"~6–8% Qatar HD catheter market indexbox","share_mid":7.0,"coverage":"⭐⭐⭐⭐ (QH-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~2–3% Qatar HD catheter market indexbox","share_mid":2.5,"coverage":"⭐⭐⭐ (Limited Qatar distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader Qatar distribution"},{"name":"Medcomp","share":"~1–2% Qatar HD catheter market indexbox","share_mid":1.5,"coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + GCC manufacturing + regional support"},{"name":"Advin Healthcare","share":"~1–2% Qatar HD catheter market indexbox","share_mid":1.5,"coverage":"⭐⭐⭐ (QH-licensed distributors)","weakness":"Cost-focused; limited brand recognition; India-based","advantage":"Competitive pricing (India manufacturing)","specializes":"HD catheters, dialysis disposables, machines","edge":"AMECATH: Quality + GCC credibility + regional proximity (Egypt vs. India)"},{"name":"Local Qatar Traders (e.g., Ali Bin Ali Medical, Aamal Medical)","share":"Emerging (no HD catheter manufacturing yet) scribd","share_mid":null,"coverage":"⭐⭐⭐⭐ (QH-licensed, local trading)","weakness":"Trading companies; no HD catheter production yet","advantage":"Locally traded (QH preference for local suppliers)","specializes":"Medical equipment trading, disposables, some assembly","edge":"AMECATH: Established HD catheter portfolio + international credibility + broader range"}],"kw":[{"name":"Fresenius Medical Care","share":"~24–26% Kuwait HD catheter market grandviewresearch+2","share_mid":25.0,"coverage":"⭐⭐⭐⭐⭐ (Nationwide via MOH/KFSH tenders + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance (MOH partner); centralized tender wins","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster Kuwait supply (Egypt vs. Germany/Switzerland)"},{"name":"B. Braun Melsungen","share":"~16–18% Kuwait HD catheter market grandviewresearch+1","share_mid":17.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/KFSH framework + MOH-licensed distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + vascular access portfolio; MOH presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Baxter International","share":"~14–16% Kuwait HD catheter market grandviewresearch+1","share_mid":15.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/KFSH framework, MOH-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus (PD solutions dominant)","advantage":"Renal-care ecosystem (PD + HD catheters); home therapy systems","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility (Egypt vs. US/Ireland)"},{"name":"Medtronic (Covidien)","share":"~12–14% Kuwait HD catheter market accio+1","share_mid":13.0,"coverage":"⭐⭐⭐⭐⭐ (MOH tender participant)","weakness":"Premium pricing; cardiovascular focus stronger than renal","advantage":"Technology + clinical evidence + MOH/KFSH tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~10–12% Kuwait HD catheter market accio+1","share_mid":11.0,"coverage":"⭐⭐⭐⭐⭐ (MOH-licensed, major KFSH supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + GCC manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~8–10% Kuwait HD catheter market accio","share_mid":9.0,"coverage":"⭐⭐⭐⭐ (MOH participant, MOH-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Merit Medical","share":"~6–8% Kuwait HD catheter market accio","share_mid":7.0,"coverage":"⭐⭐⭐⭐ (MOH-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited Kuwait distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow)","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + GCC credibility"},{"name":"Nipro Corporation","share":"~7–9% Kuwait HD catheter market grandviewresearch+1","share_mid":8.0,"coverage":"⭐⭐⭐⭐ (MOH-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~3–4% Kuwait HD catheter market accio","share_mid":3.5,"coverage":"⭐⭐⭐ (Limited Kuwait distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader Kuwait distribution"},{"name":"Medcomp","share":"~2–3% Kuwait HD catheter market accio","share_mid":2.5,"coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + GCC manufacturing + regional support"},{"name":"Advin Healthcare","share":"~2–3% Kuwait HD catheter market accio","share_mid":2.5,"coverage":"⭐⭐⭐ (MOH-licensed distributors)","weakness":"Cost-focused; limited brand recognition; India-based","advantage":"Competitive pricing (India manufacturing)","specializes":"HD catheters, dialysis disposables, machines","edge":"AMECATH: Quality + GCC credibility + regional proximity (Egypt vs. India)"},{"name":"Local Kuwait Traders (e.g., Alghanim Healthcare, Himatrix)","share":"Emerging (no HD catheter manufacturing yet) scribd+1","share_mid":null,"coverage":"⭐⭐⭐⭐ (MOH-licensed, local trading)","weakness":"Trading companies; no HD catheter production yet","advantage":"Locally traded (MOH preference for local suppliers)","specializes":"Medical equipment trading, disposables, some assembly","edge":"AMECATH: Established HD catheter portfolio + international credibility + broader range"}],"om":[{"name":"Fresenius Medical Care","share":"~24–26% Oman HD catheter market grandviewresearch+2","share_mid":25.0,"coverage":"⭐⭐⭐⭐⭐ (Nationwide via MOH/KFSH tenders + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance (MOH partner); centralized tender wins","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster Oman supply (Egypt vs. Germany/Switzerland)"},{"name":"B. Braun Melsungen","share":"~16–18% Oman HD catheter market grandviewresearch+1","share_mid":17.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/KFSH framework + MOH-licensed distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + vascular access portfolio; MOH presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Baxter International","share":"~14–16% Oman HD catheter market grandviewresearch+1","share_mid":15.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/KFSH framework, MOH-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus (PD solutions dominant)","advantage":"Renal-care ecosystem (PD + HD catheters); home therapy systems","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility (Egypt vs. US/Ireland)"},{"name":"Medtronic (Covidien)","share":"~12–14% Oman HD catheter market accio+1","share_mid":13.0,"coverage":"⭐⭐⭐⭐⭐ (MOH tender participant)","weakness":"Premium pricing; cardiovascular focus stronger than renal","advantage":"Technology + clinical evidence + MOH/KFSH tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~10–12% Oman HD catheter market accio+1","share_mid":11.0,"coverage":"⭐⭐⭐⭐⭐ (MOH-licensed, major KFSH supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + GCC manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~8–10% Oman HD catheter market accio","share_mid":9.0,"coverage":"⭐⭐⭐⭐ (MOH participant, MOH-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Merit Medical","share":"~6–8% Oman HD catheter market accio","share_mid":7.0,"coverage":"⭐⭐⭐⭐ (MOH-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited Oman distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow)","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + GCC credibility"},{"name":"Nipro Corporation","share":"~7–9% Oman HD catheter market grandviewresearch+1","share_mid":8.0,"coverage":"⭐⭐⭐⭐ (MOH-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~3–4% Oman HD catheter market accio","share_mid":3.5,"coverage":"⭐⭐⭐ (Limited Oman distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader Oman distribution"},{"name":"Medcomp","share":"~2–3% Oman HD catheter market accio","share_mid":2.5,"coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + GCC manufacturing + regional support"},{"name":"Advin Healthcare","share":"~2–3% Oman HD catheter market accio","share_mid":2.5,"coverage":"⭐⭐⭐ (MOH-licensed distributors)","weakness":"Cost-focused; limited brand recognition; India-based","advantage":"Competitive pricing (India manufacturing)","specializes":"HD catheters, dialysis disposables, machines","edge":"AMECATH: Quality + GCC credibility + regional proximity (Egypt vs. India)"},{"name":"Local Oman Traders (e.g., Alghanim Healthcare, Himatrix)","share":"Emerging (no HD catheter manufacturing yet) scribd+1","share_mid":null,"coverage":"⭐⭐⭐⭐ (MOH-licensed, local trading)","weakness":"Trading companies; no HD catheter production yet","advantage":"Locally traded (MOH preference for local suppliers)","specializes":"Medical equipment trading, disposables, some assembly","edge":"AMECATH: Established HD catheter portfolio + international credibility + broader range"}],"jo":[{"name":"Fresenius Medical Care","share":"~28–30% Jordan HD catheter market gminsights+1","share_mid":29.0,"coverage":"⭐⭐⭐⭐⭐ (Nationwide via MOH/KFH tenders + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance (MOH partner); centralized tender wins","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster Jordan supply (Egypt vs. Germany/Switzerland)"},{"name":"B. Braun Melsungen","share":"~19–21% Jordan HD catheter market gminsights+1","share_mid":20.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/KFH framework + MOH-licensed distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + vascular access portfolio; MOH presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Baxter International","share":"~16–18% Jordan HD catheter market gminsights+1","share_mid":17.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/KFH framework, MOH-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus (PD solutions dominant)","advantage":"Renal-care ecosystem (PD + HD catheters); home therapy systems","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility (Egypt vs. US/Ireland)"},{"name":"Medtronic (Covidien)","share":"~14–16% Jordan HD catheter market gminsights+1","share_mid":15.0,"coverage":"⭐⭐⭐⭐⭐ (MOH tender participant)","weakness":"Premium pricing; cardiovascular focus stronger than renal","advantage":"Technology + clinical evidence + MOH/KFH tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~11–13% Jordan HD catheter market gminsights","share_mid":12.0,"coverage":"⭐⭐⭐⭐⭐ (MOH-licensed, major KFH supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution (11% global market leader) gminsights","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + Levant manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~9–11% Jordan HD catheter market gminsights","share_mid":10.0,"coverage":"⭐⭐⭐⭐ (MOH participant, MOH-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Merit Medical","share":"~7–9% Jordan HD catheter market gminsights","share_mid":8.0,"coverage":"⭐⭐⭐⭐ (MOH-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited Jordan distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow); top 5 player (36% collective) gminsights","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + Levant credibility"},{"name":"Nipro Corporation","share":"~8–10% Jordan HD catheter market coherentmarketinsights","share_mid":9.0,"coverage":"⭐⭐⭐⭐ (MOH-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~3–4% Jordan HD catheter market gminsights","share_mid":3.5,"coverage":"⭐⭐⭐ (Limited Jordan distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader Jordan distribution"},{"name":"Medcomp","share":"~2–3% Jordan HD catheter market gminsights","share_mid":2.5,"coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + Levant manufacturing + regional support"},{"name":"Advin Healthcare","share":"~2–3% Jordan HD catheter market gminsights","share_mid":2.5,"coverage":"⭐⭐⭐ (MOH-licensed distributors)","weakness":"Cost-focused; limited brand recognition; India-based","advantage":"Competitive pricing (India manufacturing)","specializes":"HD catheters, dialysis disposables, machines","edge":"AMECATH: Quality + Levant credibility + regional proximity (Egypt vs. India)"},{"name":"Local Jordan Traders (e.g., Ibn Sina Medical, Al Ghad Medical Supplies)","share":"Emerging (no HD catheter manufacturing yet) atlas-medical+2","share_mid":null,"coverage":"⭐⭐⭐⭐ (MOH-licensed, local trading)","weakness":"Trading companies; no HD catheter production yet","advantage":"Locally traded (MOH preference for local suppliers)","specializes":"Medical equipment trading, disposables, some assembly","edge":"AMECATH: Established HD catheter portfolio + international credibility + broader range"}],"lb":[{"name":"Fresenius Medical Care","share":"~30–32% Lebanon HD catheter market lebanontenders+1","share_mid":31.0,"coverage":"⭐⭐⭐⭐⭐ (Nationwide via MOH/AUBMC tenders + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance (MOH partner); centralized tender wins","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster Lebanon supply (Egypt vs. Germany/Switzerland)"},{"name":"B. Braun Melsungen","share":"~20–22% Lebanon HD catheter market lebanontenders+1","share_mid":21.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/AUBMC framework + MOH-licensed distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + vascular access portfolio; MOH presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Baxter International","share":"~17–19% Lebanon HD catheter market lebanontenders+1","share_mid":18.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/AUBMC framework, MOH-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus (PD solutions dominant)","advantage":"Renal-care ecosystem (PD + HD catheters); home therapy systems","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility (Egypt vs. US/Ireland)"},{"name":"Medtronic (Covidien)","share":"~15–17% Lebanon HD catheter market lebanontenders","share_mid":16.0,"coverage":"⭐⭐⭐⭐⭐ (MOH tender participant)","weakness":"Premium pricing; cardiovascular focus stronger than renal","advantage":"Technology + clinical evidence + MOH/AUBMC tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~12–14% Lebanon HD catheter market lebanontenders","share_mid":13.0,"coverage":"⭐⭐⭐⭐⭐ (MOH-licensed, major AUBMC supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution (11% global market leader)","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + Levant manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~10–12% Lebanon HD catheter market lebanontenders","share_mid":11.0,"coverage":"⭐⭐⭐⭐ (MOH participant, MOH-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Merit Medical","share":"~8–10% Lebanon HD catheter market lebanontenders","share_mid":9.0,"coverage":"⭐⭐⭐⭐ (MOH-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited Lebanon distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow); top 5 player (36% collective)","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + Levant credibility"},{"name":"Nipro Corporation","share":"~9–11% Lebanon HD catheter market lebweb","share_mid":10.0,"coverage":"⭐⭐⭐⭐ (MOH-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~3–4% Lebanon HD catheter market lebanontenders","share_mid":3.5,"coverage":"⭐⭐⭐ (Limited Lebanon distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader Lebanon distribution"},{"name":"Medcomp","share":"~2–3% Lebanon HD catheter market lebanontenders","share_mid":2.5,"coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + Levant manufacturing + regional support"},{"name":"Advin Healthcare","share":"~2–3% Lebanon HD catheter market lebanontenders","share_mid":2.5,"coverage":"⭐⭐⭐ (MOH-licensed distributors)","weakness":"Cost-focused; limited brand recognition; India-based","advantage":"Competitive pricing (India manufacturing)","specializes":"HD catheters, dialysis disposables, machines","edge":"AMECATH: Quality + Levant credibility + regional proximity (Egypt vs. India)"},{"name":"Local Lebanon Traders (e.g., Dima Healthcare, Sterimed, Atallah Co.)","share":"Emerging (no HD catheter manufacturing yet) lebweb+2","share_mid":null,"coverage":"⭐⭐⭐⭐ (MOH-licensed, local trading)","weakness":"Trading companies; no HD catheter production yet","advantage":"Locally traded (MOH preference for local suppliers)","specializes":"Medical equipment trading, disposables, some assembly","edge":"AMECATH: Established HD catheter portfolio + international credibility + broader range"}],"iq":[{"name":"Fresenius Medical Care","share":"~32–34% Iraq HD catheter market kimadia.gov+1","share_mid":33.0,"coverage":"⭐⭐⭐⭐⭐ (Nationwide via KIMADIA/MOH tenders + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance (KIMADIA partner); centralized tender wins","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster Iraq supply (Egypt vs. Germany/Switzerland)"},{"name":"B. Braun Melsungen","share":"~21–23% Iraq HD catheter market kimadia.gov+1","share_mid":22.0,"coverage":"⭐⭐⭐⭐⭐ (KIMADIA/MOH framework + KIMADIA-licensed distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + vascular access portfolio; KIMADIA presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Baxter International","share":"~18–20% Iraq HD catheter market kimadia.gov+1","share_mid":19.0,"coverage":"⭐⭐⭐⭐⭐ (KIMADIA/MOH framework, KIMADIA-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus (PD solutions dominant)","advantage":"Renal-care ecosystem (PD + HD catheters); home therapy systems","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility (Egypt vs. US/Ireland)"},{"name":"Medtronic (Covidien)","share":"~16–18% Iraq HD catheter market kimadia.gov+1","share_mid":17.0,"coverage":"⭐⭐⭐⭐⭐ (KIMADIA tender participant SUP 98/2026/19) kimadia.gov","weakness":"Premium pricing; cardiovascular focus stronger than renal","advantage":"Technology + clinical evidence + KIMADIA/MOH tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~13–15% Iraq HD catheter market kimadia.gov","share_mid":14.0,"coverage":"⭐⭐⭐⭐⭐ (KIMADIA-licensed, major MOH supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution (11% global market leader)","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + Levant manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~11–13% Iraq HD catheter market kimadia.gov","share_mid":12.0,"coverage":"⭐⭐⭐⭐ (KIMADIA participant, KIMADIA-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Merit Medical","share":"~9–11% Iraq HD catheter market kimadia.gov","share_mid":10.0,"coverage":"⭐⭐⭐⭐ (KIMADIA-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited Iraq distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow); top 5 player (36% collective)","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + Levant credibility"},{"name":"Nipro Corporation","share":"~10–12% Iraq HD catheter market kimadia.gov","share_mid":11.0,"coverage":"⭐⭐⭐⭐ (KIMADIA-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~4–5% Iraq HD catheter market kimadia.gov","share_mid":4.5,"coverage":"⭐⭐⭐ (Limited Iraq distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader Iraq distribution"},{"name":"Medcomp","share":"~3–4% Iraq HD catheter market kimadia.gov","share_mid":3.5,"coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + Levant manufacturing + regional support"},{"name":"Advin Healthcare","share":"~3–4% Iraq HD catheter market kimadia.gov","share_mid":3.5,"coverage":"⭐⭐⭐ (KIMADIA-licensed distributors)","weakness":"Cost-focused; limited brand recognition; India-based","advantage":"Competitive pricing (India manufacturing)","specializes":"HD catheters, dialysis disposables, machines","edge":"AMECATH: Quality + Levant credibility + regional proximity (Egypt vs. India)"},{"name":"Local Iraq Traders (e.g., Bioscope Medical, Albanna Group, Future Light)","share":"Emerging (no HD catheter manufacturing yet) rentechdigital+3","share_mid":null,"coverage":"⭐⭐⭐⭐ (KIMADIA-licensed, local trading)","weakness":"Trading companies; no HD catheter production yet","advantage":"Locally traded (KIMADIA preference for local suppliers)","specializes":"Medical equipment trading, disposables, some assembly","edge":"AMECATH: Established HD catheter portfolio + international credibility + broader range"}],"bh":[{"name":"Fresenius Medical Care","share":"~34–36% Bahrain HD catheter market selltostate","share_mid":35.0,"coverage":"⭐⭐⭐⭐⭐ (Nationwide via MOH/Salmaniya tenders + direct)","weakness":"Catheters bundled with machines/disposables; less catheter-focused innovation","advantage":"Dialysis ecosystem dominance (MOH partner); centralized tender wins","specializes":"HD catheters (tunneled/non-tunneled), dialysis machines, disposables","edge":"AMECATH: Dedicated HD catheter specialization + better pricing flexibility + faster Bahrain supply (Egypt vs. Germany/Switzerland)"},{"name":"B. Braun Melsungen","share":"~22–24% Bahrain HD catheter market selltostate","share_mid":23.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/Salmaniya framework + NHRA-licensed distributors)","weakness":"Large diversified portfolio; catheters secondary to dialyzers/machines","advantage":"Cost-competitive catheters + vascular access portfolio; MOH presence","specializes":"HD catheters, dialyzers, vascular access, surgical devices","edge":"AMECATH: Agile regional supply + competitive pricing + focused HD catheter portfolio"},{"name":"Baxter International","share":"~19–21% Bahrain HD catheter market selltostate","share_mid":20.0,"coverage":"⭐⭐⭐⭐⭐ (MOH/Salmaniya framework, NHRA-licensed)","weakness":"PD catheters stronger than HD; catheters not core focus (PD solutions dominant)","advantage":"Renal-care ecosystem (PD + HD catheters); home therapy systems","specializes":"PD/HD catheters, dialysis solutions, renal disposables","edge":"AMECATH: HD catheter specialization + competitive pricing + regional agility (Egypt vs. US/Ireland)"},{"name":"Medtronic (Covidien)","share":"~17–19% Bahrain HD catheter market selltostate","share_mid":18.0,"coverage":"⭐⭐⭐⭐⭐ (MOH tender participant)","weakness":"Premium pricing; cardiovascular focus stronger than renal","advantage":"Technology + clinical evidence + MOH/Salmaniya tender wins","specializes":"Peritoneal/HD catheters, vascular access, cardiovascular devices","edge":"AMECATH: Specialized HD catheter company + cost advantage + regional agility (Egypt vs. US)"},{"name":"BD (Becton Dickinson)","share":"~14–16% Bahrain HD catheter market selltostate","share_mid":15.0,"coverage":"⭐⭐⭐⭐⭐ (NHRA-licensed, major Salmaniya supplier)","weakness":"Premium pricing; vascular access broader than HD catheters","advantage":"Brand + clinical evidence + global distribution (11% global market leader)","specializes":"HD catheters, PICC, CVC, vascular access devices","edge":"AMECATH: Better value proposition + GCC manufacturing credibility + customization"},{"name":"Teleflex (Arrow)","share":"~12–14% Bahrain HD catheter market selltostate","share_mid":13.0,"coverage":"⭐⭐⭐⭐ (MOH participant, NHRA-licensed)","weakness":"Premium positioning; Arrow brand vascular-focused","advantage":"Advanced HD catheter technology (Arrow brand)","specializes":"HD catheters (Arrow), vascular access, urology devices","edge":"AMECATH: Cost + product flexibility + regional proximity (Egypt vs. Ireland)"},{"name":"Merit Medical","share":"~10–12% Bahrain HD catheter market selltostate","share_mid":11.0,"coverage":"⭐⭐⭐⭐ (NHRA-licensed distributors)","weakness":"Smaller scale vs. Fresenius/B. Braun; limited Bahrain distribution","advantage":"Strong HD catheter portfolio (Permcath, OptiFlow); top 5 player (36% collective)","specializes":"HD catheters (tunneled/non-tunneled), interventional devices","edge":"AMECATH: Price + flexible supply/customization + GCC credibility"},{"name":"Nipro Corporation","share":"~11–13% Bahrain HD catheter market selltostate","share_mid":12.0,"coverage":"⭐⭐⭐⭐ (NHRA-licensed distributors)","weakness":"Japan-based; slower supply chain; less regional presence","advantage":"Cost-competitive Japanese quality; dialysis disposables","specializes":"HD catheters, tubing sets, dialyzers","edge":"AMECATH: Regional proximity (Egypt vs. Japan) + faster supply + customization"},{"name":"AngioDynamics","share":"~4–5% Bahrain HD catheter market selltostate","share_mid":4.5,"coverage":"⭐⭐⭐ (Limited Bahrain distribution)","weakness":"Smaller footprint; vascular-focused, not HD-specific","advantage":"Specialty HD catheters (e.g., Groshong, Vectra)","specializes":"HD catheters, vascular access, oncology devices","edge":"AMECATH: Dedicated HD catheter focus + broader Bahrain distribution"},{"name":"Medcomp","share":"~3–4% Bahrain HD catheter market selltostate","share_mid":3.5,"coverage":"⭐⭐⭐ (Niche distributor presence)","weakness":"Limited brand recognition; small HD catheter portfolio","advantage":"Specialty HD catheter designs (Split-Step, Catheter Lock)","specializes":"HD catheters, vascular access locks","edge":"AMECATH: Better value + GCC manufacturing + regional support"},{"name":"Advin Healthcare","share":"~3–4% Bahrain HD catheter market selltostate","share_mid":3.5,"coverage":"⭐⭐⭐ (NHRA-licensed distributors)","weakness":"Cost-focused; limited brand recognition; India-based","advantage":"Competitive pricing (India manufacturing)","specializes":"HD catheters, dialysis disposables, machines","edge":"AMECATH: Quality + GCC credibility + regional proximity (Egypt vs. India)"},{"name":"Local Bahrain Traders (e.g., Al Zayani Medical, Cigalah Gulf Medical, Gulf Biotech)","share":"Emerging (no HD catheter manufacturing yet) scribd+1","share_mid":null,"coverage":"⭐⭐⭐⭐ (NHRA-licensed, local trading)","weakness":"Trading companies; no HD catheter production yet","advantage":"Locally traded (MOH preference for local suppliers)","specializes":"Medical equipment trading, disposables, some assembly","edge":"AMECATH: Established HD catheter portfolio + international credibility + broader range"}]}};</script>
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
  <div style="text-align:center;padding:8px 16px 16px;font-size:10px;color:#2a4060;">Data source: Amecath Dash workbook &nbsp;·&nbsp; 2026 Edition &nbsp;·&nbsp; 9 Markets</div>
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

  <!-- Country Forecast Chart -->
  <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;padding:20px;margin-bottom:18px;">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:5px;">
      <div>
        <div style="font-size:13px;font-weight:600;color:#c8d8f0;">📊 Scenario Comparison by Year</div>
        <div style="font-size:10px;color:#3a5278;margin-top:3px;">Base Case revenue forecast in USD — select a country to view its 2026–2028 forecast</div>
      </div>
      <select id="forecast-country-chart-filter" style="min-width:190px;padding:9px 12px;border-radius:9px;border:1px solid #2563eb;background:#081321;color:#e8edf5;font-size:11px;font-weight:600;outline:none;cursor:pointer;">
        <option value="">Select country</option>
      </select>
    </div>
    <div id="forecast-country-chart" style="margin-top:10px;"></div>
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
  <div style="padding:0 16px 24px;"><div style="margin-bottom:18px;"><div style="font-size:15px;font-weight:700;color:#c8d8f0;">💲 Pricing Intelligence</div><div style="font-size:10px;color:#6a85b0;margin-top:4px;">Workbook-derived AMECATH ASP by country + competitor kit ASP benchmarks.</div></div>
  <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;overflow:hidden;margin-bottom:16px;"><div style="padding:14px 16px;border-bottom:1px solid #1e3d7a;font-size:12px;font-weight:700;color:#e8edf5;">AMECATH ASP by Country (USD)</div><div style="overflow-x:auto;"><table style="width:100%;min-width:760px;border-collapse:collapse;font-size:11px;"><thead><tr style="background:#070f1f;"><th style="padding:11px 14px;text-align:left;color:#6a85b0;">Country</th><th style="padding:11px 14px;color:#6a85b0;">Short-Term / STD</th><th style="padding:11px 14px;color:#6a85b0;">Mid-Term</th><th style="padding:11px 14px;color:#6a85b0;">Long-Term / Tunneled</th></tr></thead><tbody id="our-asp-body"></tbody></table></div></div>
  <div style="background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;overflow:hidden;"><div style="padding:14px 16px;border-bottom:1px solid #1e3d7a;font-size:12px;font-weight:700;color:#e8edf5;">Competitor ASP Benchmark</div><div style="overflow-x:auto;"><table style="width:100%;min-width:980px;border-collapse:collapse;font-size:11px;"><thead><tr style="background:#070f1f;"><th style="padding:11px 14px;text-align:left;color:#6a85b0;">Company</th><th style="padding:11px 14px;color:#6a85b0;">Region</th><th style="padding:11px 14px;color:#6a85b0;">Short-Term Kit</th><th style="padding:11px 14px;color:#6a85b0;">Long-Term Kit</th><th style="padding:11px 14px;text-align:left;color:#6a85b0;">Notes</th></tr></thead><tbody id="comp-asp-body"></tbody></table></div></div>
  <div style="margin-top:12px;padding:11px 14px;border:1px dashed #1e3d7a;border-radius:10px;color:#6a85b0;font-size:10px;">Source: <b style="color:#c8d8f0;">our ASP</b> and <b style="color:#c8d8f0;">Competitor_Aspiration</b>. These are benchmark/aspiration figures, not live awarded tender prices.</div></div>
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
      #page-tenders .tndr-status-active { color:#34d399; background:rgba(52,211,153,.12); border-color:rgba(52,211,153,.5); }
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
        📋 Tender Register (20)
      </button>
      <button id="tndr-tab-pipeline" onclick="tndrSwitchTab('pipeline')" style="flex:1;padding:10px 0;border:none;border-radius:9px;font-size:12px;font-weight:700;cursor:pointer;transition:all .2s;background:transparent;color:#6a85b0;">
        🔭 Pipeline Forecast (20)
      </button>
    </div>

    <div id="tndr-section-active">
      <div class="tndr-kpis">
        <div class="tndr-kpi"><div class="tndr-kpi-label">Workbook Tenders</div><div class="tndr-kpi-value">20</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Estimated Value Range</div><div class="tndr-kpi-value" style="color:#60a5fa;">$50K–$5M</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Critical Priority</div><div class="tndr-kpi-value" style="color:#f59e0b;">5</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Open / Active</div><div class="tndr-kpi-value" style="color:#3b82f6;">5</div></div>
        <div class="tndr-kpi"><div class="tndr-kpi-label">Closed</div><div class="tndr-kpi-value" style="color:#34d399;">15</div></div>
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
          <button class="tndr-filter-btn" data-tndr-status="Active">Active</button>
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
    <div id="comp-grid" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"></div>
  </div>
</div>

<!-- HOT AREAS -->

<div class="page" id="page-hotareas">
  <div class="section-header"><span style="font-size:16px">📍</span><span class="section-title">Hot Areas — Dialysis Market</span></div>
  <div class="hot-map"><div id="market-map"></div></div>
  <div style="margin:0 16px 24px;background:#0f1f3d;border:1px solid #1e3d7a;border-radius:14px;overflow:hidden;">
    <div style="padding:15px 16px;border-bottom:1px solid #1e3d7a;">
      <div style="font-size:13px;font-weight:800;color:#e8edf5;">📍 Ranked Hot Areas by Country</div>
      <div style="font-size:10px;color:#6a85b0;margin-top:3px;">Workbook-ranked city / area list from Hot_Areas. Rank 1 is the highest-priority area within each country.</div>
    </div>
    <div style="overflow-x:auto;"><table style="width:100%;min-width:900px;border-collapse:collapse;font-size:11px;">
      <thead><tr style="background:#070f1f;"><th style="padding:11px 14px;text-align:left;color:#6a85b0;">Rank</th><th style="padding:11px 14px;text-align:left;color:#6a85b0;">Country</th><th style="padding:11px 14px;text-align:left;color:#6a85b0;">Hot Area / City</th></tr></thead>
      <tbody id="hotareas-table-body"></tbody></table></div>
  </div>
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
    <div class="kpi-card"><div class="kpi-icon">✅</div><div class="kpi-label">Registered Markets</div><div class="kpi-value" style="color:#34d399">4</div><div class="kpi-sub green">Saudi Arabia · Jordan · Iraq · Lebanon</div></div>
    <div class="kpi-card"><div class="kpi-icon">⛔</div><div class="kpi-label">Not Registered</div><div class="kpi-value gold">5</div><div class="kpi-sub amber">UAE · Qatar · Kuwait · Oman · Bahrain</div></div>
    <div class="kpi-card"><div class="kpi-icon">🛡️</div><div class="kpi-label">Core Compliance</div><div class="kpi-value accent">CE / ISO</div><div class="kpi-sub muted">ISO 13485 Certified</div></div>
    <div class="kpi-card"><div class="kpi-icon">🌍</div><div class="kpi-label">Regional Coverage</div><div class="kpi-value">4 / 9</div><div class="kpi-sub muted">Markets registered</div></div>
  </div>
  <div class="reg-table-container">
    <table class="reg-table">
      <thead><tr><th>Country / Market</th><th>Health Authority</th><th>Registration Status</th><th>Key Requirements / Note</th></tr></thead>
      <tbody>
        <tr><td><b>🇸🇦 Saudi Arabia</b></td><td>SFDA</td><td><span class="badge badge-approved">Registered</span></td><td>MDNR &amp; CE Mark</td></tr>
        <tr><td><b>🇦🇪 UAE</b></td><td>MOHAP</td><td><span class="badge badge-pending">Not Registered</span></td><td>Registration required before market entry</td></tr>
        <tr><td><b>🇰🇼 Kuwait</b></td><td>MOH Kuwait</td><td><span class="badge badge-pending">Not Registered</span></td><td>Registration required before market entry</td></tr>
        <tr><td><b>🇶🇦 Qatar</b></td><td>MOPH Qatar</td><td><span class="badge badge-pending">Not Registered</span></td><td>Registration required before market entry</td></tr>
        <tr><td><b>🇴🇲 Oman</b></td><td>MOH Oman</td><td><span class="badge badge-pending">Not Registered</span></td><td>Registration required before market entry</td></tr>
        <tr><td><b>🇧🇭 Bahrain</b></td><td>NHRA</td><td><span class="badge badge-pending">Not Registered</span></td><td>Registration required before market entry</td></tr>
        <tr><td><b>🇮🇶 Iraq</b></td><td>MOH Iraq (KIMADIA)</td><td><span class="badge badge-approved">Registered</span></td><td>Tender Registration &amp; MOH Dossier</td></tr>
        <tr><td><b>🇯🇴 Jordan</b></td><td>JFDA</td><td><span class="badge badge-approved">Registered</span></td><td>JFDA Medical Device Registration</td></tr>
        <tr><td><b>🇱🇧 Lebanon</b></td><td>MOPH Lebanon</td><td><span class="badge badge-approved">Registered</span></td><td>Import Permit &amp; Quality Cert</td></tr>
      </tbody>
    </table>
  </div>
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


const networkData = {"distributors":{"sa":[{"num":1,"name":"AMHSCO – Arabian Medical Hospital Supply","relevance":"Very High — medical devices, life-sciences, specifically has a renal division","specialty":null,"institution":null,"contact":"☎️ +966 11 462 1188 · ✉️ sales@amhsco.com","extra":"AMHSCO","extra_label":"Website"},{"num":2,"name":"AlwanMed","relevance":"Very High — licensed medical-device distributor; serves major government/private hospitals; tender submissions","specialty":null,"institution":null,"contact":"Contact through website","extra":"AlwanMed","extra_label":"Website"},{"num":3,"name":"Aman Medical","relevance":"Very High — explicitly supplies dialysis systems and medical devices","specialty":null,"institution":null,"contact":"☎️ +966 54 882 1508 · ✉️ info@amanmedical.com","extra":"Aman Medical","extra_label":"Website"},{"num":4,"name":"FUMEDCO / MNAF3 Arabia","relevance":"High — medical equipment, devices & disposables; supplies large government hospitals","specialty":null,"institution":null,"contact":"☎️ +966 11 400 3493 · ✉️ info@mnaf3arabia.com","extra":"FUMEDCO","extra_label":"Website"},{"num":5,"name":"House of Rays Medical","relevance":"High — 350+ healthcare clients; medical consumables; nationwide coverage","specialty":null,"institution":null,"contact":"Website / WhatsApp","extra":"House of Rays Medical","extra_label":"Website"},{"num":6,"name":"Nipras AlSalhiya Medical","relevance":"High — medical equipment/devices/accessories; branches Dammam, Riyadh, Jeddah, Tabuk, Khamis","specialty":null,"institution":null,"contact":"Website contact","extra":"Nipras Medical","extra_label":"Website"},{"num":7,"name":"Jama Medical","relevance":"High — nationwide logistics; Riyadh/Jeddah/Dammam/Qassim facilities","specialty":null,"institution":null,"contact":"Website contact","extra":"Jama Medical","extra_label":"Website"},{"num":8,"name":"Watan Medical Company","relevance":"High — medical devices, supplies & equipment across KSA","specialty":null,"institution":null,"contact":"☎️ +966 13 833 3606 · ✉️ info@watanmedical.com","extra":"Watan Medical","extra_label":"Website"},{"num":9,"name":"Healthcare Systems Saudi","relevance":"Medium–High — medical consumables, hospital supplies; serves MOH, military, National Guard and private hospitals","specialty":null,"institution":null,"contact":"☎️ +966 92 000 4438 · ✉️ sales@hs-saudi.com","extra":"Healthcare Systems Saudi","extra_label":"Website"},{"num":10,"name":"Raqwani Medicals","relevance":"Medium–High — medical devices, equipment, surgical supplies and hospital products","specialty":null,"institution":null,"contact":"☎️ +966 56 393 3574 / +966 50 124 3758 · ✉️ info@raqwanimedicals.com","extra":"Raqwani Medicals","extra_label":"Website"}],"ae":[{"num":1,"name":"Majestic Medical & Technical Supplies","relevance":"Dialysis-specific; explicitly has a dialysis division","specialty":null,"institution":null,"contact":"☎️ +971 2 632 6999 / +971 4 227 8883 · ✉️ info@majesticmedical.ae","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Samir Medical Supplies","relevance":"Medical equipment/distribution; Dubai + Abu Dhabi","specialty":null,"institution":null,"contact":"☎️ +971 4 442 1118 / +971 2 445 3228 · ✉️ info@sdtdxb.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Unicare Medical Trading","relevance":"Healthcare distribution + UAE-wide logistics","specialty":null,"institution":null,"contact":"☎️ +971 4 255 3999 · Abu Dhabi +971 2 443 5500","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Al Naghi Medical","relevance":"Major medical distribution; Dubai + Abu Dhabi","specialty":null,"institution":null,"contact":"☎️ +971 4 512 6500 · +971 2 691 3222 · ✉️ naghi@naghimedical.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"MAS Medical Equipment & Supplies","relevance":"Hospital/medical equipment supplier; Dubai + Abu Dhabi","specialty":null,"institution":null,"contact":"☎️ +971 4 399 4919 · +971 2 554 4094 · ✉️ info@mas-uae.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":6,"name":"Olive Medical Equipment Trading","relevance":"Medical/surgical supplies, devices & consumables; UAE-wide","specialty":null,"institution":null,"contact":"☎️ +971 55 900 3182 · ✉️ sales@olivemed.ae","extra":"🟠 4/5","extra_label":"Priority"},{"num":7,"name":"Dupharm","relevance":"Medical consumables + equipment; established UAE distributor","specialty":null,"institution":null,"contact":"☎️ +971 4 268 5054 · ✉️ dupharm@dupharm.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":8,"name":"Life World Medical Supplies","relevance":"Medical supplies with Abu Dhabi, Al Ain & Dubai presence","specialty":null,"institution":null,"contact":"☎️ +971 50 777 1462 · ✉️ sales2@lifewrld.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"MEDINOVA Medical Supplies LLC","relevance":"Medical-supply company in Abu Dhabi","specialty":null,"institution":null,"contact":"☎️ +971 2 559 7275","extra":"🟡 3/5","extra_label":"Priority"},{"num":10,"name":"Westfort Trading LLC","relevance":"Medical-equipment supplier in Abu Dhabi","specialty":null,"institution":null,"contact":"☎️ +971 2 554 7371","extra":"🟡 3/5","extra_label":"Priority"}],"qa":[{"num":1,"name":"Fayn Al Tbyh / Fayn Medical","relevance":"Vascular access + medical consumables + distribution; explicitly offers vascular-access products and partnership/distribution services","specialty":null,"institution":null,"contact":"☎️ +974 4491 9296 / +974 4431 0911 · ✉️ info@fayn.qa","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Care Medical Trading","relevance":"Established medical-equipment distributor serving healthcare, diagnostics & life sciences","specialty":null,"institution":null,"contact":"Website/contact form","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Universal Trade Line (UTL)","relevance":"20+ years distributing medical equipment, consumables & laboratory products to government/private sectors","specialty":null,"institution":null,"contact":"Website/contact","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Barzan Medical Supplies","relevance":"Major Qatar healthcare distributor; medical equipment, hospital disposables & consumables","specialty":null,"institution":null,"contact":"☎️ +974 4441 0270 · ✉️ info@barzanmedical.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"Origin Trading & Contracting WLL","relevance":"Medical equipment + consumables + procurement/logistics; 13+ years","specialty":null,"institution":null,"contact":"☎️ +974 4002 0246 · ✉️ info@originqatar.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":6,"name":"Gulfmed Medical Supplies","relevance":"Medical-supply company in Doha","specialty":null,"institution":null,"contact":"☎️ +974 4486 6216","extra":"🟠 4/5","extra_label":"Priority"},{"num":7,"name":"Ibn Al Haytham Centre","relevance":"Medical devices/equipment + consumables + surgical instruments","specialty":null,"institution":null,"contact":"☎️ +974 4431 2283 · ✉️ sales@ibncentre.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":8,"name":"Novel Medical Solutions W.L.L.","relevance":"Healthcare supply & distribution company; wholesale medical supplies","specialty":null,"institution":null,"contact":"☎️ +974 4467 5151 · ✉️ info@novelmedsolution.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"GerminMED","relevance":"Medical-equipment supplier in Doha","specialty":null,"institution":null,"contact":"☎️ +974 4427 2148","extra":"🟡 3/5","extra_label":"Priority"},{"num":10,"name":"Dynamic Medical Supplies","relevance":"Medical equipment + medical supplies; Doha","specialty":null,"institution":null,"contact":"☎️ +974 7057 0595","extra":"🟡 3/5","extra_label":"Priority"}],"kw":[{"num":1,"name":"Leader Medical Company for Equipment and Medical Supplies W.L.L","relevance":"Medical equipment + supplies","specialty":null,"institution":null,"contact":"☎️ +965 2246 1967","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"DMC Trading Co.","relevance":"25+ years; supplies MOH, Ministry of Defense & private hospitals","specialty":null,"institution":null,"contact":"☎️ +965 6515 0700 · ✉️ info@dmc-kw.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"United Medical Commodities (UMC)","relevance":"20+ years; represents international medical manufacturers","specialty":null,"institution":null,"contact":"☎️ +965 2245 0815/6 · ✉️ info@medcom.com.kw","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Arabi Medical & Scientific Equipment","relevance":"Major healthcare supplier; explicitly supplies dialysis equipment + consumables","specialty":null,"institution":null,"contact":"Arabi Holding contact","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"Medical Means Co. / Al Redwan Group","relevance":"Major GCC dialysis/medical-supply organization","specialty":null,"institution":null,"contact":"Regional contact","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"Warba Medical Supplies Co","relevance":"Medical supplies","specialty":null,"institution":null,"contact":"☎️ +965 2232 3850","extra":"🟠 4/5","extra_label":"Priority"},{"num":7,"name":"Ahmed Company for Wholesale","relevance":"30+ years; clinical disposables, surgical tools & medical consumables; handles tenders","specialty":null,"institution":null,"contact":"Sales team / website","extra":"🟠 4/5","extra_label":"Priority"},{"num":8,"name":"Revan Middle East","relevance":"Medical equipment, surgical supplies & distribution","specialty":null,"institution":null,"contact":"☎️ +965 2573 7373 · ✉️ info@revankw.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"QuipMed","relevance":"Procurement + distribution of medical products","specialty":null,"institution":null,"contact":"☎️ +965 6902 8587 · ✉️ info@quipmed.co","extra":"🟠 4/5","extra_label":"Priority"},{"num":10,"name":"Dmetco","relevance":"Medical equipment + laboratory + pharmaceutical supplies","specialty":null,"institution":null,"contact":"☎️ +965 2241 6184","extra":"🟡 3/5","extra_label":"Priority"}],"om":[{"num":1,"name":"Oman Medical Supplies & Services (OMANMED)","relevance":"Medical equipment + surgical/general consumables; established hospital-supply operation","specialty":null,"institution":null,"contact":"☎️ +968 2459 3395 / +968 9012 6075 · ✉️ medical@omanmed.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Medical & Scientific Supplies LLC","relevance":"Imports/markets hospital equipment, surgical products, pharmaceuticals & consumables","specialty":null,"institution":null,"contact":"☎️ +968 2449 7844","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Al Farsi Medical Supplies (AFMS)","relevance":"Established importer/distributor; surgical consumables + medical equipment","specialty":null,"institution":null,"contact":"☎️ +968 2448 5625 · WhatsApp +968 9225 8225","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Niemath Al Noor Trading LLC (NieMed)","relevance":"Nationwide medical equipment + consumables; hospital/clinic supply","specialty":null,"institution":null,"contact":"☎️ +968 7928 3733 / +968 7952 7382 · ✉️ info@niemathalnoor.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"MSTE LLC","relevance":"Medical devices, consumables & disposables; large Muscat warehouse","specialty":null,"institution":null,"contact":"☎️ +968 2423 8417 · ✉️ info@msteoman.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"Seha Medical Supplies","relevance":"Medical equipment; cardiac & vascular solutions","specialty":null,"institution":null,"contact":"☎️ +968 2411 2944 · ✉️ info@seha.om","extra":"🟠 4/5","extra_label":"Priority"},{"num":7,"name":"MuscatMed / HUI Medical Supplies","relevance":"Importer/distributor of medical equipment & surgical disposables","specialty":null,"institution":null,"contact":"☎️ +968 7909 8973 / +968 9257 5465","extra":"🟠 4/5","extra_label":"Priority"},{"num":8,"name":"Mazoon Medical Supplies","relevance":"Public/private healthcare supply; consumables including catheters","specialty":null,"institution":null,"contact":"☎️ +968 9644 2500 · ✉️ info@mazoonmedical.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"Advanced Medical Instruments Co. (AMICO)","relevance":"Medical equipment, medical supplies & consumables","specialty":null,"institution":null,"contact":"Oman Yellow Pages / company contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":10,"name":"IBN Sina Medical Supply","relevance":"Hospital equipment, medical equipment & consumables","specialty":null,"institution":null,"contact":"Oman Yellow Pages / company contact","extra":"🟡 3/5","extra_label":"Priority"}],"jo":[{"num":1,"name":"Greenland Medical","relevance":"⭐ Vascular Access + Interventional Radiology specifically listed","specialty":null,"institution":null,"contact":"☎️ +962 6 515 6480 · +962 79 588 7422","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Hijazi Medical Supplies (HMS)","relevance":"⭐ Catheters + vascular/interventional products","specialty":null,"institution":null,"contact":"☎️ +962 6 515 4826 · ✉️ info@hijazibros.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"RAMANA Medical Supplies","relevance":"⭐ Vascular + interventional radiology; distributor for international companies","specialty":null,"institution":null,"contact":"Contact via website","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"NAJD Medical","relevance":"⭐ Interventional products; supplies major public/private hospitals","specialty":null,"institution":null,"contact":"☎️ +962 79 621 7161 · ✉️ elayan@najdmed.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"World Medical Supplies (WMS)","relevance":"⭐ Supplies Jordan MOH + Royal Medical Services","specialty":null,"institution":null,"contact":"☎️ +962 79 914 0755","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"United for Marketing","relevance":"⭐ Works directly with Jordan MOH and public/private hospitals","specialty":null,"institution":null,"contact":"Website contact","extra":"🔴 5/5","extra_label":"Priority"},{"num":7,"name":"Al-Ahlia Company","relevance":"Medical-device distributor since 1987; strong local infrastructure","specialty":null,"institution":null,"contact":"☎️ +962 6 465 0951 · +962 77 736 8181 · ✉️ info@ahliamed.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":8,"name":"Surur Medical","relevance":"Medical equipment + surgical consumables; hospital/medical-center distribution","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"Osoul Medical","relevance":"Medical equipment + healthcare consumables + procurement support","specialty":null,"institution":null,"contact":"☎️ +962 79 203 3336 · ✉️ info@osoulhealth.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":10,"name":"Mahmoud Moghrabi Medical Supplies","relevance":"Medical consumables/devices; private + selected public sector","specialty":null,"institution":null,"contact":"☎️ +962 6 552 0954 · ✉️ info@immc-jo.com","extra":"🟠 4/5","extra_label":"Priority"}],"lb":[{"num":1,"name":"MedTrust Solutions","relevance":"⭐ Vascular access + hemodialysis + endovascular","specialty":null,"institution":null,"contact":"☎️ +961 3 293 893 · ✉️ contact via website","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Allied Medical Group (AMG)","relevance":"⭐ Vascular/peripheral intervention + medical devices","specialty":null,"institution":null,"contact":"☎️/email via website","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Promedz Lebanon","relevance":"⭐ Interventional radiology + peripheral vascular + venous therapy","specialty":null,"institution":null,"contact":"☎️ +961 70 827 807 · +961 1 364 659/60 · ✉️ promedz@promedz.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Intelmed S.A.R.L.","relevance":"⭐ Vascular + interventional radiology + cardiothoracic surgery","specialty":null,"institution":null,"contact":"☎️ +961 1 425 724","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"Biofield Medical","relevance":"Specialized medical consumables for interventional fields","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":6,"name":"Hayek Investment / HayekInv Medical","relevance":"⭐ Disposable devices for IR + vascular surgery","specialty":null,"institution":null,"contact":"☎️ +961 1 87 33 81 · +961 3 66 22 72","extra":"🟠 4/5","extra_label":"Priority"},{"num":7,"name":"CryoLebanon & Medical Devices","relevance":"Medical devices + university hospitals + interventional-radiology network","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":8,"name":"Medical Value","relevance":"Medical equipment / hospital supplies","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"Medica Group Lebanon","relevance":"Medical devices + hospital/clinical supply","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":10,"name":"Medical Line","relevance":"Medical equipment + consumables / hospital distribution","specialty":null,"institution":null,"contact":"Website contact","extra":"🟡 3/5","extra_label":"Priority"}],"iq":[{"num":1,"name":"Jadarah Scientific Bureau","relevance":"⭐ Medical devices/consumables + MOH tenders + nationwide distribution","specialty":null,"institution":null,"contact":"☎️ +964 770 456 4216 · ✉️ info@jadarah-iq.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Ashur Scientific Bureau / Iraqi Medical Co.","relevance":"⭐ Medical equipment & supplies; dialysis equipment; MOH/KIMADIA experience","specialty":null,"institution":null,"contact":"☎️ +964 771 393 1032 · ✉️ info@iraqimedco.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Pro Mena","relevance":"⭐ Explicitly carries Central Venous Catheters + Dialysis products","specialty":null,"institution":null,"contact":"Website contact","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Saaeda / Al-Saeeda","relevance":"⭐ Medical-device distributor; strong dialysis ecosystem; Baghdad + Kurdistan","specialty":null,"institution":null,"contact":"☎️ +964 770 700 7727 / +964 770 700 7737 · ✉️ info@saaeda.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"DiaErbil Medical","relevance":"⭐ Interventional radiology + interventional devices; Kurdistan coverage","specialty":null,"institution":null,"contact":"Website contact","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"Nova Scientific Bureau","relevance":"Nationwide medical-device + surgical-supply distribution; 18+ governorates","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":7,"name":"PlusPharma","relevance":"Medical devices, supplies & diagnostics; Baghdad + Erbil","specialty":null,"institution":null,"contact":"☎️ +964 780 121 0339 / +964 770 423 0565 · ✉️ info@pluspharma-me.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":8,"name":"Al-Hokamaa Group","relevance":"Long-established Iraqi pharmaceutical/medical-supply distribution network","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"Faraj Med / Al-Faraj Al-Markazi","relevance":"Medical supplies distribution across Baghdad, Kurdistan, Basrah and other areas","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":10,"name":"Wadi Alnahrayn","relevance":"Medical equipment/supplies importer; nationwide distribution + MOH registration support","specialty":null,"institution":null,"contact":"☎️ +964 771 666 2808 / +964 770 242 0214 · ✉️ info@wadi-alnahrayn.com.iq","extra":"🟠 4/5","extra_label":"Priority"}],"bh":[{"num":1,"name":"Wael Pharmacy Co. W.L.L.","relevance":"⭐ Dialysis filters/bloodlines + vascular access devices + hospital consumables","specialty":null,"institution":null,"contact":"☎️ +973 1737 7000 · ✉️ sales@waelpharmacy.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Trilink","relevance":"⭐ Medical devices, cardiovascular devices, disposables; established 1997","specialty":null,"institution":null,"contact":"Website contact","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Gulf Corporation for Technology (GCT)","relevance":"⭐ Major Bahrain medical distributor; medical equipment + hospital supplies","specialty":null,"institution":null,"contact":"☎️ +973 17 239 399 · ✉️ office@gctbahrain.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Medica Healthcare Supply","relevance":"Medical/surgical/biomedical equipment + consumables","specialty":null,"institution":null,"contact":"☎️ +973 1756 4788 / 1791 0765 · ✉️ info@medica-healthcare.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":5,"name":"Better Medical Solutions","relevance":"⭐ Medical consumables + clinical sales + distribution","specialty":null,"institution":null,"contact":"☎️ +973 1753 2010 · ✉️ sales@bettermedicals.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":6,"name":"Gulf House Medical System","relevance":"Medical equipment + hospital solutions + scientific products","specialty":null,"institution":null,"contact":"☎️ +973 1741 1037 · ✉️ info@gulfhousemedical.com","extra":"🟠 4/5","extra_label":"Priority"},{"num":7,"name":"Innova Medical Technologies","relevance":"Authorized medical-equipment/surgical supplier; government + private healthcare","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":8,"name":"Sahha Tech Medical","relevance":"Medical-equipment distribution + clinical support; Bahrain/Saudi network","specialty":null,"institution":null,"contact":"Website contact","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"Medline Medical Equipment","relevance":"Medical equipment/device distribution + maintenance","specialty":null,"institution":null,"contact":"☎️ +973 1782 5581 · ✉️ sales@medlinemedicalbh.com","extra":"🟡 3/5","extra_label":"Priority"},{"num":10,"name":"Mohammed Fakhroo & Bros. W.L.L.","relevance":"⭐ Established medical-equipment distributor; Philips healthcare distributor","specialty":null,"institution":null,"contact":"☎️ +973 1725 3529","extra":"🟡 3/5","extra_label":"Priority"}]},"kols":{"sa":[{"num":1,"name":"Prof. Faissal A. M. Shaheen","relevance":null,"specialty":"⭐⭐⭐⭐⭐ Nephrology / transplantation","institution":"Dr. Soliman Fakeeh Hospital / SCOT","contact":"✉️ famshaheen@gmail.com","extra":null,"extra_label":""},{"num":2,"name":"Prof. Abdullah Al-Hwiesh","relevance":null,"specialty":"⭐⭐⭐⭐⭐ Nephrology / dialysis / vascular access","institution":"King Fahd Hospital of the University / IAU","contact":"✉️ ahwiesh@iau.edu.sa","extra":null,"extra_label":""},{"num":3,"name":"Dr. Abdullah Al Sayyari","relevance":null,"specialty":"⭐⭐⭐⭐⭐ Nephrology / dialysis","institution":"MNGHA / King Abdulaziz Medical City","contact":"MNGHA Nephrology Department","extra":null,"extra_label":""},{"num":4,"name":"Dr. Ali Alharbi","relevance":null,"specialty":"⭐⭐⭐⭐⭐ Nephrology / dialysis","institution":"Diaverum Saudi Arabia","contact":"Professional profile","extra":null,"extra_label":""},{"num":5,"name":"Dr. Dujanah Hassan Mousa","relevance":null,"specialty":"⭐⭐⭐⭐ Nephrology / dialysis","institution":"Diaverum Saudi Arabia","contact":"Diaverum Saudi Arabia","extra":null,"extra_label":""},{"num":6,"name":"Dr. Mohammed Alhomrany","relevance":null,"specialty":"⭐⭐⭐⭐ Nephrology / dialysis","institution":"Diaverum Saudi Arabia","contact":"Diaverum Saudi Arabia","extra":null,"extra_label":""},{"num":7,"name":"Dr. Fayez Alhejaili","relevance":null,"specialty":"⭐⭐⭐⭐ Nephrology / dialysis","institution":"Diaverum Saudi Arabia","contact":"Diaverum Saudi Arabia","extra":null,"extra_label":""},{"num":8,"name":"Dr. Hassan Alshehri","relevance":null,"specialty":"⭐⭐⭐⭐ Interventional Radiology","institution":"Prince Sultan Military Medical City, Riyadh","contact":"Saudi Interventional Radiology Society","extra":null,"extra_label":""},{"num":9,"name":"Dr. Shaker Alshehri","relevance":null,"specialty":"⭐⭐⭐⭐ Vascular & Interventional Radiology","institution":"King Abdulaziz Medical City, Riyadh","contact":"Saudi Interventional Radiology Society","extra":null,"extra_label":""},{"num":10,"name":"Dr. Shagran Binkhamis","relevance":null,"specialty":"⭐⭐⭐⭐ Vascular & Interventional Radiology","institution":"King Faisal Specialist Hospital & Research Centre","contact":"Saudi Interventional Radiology Society","extra":null,"extra_label":""}],"ae":[{"num":1,"name":"Dr. Ayman Kamal Almadani","relevance":null,"specialty":"Nephrology / dialysis leadership","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":null,"extra_label":""},{"num":2,"name":"Dr. Wasim Ahmed","relevance":null,"specialty":"Nephrology / advanced HD","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":null,"extra_label":""},{"num":3,"name":"Dr. Salaheldin Khalil Issa","relevance":null,"specialty":"Nephrology / advanced HD","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":null,"extra_label":""},{"num":4,"name":"Dr. Hormaz Dara Dastoor","relevance":null,"specialty":"Nephrology / advanced HD","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":null,"extra_label":""},{"num":5,"name":"Dr. Mohammad Raafat Al Hakim","relevance":null,"specialty":"Nephrology / dialysis / RRT","institution":"SEHA Kidney Care – Al Ain / Tawam","contact":"SEHA appointment/contact","extra":null,"extra_label":""},{"num":6,"name":"Dr. Anvar Hussain Hamid Khan","relevance":null,"specialty":"Nephrology / vascular disease / HD","institution":"SEHA Kidney Care","contact":"☎️ 80050 / SEHA appointment","extra":null,"extra_label":""},{"num":7,"name":"Dr. Mohamed Hassan","relevance":null,"specialty":"Nephrology / HD / PD / transplant","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":null,"extra_label":""},{"num":8,"name":"Dr. Abraham George","relevance":null,"specialty":"Nephrology / HD / vascular disease","institution":"SEHA Kidney Care – Al Ain","contact":"SEHA appointment/contact","extra":null,"extra_label":""},{"num":9,"name":"Dr. Hefsa Al Shamsi","relevance":null,"specialty":"Nephrology / HD / transplantation","institution":"SEHA Kidney Care","contact":"SEHA appointment/contact","extra":null,"extra_label":""},{"num":10,"name":"Dr. Fadi Hijazi","relevance":null,"specialty":"Nephrology","institution":"Cleveland Clinic Abu Dhabi","contact":"Cleveland Clinic Abu Dhabi appointment","extra":null,"extra_label":""}],"qa":[{"num":1,"name":"Dr. Hassan Al-Malki","relevance":null,"specialty":"⭐ Nephrology / dialysis leadership","institution":"HMC","contact":"HMC +974 4439 5777","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Dr. Omar Fituri","relevance":null,"specialty":"⭐ Nephrology / transplant / RRT","institution":"HMC + Weill Cornell Medicine-Qatar","contact":"HMC / WCM-Q","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Dr. Muhammad Asim","relevance":null,"specialty":"⭐ Senior nephrology / dialysis / CRRT","institution":"HMC","contact":"HMC +974 4439 5777","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Dr. Ihab T. M. Elmadhoun","relevance":null,"specialty":"⭐ Nephrology / CRRT / dialysis","institution":"HMC","contact":"HMC +974 4439 5777","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"Dr. Abdullah Ibrahim Hamad","relevance":null,"specialty":"⭐ Nephrology / dialysis","institution":"HMC","contact":"HMC +974 4439 5777","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"Dr. Muftah Othman","relevance":null,"specialty":"⭐ Senior nephrology / dialysis","institution":"HMC","contact":"HMC +974 4439 5777","extra":"🔴 5/5","extra_label":"Priority"},{"num":7,"name":"Dr. Khaled Mahmoud","relevance":null,"specialty":"⭐ Nephrology / dialysis","institution":"HMC","contact":"HMC +974 4439 5777","extra":"🔴 5/5","extra_label":"Priority"},{"num":8,"name":"Dr. Alaedine Shurrab","relevance":null,"specialty":"⭐ Nephrology / renal replacement therapy","institution":"HMC / Al Khor Hospital","contact":"HMC +974 4439 5777","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"Dr. Awais Nauman","relevance":null,"specialty":"Nephrology / renal medicine","institution":"HMC","contact":"HMC +974 4439 5777","extra":"🟠 4/5","extra_label":"Priority"},{"num":10,"name":"Dr. Ali A. Haydar","relevance":null,"specialty":"⭐ Interventional radiology / vascular intervention","institution":"Aman Hospital","contact":"☎️ +974 4400 4400 · ✉️ [email protected]","extra":"🔴 5/5","extra_label":"Priority"}],"kw":[{"num":1,"name":"Prof. Hamed Al-Essa","relevance":null,"specialty":"⭐ Nephrology / transplant / dialysis","institution":"Kuwait renal network","contact":"MOH / hospital","extra":null,"extra_label":"Priority"},{"num":2,"name":"Dr. Hamad Behbehani","relevance":null,"specialty":"⭐ Nephrology / renal medicine","institution":"Kuwait MOH","contact":"MOH / hospital","extra":null,"extra_label":"Priority"},{"num":3,"name":"Dr. Omar Al-Hunidi","relevance":null,"specialty":"⭐ Nephrology / renal medicine","institution":"Kuwait","contact":"Hospital / clinic","extra":null,"extra_label":"Priority"},{"num":4,"name":"Dr. Ahmed Ramadan","relevance":null,"specialty":"Nephrology / renal medicine","institution":"Amiri Hospital","contact":"MOH / Amiri","extra":null,"extra_label":"Priority"},{"num":5,"name":"Dr. Hisham Al-Sabah","relevance":null,"specialty":"Nephrology / renal medicine","institution":"Kuwait MOH","contact":"MOH","extra":null,"extra_label":"Priority"},{"num":6,"name":"Dr. Abdulaziz Al-Mousawi","relevance":null,"specialty":"Nephrology / dialysis","institution":"Kuwait MOH","contact":"MOH / hospital","extra":null,"extra_label":"Priority"},{"num":7,"name":"Dr. Mohammed Al-Mousawi","relevance":null,"specialty":"Nephrology / renal medicine","institution":"Kuwait","contact":"MOH / hospital","extra":null,"extra_label":"Priority"},{"num":8,"name":"Dr. Khaled Al-Sabah","relevance":null,"specialty":"Nephrology / renal medicine","institution":"Kuwait","contact":"MOH / hospital","extra":null,"extra_label":"Priority"},{"num":9,"name":"Dr. Faisal Al-Rashidi","relevance":null,"specialty":"Nephrology / dialysis","institution":"Kuwait","contact":"MOH / hospital","extra":null,"extra_label":"Priority"},{"num":10,"name":"Dr. Ahmed Al-Sabah","relevance":null,"specialty":"Renal medicine / transplantation","institution":"Kuwait","contact":"MOH / hospital","extra":null,"extra_label":"Priority"}],"om":[{"num":1,"name":"Dr. Dawood Al-Riyami","relevance":null,"specialty":"⭐ Nephrology / dialysis","institution":"Sultan Qaboos University Hospital","contact":"✉️ dawood@squ.edu.om","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Dr. Ali Al Lawati","relevance":null,"specialty":"⭐ Nephrology / dialysis","institution":"Sultan Qaboos University Hospital","contact":"✉️ aallawati@squ.edu.om","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Dr. Sadiq Al Lawati","relevance":null,"specialty":"⭐ Senior Consultant Nephrologist","institution":"Royal Hospital","contact":"Royal Hospital / MOH","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Dr. Issa Al Salmi","relevance":null,"specialty":"⭐ Senior Consultant Nephrologist","institution":"Royal Hospital","contact":"Royal Hospital / MOH","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"Dr. Alan Hola","relevance":null,"specialty":"⭐ Senior Consultant Nephrologist","institution":"Royal Hospital","contact":"Royal Hospital / MOH","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"Dr. Mahmood Nasser Al Hajiry","relevance":null,"specialty":"⭐ IR / dialysis access / PermCath / PD catheter","institution":"Royal Hospital","contact":"Aster / Royal Hospital","extra":"🔴 5/5","extra_label":"Priority"},{"num":7,"name":"Dr. Tamer Sayed Fouad","relevance":null,"specialty":"⭐ Vascular & endovascular surgery / HD access","institution":"Burjeel Hospital Oman","contact":"Burjeel Hospital","extra":"🔴 5/5","extra_label":"Priority"},{"num":8,"name":"Dr. Said Al-Lamki","relevance":null,"specialty":"⭐ Interventional Radiology / central venous catheter insertion","institution":"Burjeel Hospital Muscat","contact":"Burjeel Hospital","extra":"🔴 5/5","extra_label":"Priority"},{"num":9,"name":"Dr. Faisal Al Balushi","relevance":null,"specialty":"Interventional Radiology","institution":"Royal Hospital","contact":"Oman Vascular Society / Royal Hospital","extra":"🟠 4/5","extra_label":"Priority"},{"num":10,"name":"Dr. Suliman Al Shamsi","relevance":null,"specialty":"⭐ Senior Consultant Vascular Surgeon","institution":"Royal Hospital","contact":"Royal Hospital / MOH","extra":"🔴 5/5","extra_label":"Priority"}],"jo":[{"num":1,"name":"Prof. Riyad Abdel Raouf Saeed","relevance":null,"specialty":"⭐ Nephrology / kidney transplantation","institution":"Jordan Hospital","contact":"☎️ +962 6 560 8080","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Dr. Fouad Riad Saeed","relevance":null,"specialty":"⭐ Nephrology / transplantation","institution":"Jordan Hospital","contact":"☎️ +962 6 560 8080 · ✉️ info@jordan-hospital.com","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Dr. Bisher Kawar","relevance":null,"specialty":"⭐ Nephrology / dialysis / transplantation","institution":"Abdali Hospital","contact":"☎️ +962 6 510 9999","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Dr. Hiba Barghouthi","relevance":null,"specialty":"⭐ Nephrology","institution":"Abdali Hospital","contact":"☎️ +962 6 510 9999","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"Dr. Jawad Syouri","relevance":null,"specialty":"⭐ Nephrology / kidney transplant","institution":"Ibn Al-Haytham Hospital","contact":"Hospital: +962 6 569 4420","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"Dr. Ahmed Rashid","relevance":null,"specialty":"⭐ Nephrology / internal medicine","institution":"Al Khalidi Hospital","contact":"☎️ +962 6 464 4281","extra":"🔴 5/5","extra_label":"Priority"},{"num":7,"name":"Dr. Bashar Zuhair Ghosheh","relevance":null,"specialty":"⭐ Vascular Surgery","institution":"Jordan Hospital","contact":"☎️ +962 6 560 8080","extra":"🔴 5/5","extra_label":"Priority"},{"num":8,"name":"Dr. Omar Nader Hamdallah","relevance":null,"specialty":"⭐ Vascular surgery + catheterization + kidney transplant","institution":"Jordan Hospital / Jordan Vascular Clinic","contact":"☎️ Hospital +962 6 560 8080","extra":"🔴 5/5","extra_label":"Priority"},{"num":9,"name":"Dr. Sizeph Haddad","relevance":null,"specialty":"⭐ Vascular & Interventional Radiology","institution":"Abdali Hospital","contact":"☎️ +962 6 510 9999","extra":"🔴 5/5","extra_label":"Priority"},{"num":10,"name":"Dr. Farid Al-Adham","relevance":null,"specialty":"⭐ Interventional radiology / vascular catheter procedures","institution":"Amman","contact":"Vezeeta / clinic","extra":"🟠 4/5","extra_label":"Priority"}],"lb":[{"num":1,"name":"Dr. Hicham Cheikh Hassan","relevance":null,"specialty":"⭐ Nephrology / dialysis / renal vascular services","institution":"LAU Medical Center","contact":"LAU Medicine","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Prof. Dania Chelala","relevance":null,"specialty":"⭐ Nephrology / HD / transplantation","institution":"Hôtel-Dieu de France","contact":"HDF","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Dr. Hiba Azar","relevance":null,"specialty":"Nephrology / dialysis","institution":"Hôtel-Dieu de France","contact":"HDF","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Dr. Kassem Bdeiri","relevance":null,"specialty":"Nephrology / dialysis","institution":"Hôtel-Dieu de France","contact":"HDF","extra":"🟠 4/5","extra_label":"Priority"},{"num":5,"name":"Dr. Majdi Hamedeh","relevance":null,"specialty":"⭐ Nephrology + dialysis","institution":"Al Zahraa Hospital UMC","contact":"✉️ majdi.hmedeh@zhumc.org.lb · ☎️ +961 1 851040","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"Dr. Lynn Bou Khalil","relevance":null,"specialty":"⭐ Nephrology & Hypertension","institution":"Mount Lebanon Hospital UMC","contact":"☎️ +961 25 957 000","extra":"🔴 5/5","extra_label":"Priority"},{"num":7,"name":"Prof. Jamal Hoballah","relevance":null,"specialty":"⭐ Vascular surgery","institution":"AUB Medical Center","contact":"AUB","extra":"🔴 5/5","extra_label":"Priority"},{"num":8,"name":"Dr. Fady Haddad","relevance":null,"specialty":"⭐ Vascular Surgery","institution":"Mount Lebanon Hospital UMC","contact":"☎️ +961 25 957 000","extra":"🔴 5/5","extra_label":"Priority"},{"num":9,"name":"Dr. Abdallah Noufaily","relevance":null,"specialty":"⭐ Interventional vascular/nonvascular radiology","institution":"LAU Medical Center","contact":"☎️ +961 1 200800 ext. 6979","extra":"🔴 5/5","extra_label":"Priority"},{"num":10,"name":"Dr. Hadi Khoury","relevance":null,"specialty":"⭐ Interventional Radiology / vascular intervention","institution":"Khoury Vascular Clinic","contact":"KVC","extra":"🟠 4/5","extra_label":"Priority"}],"iq":[{"num":1,"name":"Prof. Arif Sami Malik","relevance":null,"specialty":"⭐ Nephrology / HD + PD","institution":"Al-Nahrain University / Iraq","contact":"✉️ dr.arifsami@nahrainuniv.edu.iq","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Dr. Zaid Ali","relevance":null,"specialty":"⭐ Vascular surgery / angiography / angioplasty","institution":"Ministry of Health, Al-Muthanna","contact":"PAIRS physician directory","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Dr. Fadhil Al-Ammar","relevance":null,"specialty":"Medical/academic leadership","institution":"Founder, Nova Scientific Bureau","contact":"Nova Scientific Bureau","extra":"🟠 4/5","extra_label":"Priority"},{"num":4,"name":"Dr. Abdul-Hadi Al-Hassan","relevance":null,"specialty":"Nephrology / renal medicine","institution":"Iraqi nephrology network","contact":"Hospital/professional route","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"Dr. Ahmed Al-Jubouri","relevance":null,"specialty":"Nephrology / dialysis","institution":"Iraqi renal-care network","contact":"Hospital/professional route","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"Dr. Ali Al-Mashhadani","relevance":null,"specialty":"Nephrology / dialysis","institution":"Baghdad","contact":"Hospital/professional route","extra":"🟠 4/5","extra_label":"Priority"},{"num":7,"name":"Dr. Raad Al-Khafaji","relevance":null,"specialty":"Vascular surgery","institution":"Baghdad / MOH","contact":"Hospital/professional route","extra":"🔴 5/5","extra_label":"Priority"},{"num":8,"name":"Dr. Haider Al-Saadi","relevance":null,"specialty":"Interventional radiology","institution":"Baghdad","contact":"Hospital/professional route","extra":"🔴 5/5","extra_label":"Priority"},{"num":9,"name":"Dr. Mohammed Al-Taie","relevance":null,"specialty":"Interventional radiology / vascular intervention","institution":"Baghdad","contact":"Hospital/professional route","extra":"🔴 5/5","extra_label":"Priority"},{"num":10,"name":"Dr. Ahmed Al-Bayati","relevance":null,"specialty":"Vascular / endovascular surgery","institution":"Iraq","contact":"Hospital/professional route","extra":"🟠 4/5","extra_label":"Priority"}],"bh":[{"num":1,"name":"Dr. Issa Kawalit","relevance":null,"specialty":"⭐ Nephrology + dialysis + transplant","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"🔴 5/5","extra_label":"Priority"},{"num":2,"name":"Dr. Abdulraqeeb Alomari","relevance":null,"specialty":"⭐ Nephrologist + kidney transplant","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"🔴 5/5","extra_label":"Priority"},{"num":3,"name":"Dr. Muhand Salemah Raji Eltwal","relevance":null,"specialty":"⭐ Nephrology","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"🔴 5/5","extra_label":"Priority"},{"num":4,"name":"Dr. Ahmed Mordi","relevance":null,"specialty":"⭐ Interventional Radiology + dialysis access","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800 · WhatsApp +973 3218 1810","extra":"🔴 5/5","extra_label":"Priority"},{"num":5,"name":"Dr. Wadie Yousif","relevance":null,"specialty":"⭐ Vascular & Interventional Radiology","institution":"Ibn Al-Nafees Hospital","contact":"☎️ +973 1782 8282 / 1782 8253","extra":"🔴 5/5","extra_label":"Priority"},{"num":6,"name":"Dr. Sharif Abdulsalam Hamza Khashaba","relevance":null,"specialty":"⭐ Vascular Surgery","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"🔴 5/5","extra_label":"Priority"},{"num":7,"name":"Dr. Sawsan Kadhem","relevance":null,"specialty":"Interventional Radiology","institution":"Dawali Clinics / Salmaniya","contact":"Hospital/clinic route","extra":"🟠 4/5","extra_label":"Priority"},{"num":8,"name":"Dr. Jinane Khaled","relevance":null,"specialty":"Radiology","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"🟠 4/5","extra_label":"Priority"},{"num":9,"name":"Dr. Suzanne Abbas","relevance":null,"specialty":"Radiology","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"🟠 4/5","extra_label":"Priority"},{"num":10,"name":"Dr. Fatema Abdulrahman","relevance":null,"specialty":"Radiology","institution":"Royal Bahrain Hospital","contact":"☎️ +973 1724 6800","extra":"🟠 4/5","extra_label":"Priority"}]}}

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

function networkContactParts(contact){
  const s=String(contact||'');
  const phones=(s.match(/(?:☎️|Phone:?|WhatsApp:?|Tel:?)[^·|✉️]*/gi)||[]).map(x=>x.trim()).join(' · ') || 'Not provided';
  const emails=(s.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}/gi)||[]).join(' · ') || 'Not provided';
  const route=(emails==='Not provided' && phones==='Not provided') ? (s||'Not provided') : (emails==='Not provided'?s.replace(/(?:☎️|Phone:?|WhatsApp:?|Tel:?)[^·|✉️]*/gi,'').trim():'Not provided');
  return {phones,emails,route};
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
  rows.forEach(r=>{r._extraLabel=r.extra_label||'';r._extra=r.extra||'';});
  const isDist=type==='distributors';
  const label=isDist?'Distributors':'KOLs';
  const icon=isDist?'🤝':'⭐';

  page.innerHTML=`
    <div class="network-shell network-table-only">
      <div class="network-clean-header">
        <button class="network-back" onclick="openCountry('${code}')">← Country Analysis</button>
        <div class="network-clean-title"><span class="network-clean-icon">${icon}</span><div><div class="network-title">${label} — ${meta.name}</div><div class="network-subtitle">${isDist?'Key distribution partners in this market':'Key opinion leaders in this market'}</div></div></div>
      </div>
      <div class="network-table-wrap">
        <div class="network-table-header">
          <div>
            <div class="network-table-title">${icon} ${label} — ${meta.name}</div>
            <div class="network-table-subtitle">${rows.length} ${label.toLowerCase()} listed · Source: ${isDist?'Distributors':'KOL_Catalog'} sheet</div>
          </div>
          <input id="network-search-${type}-${code}" class="network-search" type="text"
            placeholder="🔎 Search ${isDist?'distributor, relevance or contact':'KOL, specialty, institution or contact'}..."
            oninput="filterNetworkTable('${type}','${code}')">
        </div>
        <div class="network-table-scroll">
          <table class="network-table" id="network-table-${type}-${code}">
            <thead><tr>
              <th>#</th><th>${isDist?'Distributor':'KOL'}</th><th>${isDist?'AMECATH Relevance':'Specialty'}</th>
              ${isDist?'<th>Priority</th><th>Contact</th>':'<th>Institution</th><th>Priority</th><th>Contact</th>'}
            </tr></thead>
            <tbody>
              ${rows.map(r=>{
                const priority=String(r._extra||'—');
                const search=[r.name,r.relevance,r.specialty,r.institution,r.contact,r.extra].filter(Boolean).join(' ').toLowerCase();
                return `<tr data-search="${search}">
                  <td class="network-table-num">${r.num||'—'}</td>
                  <td><div class="network-table-name">${r.name||'—'}</div></td>
                  <td><div class="network-table-main">${isDist?(r.relevance||'—'):(r.specialty||'—')}</div></td>
                  ${isDist
                    ? `<td><span class="network-priority ${networkPriorityClass(priority)}">${priority}</span></td><td><div class="network-contact-cell">${r.contact||'—'}</div></td>`
                    : `<td><div class="network-table-main">${r.institution||'—'}</div></td><td><span class="network-priority ${networkPriorityClass(priority)}">${priority}</span></td><td><div class="network-contact-cell">${r.contact||'—'}</div></td>`}
                </tr>`;
              }).join('') || `<tr><td colspan="${isDist?5:6}" class="network-empty">No records available for this country.</td></tr>`}
            </tbody>
          </table>
        </div>
        <div class="network-table-footer"><span>Showing ${rows.length} ${label.toLowerCase()}</span><span>Country: ${meta.name}</span></div>
      </div>
    </div>`;
  window.scrollTo({top:0,behavior:'smooth'});
}

window.openNetwork=openNetwork;
function filterNetworkTable(type, code){

  const input = document.getElementById(
    `network-search-${type}-${code}`
  );

  const table = document.getElementById(
    `network-table-${type}-${code}`
  );

  if(!input || !table) return;

  const query = input.value.trim().toLowerCase();

  const rows = table.querySelectorAll('tbody tr');

  rows.forEach(row => {

    const searchText = (
      row.getAttribute('data-search') || ''
    ).toLowerCase();

    row.style.display =
      !query || searchText.includes(query)
        ? ''
        : 'none';

  });
}

window.filterNetworkTable = filterNetworkTable;
function formatMacroValue(v,type){
  if(v===null||v===undefined||v==='') return '—';
  if(type==='integer' && typeof v==='number') return v.toLocaleString();
  if(type==='percent' && typeof v==='number') return (v*100).toFixed(1)+'%';
  if(type==='money' && typeof v==='number') return '$'+v.toLocaleString(undefined,{maximumFractionDigits:2})+'M';
  return String(v);
}
function renderCompetitorShareChart(){
  const box=document.getElementById('competitor-share-chart-body');
  if(!box)return;
  const list=(competitorData[selectedCompetitorCountry]||[])
    .filter(x=>typeof x.share_mid==='number')
    .sort((a,b)=>b.share_mid-a.share_mid);
  if(!list.length){
    box.innerHTML='<div class="cid-chart-empty">No numeric market-share data available in Competitor_Matrix.</div>';
    return;
  }
  const max=Math.max(...list.map(x=>x.share_mid),1);
  box.innerHTML=list.map(c=>`<div class="cid-chart-row" title="${c.name}: ${c.share||'—'}">
    <div class="cid-chart-name">${c.name}</div>
    <div class="cid-chart-track"><div class="cid-chart-bar" style="width:${Math.max(2,c.share_mid/max*100)}%"></div></div>
    <div class="cid-chart-value">${c.share_mid.toFixed(1)}%</div>
  </div>`).join('')+
  '<div class="cid-chart-note">Chart value = midpoint of the workbook range for comparison (for example, 18–20% → 19%). Hover each bar to see the original workbook range.</div>';
}

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
   const macro = workbookData.macro[code] || {};
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
      <div class="cid-macro-section">
        <div class="cid-kpi-grid-final">
        ${[
          ["Population 2026",macro.population,"integer"],
          ["Est. 2026 HD",macro.hd,"integer"],
          ["Est. 2026 PD",macro.pd,"integer"],
          ["Annual Growth",macro.annual_growth,"percent"],
          ["Annual Catheter Demand",macro.demand,"integer"],
          ["Market Value",macro.market_value,"money"],
          ["Dialysis Facilities",macro.facilities,"integer"],
          ["Hospital Growth",macro.hospital_growth,"percent"],
          ["Unit Growth",macro.unit_growth,"percent"],
          ["HD Machines",macro.machines,"integer"],
          ["Nephrologists",macro.nephrologists,"text"],
          ["Vascular Surgeons",macro.vascular_surgeons,"text"],
          ["Radiologists",macro.radiologists,"text"],
          ["Healthcare Coverage",macro.coverage,"text"],
          ["OOP Share",macro.oop,"text"]
        ].map(k=>`<div class="cid-kpi-card-final"><div class="cid-kpi-icon-final">📊</div><div class="cid-kpi-content-final"><div class="cid-kpi-label-final">${k[0]}</div><div class="cid-kpi-value-final">${formatMacroValue(k[1],k[2])}</div></div></div>`).join('')}
        </div>
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

(function(){
  const ob=document.getElementById('our-asp-body');
  if(ob) ob.innerHTML=(workbookData.ourASP||[]).map(r=>`<tr style="border-bottom:1px solid #14284b;"><td style="padding:10px 14px;color:#e8edf5;font-weight:700;">${r.country}</td><td style="padding:10px 14px;color:#60a5fa;text-align:center;">$${r.short}</td><td style="padding:10px 14px;color:#60a5fa;text-align:center;">$${r.mid}</td><td style="padding:10px 14px;color:#60a5fa;text-align:center;">$${r.long}</td></tr>`).join('');
  const cb=document.getElementById('comp-asp-body');
  if(cb) cb.innerHTML=(workbookData.competitorASP||[]).map(r=>`<tr style="border-bottom:1px solid #14284b;"><td style="padding:10px 14px;color:#e8edf5;font-weight:600;">${r.company}</td><td style="padding:10px 14px;color:#c8d8f0;">${r.region}</td><td style="padding:10px 14px;color:#60a5fa;">${r.short}</td><td style="padding:10px 14px;color:#60a5fa;">${r.long}</td><td style="padding:10px 14px;color:#94a8c4;">${r.notes||'—'}</td></tr>`).join('');
})();
const competitorCountries={"sa":{"flag":"🇸🇦","name":"Saudi Arabia","market":"Largest market in the workbook scope","hd":30000,"pd":2200,"facilities":360,"machines":18000,"demand":77530,"marketValue":9.3},"ae":{"flag":"🇦🇪","name":"UAE","market":"Major GCC regional hub","hd":3000,"pd":120,"facilities":60,"machines":4500,"demand":7638,"marketValue":0.99},"qa":{"flag":"🇶🇦","name":"Qatar","market":"Centralized procurement market","hd":1200,"pd":180,"facilities":18,"machines":1100,"demand":3207,"marketValue":0.42},"kw":{"flag":"🇰🇼","name":"Kuwait","market":"GCC dialysis market","hd":2156,"pd":294,"facilities":25,"machines":3000,"demand":5728,"marketValue":0.72},"om":{"flag":"🇴🇲","name":"Oman","market":"Growing GCC dialysis market","hd":2500,"pd":100,"facilities":20,"machines":2200,"demand":6365,"marketValue":0.76},"jo":{"flag":"🇯🇴","name":"Jordan","market":"Levant medical hub","hd":6400,"pd":110,"facilities":50,"machines":2500,"demand":16127,"marketValue":1.61},"lb":{"flag":"🇱🇧","name":"Lebanon","market":"Levant market under pressure","hd":4730,"pd":210,"facilities":85,"machines":3000,"demand":12067,"marketValue":1.21},"iq":{"flag":"🇮🇶","name":"Iraq","market":"High-volume expansion market","hd":10721,"pd":450,"facilities":130,"machines":9000,"demand":27320,"marketValue":2.46},"bh":{"flag":"🇧🇭","name":"Bahrain","market":"Small high-income GCC market","hd":4547,"pd":450,"facilities":14,"machines":750,"demand":11885,"marketValue":1.43}};
const competitorData = workbookData.competitors;
let selectedCompetitorCountry='sa';
function renderCompetitors(){const country=competitorCountries[selectedCompetitorCountry],header=document.getElementById('competitor-country-header'),grid=document.getElementById('comp-grid');if(!header||!grid)return;const list=competitorData[selectedCompetitorCountry]||[];header.innerHTML=`<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3"><div><div class="comp-country-title">${country.flag} ${country.name}</div><div class="comp-country-sub">${country.market} · Source: Competitor_Matrix</div></div><div class="comp-summary"><div class="comp-summary-pill">🏢 ${list.length} Competitors</div><div class="comp-summary-pill">👥 HD ${country.hd.toLocaleString()}</div><div class="comp-summary-pill">💉 Demand ${country.demand.toLocaleString()}</div><div class="comp-summary-pill">💰 Market $${country.marketValue}M</div></div></div>`;renderCompetitorShareChart();grid.innerHTML=list.map((c,i)=>{const id='comp-detail-'+selectedCompetitorCountry+'-'+i;return `<div class="comp-card-new"><div class="comp-card-topline" style="background:#3b82f6;"></div><div class="flex justify-between items-start gap-3"><div><div class="comp-card-company">${c.name}</div><div class="comp-card-origin">${c.coverage}</div></div><span class="comp-threat-badge" style="background:rgba(59,130,246,.12);color:#60a5fa;border:1px solid rgba(59,130,246,.3);">${c.share}</span></div><div class="comp-share-row"><span>Market Share*</span><span class="comp-share-value">${c.share}</span></div><div class="comp-mini-grid"><div class="comp-mini-box"><span class="comp-mini-label">Main Advantage</span><span class="comp-mini-text">${c.advantage}</span></div><div class="comp-mini-box"><span class="comp-mini-label">Weakness / Gap</span><span class="comp-mini-text">${c.weakness}</span></div></div><div class="comp-edge"><b>Specializes in:</b> ${c.specializes}</div><button class="comp-details-btn" onclick="toggleCompetitorDetails('${id}',this)">View Details ↓</button><div class="comp-details-panel" id="${id}"><div class="comp-detail-row"><span class="comp-detail-label">Company</span><span class="comp-detail-value">${c.name}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Market Share*</span><span class="comp-detail-value">${c.share}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Coverage</span><span class="comp-detail-value">${c.coverage}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Main Advantage</span><span class="comp-detail-value">${c.advantage}</span></div><div class="comp-detail-row"><span class="comp-detail-label">Specializes in</span><span class="comp-detail-value">${c.specializes}</span></div><div style="margin-top:8px;color:#34d399;font-size:10px;line-height:1.45;"><b>AMECATH Competitive Advantage:</b> ${c.edge}</div></div></div>`;}).join('')||'<div class="placeholder-page">No competitor data available for this country.</div>'; }
function setCompetitorCountry(id,btn){selectedCompetitorCountry=id;document.querySelectorAll('.country-filter-btn').forEach(b=>b.classList.remove('comp-country-active'));if(btn)btn.classList.add('comp-country-active');renderCompetitors();}
function toggleCompetitorDetails(id,btn){const panel=document.getElementById(id);if(!panel)return;const open=panel.classList.toggle('open');btn.textContent=open?'Hide Details ↑':'View Details ↓';}
function filterCompetitors(type,btn){setCompetitorThreat(type,btn);}
function toggleDetails(btn){const panel=btn.closest('.comp-card-new')?.querySelector('.comp-details-panel');if(!panel)return;const open=panel.classList.toggle('open');btn.textContent=open?'Hide Details ↑':'View Details ↓';}
renderCompetitors();

let marketMap=null;
const marketPoints=[{"country": "🇸🇦 Saudi Arabia", "city": "Riyadh", "lat": 24.7136, "lng": 46.6753, "rank": 1, "area": "Riyadh (39 centers; ~19% of KSA centers; national dialysis PPP hub) [Expert Judgment]"}, {"country": "🇦🇪 UAE", "city": "Dubai", "lat": 25.2048, "lng": 55.2708, "rank": 1, "area": "Dubai (~7+ centers; ~28%+ of UAE centers; largest private market) [Expert Judgment]"}, {"country": "🇶🇦 Qatar", "city": "Doha", "lat": 25.2854, "lng": 51.531, "rank": 1, "area": "Doha – Fahad Bin Jassim Kidney Center + Hamad General (majority of Qatar's ~1,300 HD patients) [Sourced: HMC, Jul‑2026] hamad"}, {"country": "🇰🇼 Kuwait", "city": "Kuwait City", "lat": 29.3759, "lng": 47.9774, "rank": 1, "area": "Kuwait City – Al‑Sabah medical area (Al‑Nafisi Dialysis Center + MOH hubs) [Expert Judgment]"}, {"country": "🇴🇲 Oman", "city": "Muscat", "lat": 23.588, "lng": 58.3829, "rank": 1, "area": "Muscat (~4 centers; ~20% of Oman centers; Seeb, Al Amerat, Bousher) [Expert Judgment; Total: 20 centers, POI Data, Aug‑2026] poidata"}, {"country": "🇯🇴 Jordan", "city": "Amman", "lat": 31.9539, "lng": 35.9106, "rank": 1, "area": "Amman (~5 centers; ~50% of Jordan centers; Yarmouk, Al‑Basheer, King Abdullah Univ. Hospital) [Expert Judgment]"}, {"country": "🇱🇧 Lebanon", "city": "Beirut", "lat": 33.8938, "lng": 35.5018, "rank": 1, "area": "Greater Beirut (majority of ~4,730 HD patients; AUBMC, Hotel Dieu, Mount Lebanon Hospital) [Expert Judgment; Total: 78 centers, WHO/EMRO, 2025]"}, {"country": "🇮🇶 Iraq", "city": "Baghdad", "lat": 33.3152, "lng": 44.3661, "rank": 1, "area": "Baghdad (~11 centers; ~37% of Iraq centers; Baghdad Medical City, Marina, Sidral network) [Expert Judgment; Total: 10,721 HD patients, Iraqi Natl J Med, Jan‑2025]"}, {"country": "🇧🇭 Bahrain", "city": "Manama", "lat": 26.2235, "lng": 50.5876, "rank": 1, "area": "Manama / Riffa (H.H. Shaikh Abdullah Center, Royal Bahrain Hospital, Bahrain Specialist Hospital) [Expert Judgment; Total: 4,547 dialysis patients, Daily Tribune Bahrain, Jan‑2026]"}, {"country": "🇸🇦 Saudi Arabia", "city": "Jeddah", "lat": 21.4858, "lng": 39.1925, "rank": 2, "area": "Jeddah (12 centers; ~5.9%; major western hub; Diaverum + DaVita) [Expert Judgment]"}, {"country": "🇦🇪 UAE", "city": "Abu Dhabi", "lat": 24.4539, "lng": 54.3773, "rank": 2, "area": "Abu Dhabi (~5 centers; ~20%; SEHA Kidney Care network; Cleveland Clinic) [Expert Judgment]"}, {"country": "🇶🇦 Qatar", "city": "Doha", "lat": 25.2854, "lng": 51.531, "rank": 2, "area": "Doha – Al Wakrah / Al Shamal / Al Khor (HMC satellite units) [Expert Judgment]"}, {"country": "🇰🇼 Kuwait", "city": "Ahmadi", "lat": 29.0826, "lng": 48.0839, "rank": 2, "area": "Ahmadi (new 83‑unit Jaber Al‑Ahmad Kidney Dialysis Center, opened Aug‑2026) [Expert Judgment; Total: 2,450 dialysis patients, Arab Times, Mar‑2025]"}, {"country": "🇴🇲 Oman", "city": "Salalah", "lat": 17.0194, "lng": 54.0897, "rank": 2, "area": "Salalah (secondary southern hub; regional hospitals) [Expert Judgment]"}, {"country": "🇯🇴 Jordan", "city": "Irbid", "lat": 32.5556, "lng": 35.85, "rank": 2, "area": "Irbid (Yarmouk Hospital dialysis unit; northern Jordan hub) [Expert Judgment]"}, {"country": "🇱🇧 Lebanon", "city": "Tripoli", "lat": 34.4367, "lng": 35.8497, "rank": 2, "area": "Tripoli (secondary northern hub; public hospital dialysis) [Expert Judgment]"}, {"country": "🇮🇶 Iraq", "city": "Basra", "lat": 30.5085, "lng": 47.7804, "rank": 2, "area": "Basra (3+ centers; southern Iraq hub; major MOH hospitals) [Expert Judgment]"}, {"country": "🇧🇭 Bahrain", "city": "A'Ali", "lat": 26.13, "lng": 50.555, "rank": 2, "area": "A'Ali (King Hamad American Mission Hospital – large catchment) [Expert Judgment]"}, {"country": "🇸🇦 Saudi Arabia", "city": "Makkah", "lat": 21.3891, "lng": 39.8579, "rank": 3, "area": "Makkah (12 centers; ~5.9%; high seasonal patient flow) [Expert Judgment]"}, {"country": "🇦🇪 UAE", "city": "Sharjah", "lat": 25.3463, "lng": 55.4209, "rank": 3, "area": "Sharjah (~3 centers; ~12%; public + private mix) [Expert Judgment]"}, {"country": "🇶🇦 Qatar", "city": "Doha", "lat": 25.2854, "lng": 51.531, "rank": 3, "area": "Doha – Al Shahania (HMC unit) [Expert Judgment]"}, {"country": "🇰🇼 Kuwait", "city": "Hawalli", "lat": 29.3375, "lng": 48.0281, "rank": 3, "area": "Hawalli (established MOH dialysis units) [Expert Judgment]"}, {"country": "🇴🇲 Oman", "city": "Ibri", "lat": 23.2257, "lng": 56.5157, "rank": 3, "area": "Ibri (2 centers; ~10%; Ibri Referral Hospital PD unit) [Expert Judgment]"}, {"country": "🇯🇴 Jordan", "city": "Zarqa", "lat": 32.0728, "lng": 36.0879, "rank": 3, "area": "Zarqa (growing urban center; private hospitals) [Expert Judgment]"}, {"country": "🇱🇧 Lebanon", "city": "Sidon", "lat": 33.5571, "lng": 35.3729, "rank": 3, "area": "Sidon (southern Lebanon hub; government hospital dialysis) [Expert Judgment]"}, {"country": "🇮🇶 Iraq", "city": "Erbil", "lat": 36.1911, "lng": 44.0092, "rank": 3, "area": "Erbil (Kurdistan; >3,000 dialysis patients in KRI; private + public centers) [Expert Judgment]"}, {"country": "🇧🇭 Bahrain", "city": "Muharraq", "lat": 26.2572, "lng": 50.6119, "rank": 3, "area": "Muharraq (secondary urban cluster; private hospitals) [Expert Judgment]"}, {"country": "🇸🇦 Saudi Arabia", "city": "Dammam", "lat": 26.4207, "lng": 50.0888, "rank": 4, "area": "Dammam / Khobar (6+ centers; Eastern Province industrial hub) [Expert Judgment]"}, {"country": "🇦🇪 UAE", "city": "Al Ain", "lat": 24.2075, "lng": 55.7447, "rank": 4, "area": "Al Ain (SEHA Kidney Care – Al Ain Hospital) [Expert Judgment]"}, {"country": "🇶🇦 Qatar", "city": "Doha", "lat": 25.2854, "lng": 51.531, "rank": 4, "area": "Doha – Hamad General (central tertiary hub) [Sourced: HMC, Jul‑2026] hamad"}, {"country": "🇰🇼 Kuwait", "city": "Farwaniya", "lat": 29.2775, "lng": 47.9586, "rank": 4, "area": "Farwaniya (MOH dialysis units) [Expert Judgment]"}, {"country": "🇴🇲 Oman", "city": "Sohar", "lat": 24.342, "lng": 56.729, "rank": 4, "area": "Sohar (2 centers; ~10%; northern Oman hub) [Expert Judgment]"}, {"country": "🇯🇴 Jordan", "city": "Salt", "lat": 32.0392, "lng": 35.7272, "rank": 4, "area": "Salt (secondary Amman metro; private hospitals) [Expert Judgment]"}, {"country": "🇱🇧 Lebanon", "city": "Zahle", "lat": 33.8475, "lng": 35.902, "rank": 4, "area": "Zahle (eastern Lebanon hub; private hospitals) [Expert Judgment]"}, {"country": "🇮🇶 Iraq", "city": "Sulaymaniyah", "lat": 35.557, "lng": 45.435, "rank": 4, "area": "Sulaymaniyah (Kurdistan; major tertiary hospitals) [Expert Judgment]"}, {"country": "🇧🇭 Bahrain", "city": "Saar", "lat": 26.13, "lng": 50.555, "rank": 4, "area": "Saar (American Mission Hospital branch) [Expert Judgment]"}, {"country": "🇸🇦 Saudi Arabia", "city": "Madinah", "lat": 24.5247, "lng": 39.5692, "rank": 5, "area": "Madinah (5 centers; ~2.5%; western region hub) [Expert Judgment]"}, {"country": "🇦🇪 UAE", "city": "Ajman", "lat": 25.4052, "lng": 55.5136, "rank": 5, "area": "Ajman (~2 centers; ~8%; growing private sector) [Expert Judgment]"}, {"country": "🇶🇦 Qatar", "city": "Lusail", "lat": 25.9053, "lng": 51.55, "rank": 5, "area": "Lusail / Al Daayen (new urban growth; future clinics) [Expert Judgment]"}, {"country": "🇰🇼 Kuwait", "city": "Jahra", "lat": 29.3375, "lng": 47.6581, "rank": 5, "area": "Jahra (new medical city with dialysis component) [Expert Judgment]"}, {"country": "🇴🇲 Oman", "city": "Barka", "lat": 23.7077, "lng": 57.8899, "rank": 5, "area": "Barka / Seeb (new MOH units) [Expert Judgment]"}, {"country": "🇯🇴 Jordan", "city": "Karak", "lat": 31.1853, "lng": 35.7048, "rank": 5, "area": "Karak (southern Jordan; regional hospital) [Expert Judgment]"}, {"country": "🇱🇧 Lebanon", "city": "Nabatieh", "lat": 33.377, "lng": 35.483, "rank": 5, "area": "Nabatieh (southern Lebanon; regional hospital) [Expert Judgment]"}, {"country": "🇮🇶 Iraq", "city": "Kirkuk", "lat": 35.4681, "lng": 44.3922, "rank": 5, "area": "Kirkuk (Al‑Amal Center – ~463 patients) [Expert Judgment]"}, {"country": "🇧🇭 Bahrain", "city": "Riffa", "lat": 26.13, "lng": 50.555, "rank": 5, "area": "Riffa (additional private clinics) [Expert Judgment]"}, {"country": "🇸🇦 Saudi Arabia", "city": "Buraydah", "lat": 26.3592, "lng": 43.9818, "rank": 6, "area": "Buraydah (7 centers; ~3.4%; Qassim region hub) [Expert Judgment]"}, {"country": "🇦🇪 UAE", "city": "Fujairah", "lat": 25.1288, "lng": 56.3265, "rank": 6, "area": "Fujairah / Ras Al Khaimah (emerging northern emirates) [Expert Judgment]"}, {"country": "🇶🇦 Qatar", "city": "Mesaieed", "lat": 24.9909, "lng": 51.55, "rank": 6, "area": "Mesaieed / Al Wukair (industrial areas; future clinics) [Expert Judgment]"}, {"country": "🇰🇼 Kuwait", "city": "Sabah Al-Ahmad", "lat": 28.9304, "lng": 48.0903, "rank": 6, "area": "Sabah Al‑Ahmad Health Center (Sector E dialysis unit) [Expert Judgment]"}, {"country": "🇴🇲 Oman", "city": "Al Khaburah", "lat": 23.996, "lng": 57.32, "rank": 6, "area": "Al Khaburah / Al Suwayq (new MOH units) [Expert Judgment]"}, {"country": "🇯🇴 Jordan", "city": "Irbid", "lat": 32.5556, "lng": 35.85, "rank": 6, "area": "Irbid outskirts (private clinics) [Expert Judgment]"}, {"country": "🇱🇧 Lebanon", "city": "Jounieh", "lat": 34.1476, "lng": 35.6455, "rank": 6, "area": "Jounieh (coastal private hospitals) [Expert Judgment]"}, {"country": "🇮🇶 Iraq", "city": "Najaf", "lat": 32.0, "lng": 44.3333, "rank": 6, "area": "Najaf (religious tourism hub; growing private hospitals) [Expert Judgment]"}, {"country": "🇸🇦 Saudi Arabia", "city": "Hail", "lat": 27.5114, "lng": 41.7208, "rank": 7, "area": "Hail (6 centers; ~2.9%; northern region hub) [Expert Judgment]"}, {"country": "🇴🇲 Oman", "city": "Izki", "lat": 22.9333, "lng": 57.5333, "rank": 7, "area": "Izki / Ibra / Sinaw (interior hubs) [Expert Judgment]"}, {"country": "🇮🇶 Iraq", "city": "Diwaniyah", "lat": 31.999, "lng": 44.9255, "rank": 7, "area": "Diwaniyah / Amarah (regional MOH hospitals) [Expert Judgment]"}, {"country": "🇸🇦 Saudi Arabia", "city": "Taif", "lat": 21.4373, "lng": 40.5127, "rank": 8, "area": "Taif / Al Hofuf / Samtah (4 centers each; secondary western/eastern hubs) [Expert Judgment]"}, {"country": "🇴🇲 Oman", "city": "Muladdah", "lat": 23.6833, "lng": 57.8167, "rank": 8, "area": "Muladdah / Saham / حي عاصم (smaller towns) [Expert Judgment]"}, {"country": "🇮🇶 Iraq", "city": "Tikrit", "lat": 34.616, "lng": 43.683, "rank": 8, "area": "Tikrit / Fallouja / Ramadi (Sidral network centers) [Expert Judgment]"}, {"country": "🇸🇦 Saudi Arabia", "city": "Abha", "lat": 18.2164, "lng": 42.5053, "rank": 9, "area": "Abha / Khamis Mushait / Al Jubail / Al Mubarraz / Ar Rass / Arar / Tabuk (3 centers each) [Expert Judgment]"}, {"country": "🇮🇶 Iraq", "city": "Fallujah", "lat": 33.356, "lng": 43.786, "rank": 9, "area": "Mosul / Baqubah / Hilla (regional teaching hospitals) [Expert Judgment]"}, {"country": "🇸🇦 Saudi Arabia", "city": "Dhahran", "lat": 26.2361, "lng": 50.0393, "rank": 10, "area": "Secondary cities (1–2 centers each: Dhahran, Hafar Al Batin, Khulais, etc.) [Expert Judgment]"}, {"country": "🇮🇶 Iraq", "city": "Ramadi", "lat": 33.375, "lng": 43.964, "rank": 10, "area": "Secondary governorates (Diyala, Wasit, Maysan, etc.) [Expert Judgment]"}];
const priorityColors={Critical:"#ef4444",High:"#f97316",Medium:"#eab308",Low:"#22c55e"};

function hotAreaPriority(rank){
  if(rank===1)return "Critical";
  if(rank===2)return "High";
  if(rank<=5)return "Medium";
  return "Low";
}

function renderHotAreasTable(){
  const body=document.getElementById('hotareas-table-body'); if(!body)return;
  body.innerHTML=(workbookData.hotAreas||[]).map(r=>`<tr style="border-bottom:1px solid #14284b;">
    <td style="padding:10px 14px;color:#60a5fa;font-weight:800;">${r.rank}</td>
    <td style="padding:10px 14px;color:#e8edf5;font-weight:700;white-space:nowrap;">${r.country}</td>
    <td style="padding:10px 14px;color:#c8d8f0;line-height:1.45;">${r.area}</td>
  </tr>`).join('');
}

function createMarketMap(){
  const el=document.getElementById("market-map");
  if(!el || typeof L==="undefined")return;
  if(marketMap!==null){setTimeout(()=>marketMap.invalidateSize(),80);return;}
  marketMap=L.map("market-map",{zoomControl:true,scrollWheelZoom:true});
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:18,attribution:"&copy; OpenStreetMap contributors"}).addTo(marketMap);

  const layers=[];
  marketPoints.forEach(pt=>{
    const priority=hotAreaPriority(pt.rank);
    const color=priorityColors[priority];
    const radius=priority==="Critical"?13:priority==="High"?11:priority==="Medium"?9:7;
    const marker=L.circleMarker([pt.lat,pt.lng],{
      radius:radius,color:"#ffffff",weight:2,fillColor:color,fillOpacity:0.9
    }).addTo(marketMap);
    const country=String(pt.country||"").replace(/^[^A-Za-z]+/,"");
    marker.bindPopup(`<div class="map-popup">
      <div class="map-popup-title">${pt.city}, ${country}</div>
      <div class="map-popup-row"><b>Rank:</b> ${pt.rank}</div>
      <div class="map-popup-row"><b>Priority:</b> ${priority}</div>
      <div class="map-popup-row"><b>Hot area:</b> ${pt.area}</div>
    </div>`);
    if(pt.rank===1) marker.bindTooltip(`${pt.city} · ${country}`,{permanent:true,direction:"top",offset:[0,-10],className:"hot-label"});
    layers.push(marker);
  });

  if(layers.length){
    const group=L.featureGroup(layers);
    marketMap.fitBounds(group.getBounds().pad(0.18));
  }else{
    marketMap.setView([27.5,46.5],5);
  }

  const legend=L.control({position:"bottomright"});
  legend.onAdd=function(){
    const div=L.DomUtil.create("div");
    div.style.cssText="background:#0b1628;padding:10px 12px;border:1px solid #1e3d7a;border-radius:8px;color:#e8edf5;font-size:11px;";
    div.innerHTML='<div style="font-weight:700;margin-bottom:7px;color:#c8d8f0">MARKET PRIORITY</div><div>🔴 Critical</div><div>🟠 High</div><div>🟡 Medium</div><div>🟢 Low</div>';
    return div;
  };
  legend.addTo(marketMap);
  setTimeout(()=>marketMap.invalidateSize(),120);
}

renderHotAreasTable();

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
/* ─── COUNTRY FORECAST CHART ─── */
(function(){
  function initCountryForecastChart(){
    var sel=document.getElementById("forecast-country-chart-filter");
    var box=document.getElementById("forecast-country-chart");
    if(!sel || !box || typeof workbookData === "undefined" || !workbookData.forecast) return;
    var countries=workbookData.forecast.countries||[];
    if(!countries.length){
      box.innerHTML='<div style="padding:30px;text-align:center;color:#607a9f;font-size:11px;">No country forecast data available.</div>';
      return;
    }
    sel.innerHTML=countries.map(function(c){
      return '<option value="'+String(c.code||"").replace(/"/g,'&quot;')+'">'+String(c.country||"")+'</option>';
    }).join("");
    function fmt(v){
      return "$"+Number(v||0).toLocaleString("en-US",{maximumFractionDigits:0});
    }
    function render(){
      var c=countries.find(function(x){return String(x.code)===String(sel.value);})||countries[0];
      if(!sel.value) sel.value=c.code;
      var vals=[Number(c.revenue_2026||0),Number(c.revenue_2027||0),Number(c.revenue_2028||0)];
      var years=["2026","2027","2028"], max=Math.max.apply(null,vals)||1;
      var W=760,H=285,left=70,right=25,top=25,bottom=58,chartH=H-top-bottom,chartW=W-left-right;
      var step=chartW/3, barW=Math.min(110,step*0.48);
      var grid="";
      [0,.25,.5,.75,1].forEach(function(t){
        var y=top+chartH-(chartH*t);
        var v=max*t;
        grid+='<line x1="'+left+'" y1="'+y+'" x2="'+(W-right)+'" y2="'+y+'" stroke="#1e3d7a" stroke-width="1"'+(t===0?'':' stroke-dasharray="4,4"')+'/>';
        grid+='<text x="'+(left-9)+'" y="'+(y+4)+'" fill="#6a85b0" font-size="9" text-anchor="end">'+(v>=1000000?"$"+(v/1000000).toFixed(1)+"M":v>=1000?"$"+Math.round(v/1000)+"K":"$"+Math.round(v))+'</text>';
      });
      var bars="";
      vals.forEach(function(v,i){
        var h=chartH*(v/max), x=left+step*i+(step-barW)/2, y=top+chartH-h;
        bars+='<rect x="'+x+'" y="'+y+'" width="'+barW+'" height="'+h+'" fill="#60a5fa" rx="6"/>';
        bars+='<text x="'+(x+barW/2)+'" y="'+Math.max(y-8,14)+'" fill="#e8edf5" font-size="10" text-anchor="middle" font-weight="700">'+fmt(v)+'</text>';
        bars+='<text x="'+(x+barW/2)+'" y="'+(H-25)+'" fill="#c8d8f0" font-size="11" text-anchor="middle" font-weight="600">'+years[i]+'</text>';
      });
      var total=vals.reduce(function(a,b){return a+b;},0);
      box.innerHTML='<svg viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;">'+grid+bars+'</svg>'+
        '<div style="display:flex;justify-content:center;gap:28px;align-items:center;margin-top:8px;flex-wrap:wrap;">'+
        '<div style="font-size:11px;color:#c8d8f0;"><span style="display:inline-block;width:12px;height:12px;background:#60a5fa;border-radius:3px;margin-right:7px;vertical-align:-2px;"></span>'+String(c.country||"")+' — Base Case</div>'+
        '<div style="font-size:11px;color:#f59e0b;font-weight:700;">3-Year Total: '+fmt(total)+'</div></div>';
    }
    sel.addEventListener("change",render);
    render();
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",initCountryForecastChart);
  else initCountryForecastChart();
})();
/* ─── TENDERS ─── */
(function () {
  var tndrData = [{"id": 1, "country": "🇸🇦 Saudi Arabia", "name": "Medical Supplies – Direct Purchase", "ref": "NDP0802/26", "authority": "NUPCO (MOH)", "published": "01-Sep-2026", "deadline": "06‑Sep‑2026", "status": "Closed", "value": "$50K–$200K (est.)", "notes": "General medical supplies; may include catheters via INUPCO platform nupco+1", "priority": "Medium"}, {"id": 2, "country": "🇸🇦 Saudi Arabia", "name": "Respiratory Therapy & Anesthesia Supplies", "ref": "NDP0803/26", "authority": "NUPCO (SRM)", "published": "01-Sep-2026", "deadline": "07‑Sep‑2026", "status": "Closed", "value": "$100K–$300K (est.)", "notes": "Respiratory/anesthesia consumables; dialysis catheters not primary focus nupco", "priority": "Low"}, {"id": 3, "country": "🇸🇦 Saudi Arabia", "name": "General Medical Supplies", "ref": "NDP0801/26", "authority": "NUPCO", "published": "01-Sep-2026", "deadline": "03‑Sep‑2026", "status": "Closed", "value": "$50K–$150K (est.)", "notes": "General consumables; catheters possible but not specified nupco", "priority": "Medium"}, {"id": 4, "country": "🇸🇦 Saudi Arabia", "name": "Medical Supplies – Jazan Health Cluster", "ref": "NDP0798/26", "authority": "NUPCO (Jazan)", "published": "01-Sep-2026", "deadline": "10‑Sep‑2026", "status": "Open", "value": "$100K–$400K (est.)", "notes": "Medical devices & supplies; potential catheter inclusion nupco", "priority": "High"}, {"id": 5, "country": "🇸🇦 Saudi Arabia", "name": "Open Framework – Dialysis & Artificial Kidney Supplies", "ref": "NPT0043/26 (est.)", "authority": "NUPCO", "published": "01-Aug-2026", "deadline": "04‑Aug‑2026", "status": "Closed", "value": "$2M–$5M (est.)", "notes": "Direct dialysis consumables tender; framework agreement for HD/PD supplies nupco+1", "priority": "Critical"}, {"id": 6, "country": "🇶🇦 Qatar", "name": "Medical Supplies – HMC/MTCS/9120/2026", "ref": "133503238", "authority": "Hamad Medical Corp", "published": "01-Jan-2026", "deadline": "10‑Feb‑2026", "status": "Closed", "value": "$200K–$600K", "notes": "General medical supplies; dialysis items likely included hamad+1", "priority": "Medium"}, {"id": 7, "country": "🇶🇦 Qatar", "name": "Medical Consumables – HMC/TCS/9464/2026", "ref": "135633622", "authority": "Hamad Medical Corp", "published": "01-Feb-2026", "deadline": "16‑Mar‑2026", "status": "Closed", "value": "$300K–$800K", "notes": "Consumables blanket; catheters probable tendersontime", "priority": "High"}, {"id": 8, "country": "🇶🇦 Qatar", "name": "Medical Supplies – HMC/MTCS/9140/2026", "ref": "135634706", "authority": "Hamad Medical Corp", "published": "01-Feb-2026", "deadline": "02‑Mar‑2026", "status": "Closed", "value": "$200K–$500K", "notes": "General medical supplies tendersontime", "priority": "Medium"}, {"id": 9, "country": "🇴🇲 Oman", "name": "Medical Accessories 00047 (Re-tender)", "ref": "2026/2358/و ص/م ع م س م -212", "authority": "MOH Oman", "published": "10‑Aug‑2026", "deadline": "29‑Aug‑2026", "status": "Closed", "value": "$100K–$300K", "notes": "Medical accessories; may include catheters qatarrfp", "priority": "High"}, {"id": 10, "country": "🇴🇲 Oman", "name": "Supply of Renal Dialysis Consumables", "ref": "105094963", "authority": "MOH Oman", "published": "2024", "deadline": "14‑Aug‑2024", "status": "Closed", "value": "$500K–$1.5M", "notes": "Direct dialysis consumables; catheters included", "priority": "Critical"}, {"id": 11, "country": "🇴🇲 Oman", "name": "Medical Equipment for Dialysis Center (Re-tender)", "ref": "13733280", "authority": "MOH Oman", "published": "08‑Jul‑2026", "deadline": "22‑Jul‑2026", "status": "Closed", "value": "$300K–$800K", "notes": "Dialysis center equipment & consumables", "priority": "High"}, {"id": 12, "country": "🇦🇪 UAE", "name": "Medical Consumables – AJCH (5-Year Blanket)", "ref": "Various (TOT Ref.)", "authority": "Dubai Academic Health Corp", "published": "2026", "deadline": "Rolling", "status": "Active", "value": "$1M–$3M/year", "notes": "5-year blanket agreement; catheters included", "priority": "Critical"}, {"id": 13, "country": "🇦🇪 UAE", "name": "Hemodialysis Machine & Consumables", "ref": "112579009", "authority": "Health Entity (SEHA/DAHC)", "published": "2026", "deadline": "07‑May‑2026", "status": "Closed", "value": "$500K–$1.5M", "notes": "HD machines + consumables; catheters implied", "priority": "High"}, {"id": 14, "country": "🇧🇭 Bahrain", "name": "Supply of Dialysis Items (AKU & PDU)", "ref": "281/2024/BTB", "authority": "MOH Bahrain", "published": "27‑Mar‑2024", "deadline": "22‑May‑2024", "status": "Closed", "value": "$200K–$600K", "notes": "Dialysis consumables for government centers", "priority": "High"}, {"id": 15, "country": "🇯🇴 Jordan", "name": "Peritoneal Dialysis Consumables & Solutions", "ref": "103874338", "authority": "MOH Jordan", "published": "2025", "deadline": "18‑Nov‑2025", "status": "Closed", "value": "$150K–$400K", "notes": "PD consumables & solutions", "priority": "Medium"}, {"id": 16, "country": "🇯🇴 Jordan", "name": "Dialysis Machines – Yarmouk Hospital", "ref": "2026002412‑01", "authority": "MOH Jordan", "published": "06‑Aug‑2026", "deadline": "See notice", "status": "Open", "value": "$300K–$700K", "notes": "HD machines for Yarmouk Hospital", "priority": "High"}, {"id": 17, "country": "🇱🇧 Lebanon", "name": "Permanent & Single-Use Catheters (Re-Offer)", "ref": "133538485", "authority": "MOH / Public Hospitals", "published": "2026", "deadline": "16‑Jan‑2026", "status": "Closed", "value": "$100K–$300K", "notes": "Direct catheter tender; permanent + single-use", "priority": "Critical"}, {"id": 18, "country": "🇱🇧 Lebanon", "name": "Life-Saving Materials incl. Catheters", "ref": "132476287", "authority": "MOH / Public Hospitals", "published": "2025", "deadline": "09‑Jan‑2026", "status": "Closed", "value": "$200K–$500K", "notes": "Permanent + single-use catheters, urine bags, gauze", "priority": "High"}, {"id": 19, "country": "🇮🇶 Iraq", "name": "CVC & Other Catheters (Tender List)", "ref": "Various", "authority": "Kimadia / MOH Iraq", "published": "2025–2026", "deadline": "Rolling", "status": "Active", "value": "$500K–$2M/year", "notes": "Direct CVC/dialysis catheter tenders; Kimadia platform", "priority": "Critical"}, {"id": 20, "country": "🇰🇼 Kuwait", "name": "Dialysis Consumables & Equipment", "ref": "Various", "authority": "MOH Kuwait", "published": "2025–2026", "deadline": "Rolling", "status": "Active", "value": "$400K–$1.2M/year", "notes": "Dialysis consumables; listed on GCC aggregators", "priority": "High"}];


  var tndrCountryFilter = 'all';
  var tndrStatusFilter  = 'all';

  function tndrStatusClass(s) {
    if (s === 'Open')      return 'tndr-status-open';
    if (s === 'Submitted') return 'tndr-status-submitted';
    if (s === 'Won')       return 'tndr-status-won';
    return 'tndr-status-closed';
  }
  function tndrStatusLabel(s) { return s === 'Active' ? 'Active' : s; }

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
    /* Workbook register summary — source values are ranges, so no false summed total */
    html += '<tr>' +
      '<td colspan="4" style="padding:13px 14px;background:#10264a;color:#6a85b0;font-size:11px;font-weight:700;text-align:right;border-top:1px solid #1e3d7a;">WORKBOOK REGISTER</td>' +
      '<td style="padding:13px 14px;background:#10264a;color:#60a5fa;font-size:12px;font-weight:800;border-top:1px solid #1e3d7a;">20 tenders · $50K–$5M range</td>' +
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
