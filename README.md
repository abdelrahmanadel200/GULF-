# AMECATH Executive Intelligence Hub — v2

A Streamlit dashboard for AMECATH's GCC & MENA market intelligence.

---

## Repository Layout

```
amecath_dashboard/
├── dash_v2.py                        ← Main dashboard application
├── build_master_data.py              ← Data migration / sample generator
├── requirements.txt
├── README.md
├── AMECATH_Master_Data.xlsx          ← ⚠️ Single source of truth (see below)
│
└── assets/
    ├── logos/
    │   └── amecath_logo.png          ← Company logo (commit to repo)
    └── landscapes/
        ├── Saudi Arabia landscape.jpeg
        ├── UAE landscape.jpeg
        ├── Qatar landscape.jpeg
        ├── Kuwait landscape.jpeg
        ├── Oman landscape.jpeg
        ├── Bahrain landscape.jpeg
        ├── Jordan landscape.jpeg
        ├── Lebanon landscape.jpeg
        └── Egypt landscape.jpeg
```

> **Image naming convention:** `<Country Name> landscape.<ext>` (jpeg / jpg / png).
> File names are case-sensitive on Linux. Match exactly as listed above.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up the master data file

**Option A — Generate sample data (for testing):**

```bash
python build_master_data.py --sample
```

**Option B — Migrate from legacy per-country files:**

```bash
python build_master_data.py --merge path/to/country_excel_files/
```

### 3. Add images

Place landscape images and logo into `assets/landscapes/` and `assets/logos/` respectively.
These are **committed to the repository** — the dashboard reads them directly from disk.

### 4. Run the dashboard

```bash
streamlit run dash_v2.py
```

---

## Master Data File Schema

`AMECATH_Master_Data.xlsx` must contain these sheets:

| Sheet Name            | Required Columns | Purpose |
|-----------------------|-----------------|---------|
| `Overview_KPIs`       | country, dialysis_patients, market_size_usd_m, cagr_pct, top_competitor, amecath_share_pct, confidence_score, trend, last_updated | Overview tab — one row per country |
| `Macro_Summary`       | country, + macro fields | Macro tab |
| `7_Questions_Summary` | country, question, answer | 7-Questions tab |
| `Hospitals_Infra`     | country, hospital_name, city, bed_count, dialysis_stations | Hospitals tab |
| `Competitor_Matrix`   | country, competitor, market_share_pct, price_tier | Competitors tab |
| `Financials_Tenders`  | country, total_tam_usd_m, amecath_revenue_target_usd_m | Financials tab |
| `Forecast_Data`       | country, year, metric, value, scenario | Forecast tab |

Every sheet (except `Overview_KPIs`) must include a `country` column for filtering.

### Trend values (Overview_KPIs)

| Value    | Meaning |
|----------|---------|
| `up`     | Growing market, positive momentum |
| `down`   | Declining or challenged market |
| `stable` | Flat / steady state |

---

## Navigation Sections

| Tab | Content |
|-----|---------|
| 🌐 Overview | Consolidated KPI strip + 9-country mini-cards |
| 📊 Macro & Exec Summary | Country macro indicators |
| 📋 7 Questions Summary | Strategic Q&A framework |
| 🏥 Hospitals & Infrastructure | Facility-level data |
| ⚔️ Competitors & Pricing | Competitor matrix + deep-dive |
| 📈 Financials & Tenders | Revenue projections & tender pipeline |
| 🔮 Forecast | Scenario-based trend projections |

---

## Recommended Insight Types by Metric

| Metric | Insight Type | Example Output |
|--------|-------------|----------------|
| `dialysis_patients` | Benchmark comparison | "Saudi Arabia's 85k patients = 2.4× GCC average — priority market" |
| `market_size_usd_m` | Outlier detection | "UAE at $180M is 3.1σ above median — validate assumptions" |
| `cagr_pct` | Trend analysis | "Qatar CAGR 12.4% > regional avg 7.8% — high-growth opportunity" |
| `amecath_share_pct` | Gap analysis | "Jordan share 4.2% vs target 15% — 3.6× growth headroom" |
| `confidence_score` | Data quality flag | "Scores < 60: schedule in-country validation call" |
| `forecast / value` | Growth rate | "Bull scenario: +42% by 2029 vs Base +28%" |
| `active_tenders` | Pipeline analysis | "8 active tenders in KSA — highest regional pipeline" |

---

## Data Update Workflow

1. Update `AMECATH_Master_Data.xlsx` (any sheet, any row).
2. The dashboard auto-refreshes every **5 minutes** (`ttl=300` cache).
3. To force an immediate refresh: press **R** in the browser or restart Streamlit.

For live / automated updates, a simple file-watcher approach:

```python
# watch_and_reload.py — run alongside streamlit
import time, subprocess, hashlib, os

def file_hash(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()

path = "AMECATH_Master_Data.xlsx"
last = file_hash(path)
while True:
    time.sleep(30)
    current = file_hash(path)
    if current != last:
        print("File changed — Streamlit cache will auto-expire in <5 min")
        last = current
```

---

## Adding a New Country

1. Add the country to `COUNTRY_THEMES` in `dash_v2.py` (flag, colors, landmark).
2. Add the country's rows to every sheet in `AMECATH_Master_Data.xlsx`.
3. Place `<Country Name> landscape.jpeg` in `assets/landscapes/`.
4. Commit all three changes together.

---

## Production Checklist

- [ ] `AMECATH_Master_Data.xlsx` is populated with real data (not sample)
- [ ] All 9 landscape images are in `assets/landscapes/`
- [ ] `assets/logos/amecath_logo.png` is present
- [ ] `requirements.txt` pinned and installed
- [ ] `confidence_score` validated for all countries (flag any < 60)
- [ ] `last_updated` column reflects actual data vintage
- [ ] Streamlit secrets / environment variables set if deploying to Streamlit Cloud

---

## Extending the Dashboard

To add a new tab:
1. Add the label to the `nav_mode` radio list in the sidebar (Section 9 of `dash_v2.py`).
2. Write a `render_<name>(data, country, theme)` function (follow existing pattern).
3. Add a new `elif nav_mode == "..."` block in Section 11.
4. Add a new sheet name to `REQUIRED_SHEETS` and `AMECATH_Master_Data.xlsx`.
