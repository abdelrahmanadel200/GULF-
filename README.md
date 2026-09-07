# AMECATH Executive Decision Engine

A clean Streamlit foundation for the AMECATH executive market-intelligence dashboard.

## Architecture

```text
amecath_decision_engine/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── components/
│   └── executive.py
├── utils/
│   └── pricing.py
├── data/
│   ├── loader.py
│   └── mock_data.py
└── pages/
    ├── executive_overview.py
    └── pricing.py
```

## Core modules

### Executive banner

```python
from components.executive import render_executive_banner

render_executive_banner(
    "CEO Decision Summary",
    [
        "Saudi Arabia is the largest current opportunity.",
        "UAE has strong growth and market-access potential.",
        "Normalize pricing before competitor comparison.",
    ],
)
```

### Fair pricing

```python
from utils.pricing import calculate_fair_price

hospital_price = calculate_fair_price(90, 0.35)
# 121.50
```

Formula:

`Estimated Hospital Price = Distributor Price × (1 + margin_pct)`

Allowed margin range: **20%–60%**.

### Source badge

```python
from components.executive import render_source_badge

render_source_badge(
    "NUPCO",
    "https://www.nupco.com/",
    "Tender values are taken from the validated procurement source.",
)
```

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Workbook integration

`data/loader.py` includes a controlled workbook loader for the existing AMECATH workbook. The UI currently starts from `data/mock_data.py` so the scaffold runs independently.

To move to the workbook, map validated sheets into the same normalized DataFrame schemas used by the pages.

## Important data rule

The pricing engine explicitly separates:

- AMECATH: Distributor Ex-Factory
- Competitors: Hospital / End-User

This prevents a misleading apples-to-oranges price comparison.

## Next implementation layer

The scaffold is intentionally ready for:

1. Country Opportunity Score
2. Market Entry Readiness
3. Competitor Attack Score
4. AMECATH current vs target share
5. Bottom-up 2026–2028 revenue forecast
6. Executive Decision Cards
7. Confidence / source lineage
