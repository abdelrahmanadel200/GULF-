# AMECATH Dashboard (React/TS) — Global Edition

Replaces the legacy Streamlit app (`legacy/dash_v2.py`) with a tabbed, all-country React
dashboard: **Overview**, **Country Data**, **Flash Cards**, **Insights**.

## Setup

```bash
npm install
npm run dev       # http://localhost:5173
npm run build     # production build
npm run test      # vitest — data integrity + Saudi-removal guard tests
```

## Data pipeline

All data ships pre-generated in `src/data/*.generated.ts`, sourced from
`data/Amecath_Dash.xlsx`. The app has **no runtime xlsx dependency or API layer** — this
mirrors the fact that the source data updates on a manual cadence, not live.

To refresh after a new workbook export:

```bash
npx ts-node scripts/etl/buildAll.ts
```

This writes `src/data/_raw_*.json` extracts for review, then hand-update the matching
`*.generated.ts` file (kept as plain TS, not auto-overwritten, so changes stay
human-diffable in pull requests).

Two parsers cover the two sheet layouts found in the real workbook:
- `scripts/etl/parseFlatSheet.ts` — sheets with a real `Country` column (`tenders`,
  `procurement body`, `our ASP`, `Sources`, `overview`).
- `scripts/etl/parseBlockedSheet.ts` — sheets stacked as one block per country with no
  `Country` column (`Distributors`, `COMPETITORS`, `KOLS`).

## Saudi-removal audit

```bash
grep -r "Saudi Arabia" src/components/
grep -r "\"SA\"" src/context/
grep -r "saudi" src/ --include="*.ts" --include="*.tsx" -i
```
Expected: zero hits outside `src/data/*.generated.ts`.

## Legacy app

`legacy/dash_v2.py` (Streamlit) is kept for reference during cutover but is deprecated —
note that it was already broken against the real `Amecath_Dash.xlsx` schema (it expects a
different workbook, `AMECATH_Master_Data.xlsx`, with unrelated sheet names) and should not
be used as a data-schema reference going forward.
