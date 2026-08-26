# AMECATH Dashboard — Saudi‑Centric → Global (React/TS) Migration Plan v2

> **Scope correction (confirmed with stakeholder):** `dash__1_.py` is the current live app, and it is
> **Streamlit/Python, not React**. This is therefore a **Streamlit → React/TypeScript rewrite**, not an
> incremental refactor of an existing React codebase. Every "file change" below is a *new file to create*
> unless stated otherwise. Feature parity with `dash__1_.py`'s nav sections (Macro, 7‑Questions, Hospitals,
> Competitors, Financials, Forecast) is preserved by folding them into the four new tabs per the mapping
> table in §2.4, not by porting the Streamlit functions 1:1.

---

## 0. Validation Against Real Source Files

I opened `Amecath_Dash.xlsx` directly (11 sheets, not 9) and cross‑checked it against both
`dash__1_.py` and the previously drafted `amecath_global_migration_plan.md`. Results:

| Check | Result |
|---|---|
| `overview` sheet has exactly 9 country rows | ✅ Confirmed: SA, AE, QA, KW, OM, JO, LB, IQ, BH — **no Egypt**. Matches the original plan's `COUNTRIES` array, not `dash__1_.py`'s `COUNTRY_THEMES` (which invents an 8+Egypt list). |
| Numeric values in original plan's `COUNTRIES` constant | ✅ Confirmed exact match to `overview` sheet (population, HD/PD, demand, market value, ASPs) for every row spot‑checked. The data layer in the original plan is trustworthy — reuse it. |
| `dash__1_.py`'s expected workbook/sheets | ❌ **Does not match reality.** The script hard‑codes `AMECATH_Master_Data.xlsx` with sheets `Overview_KPIs`, `Macro_Summary`, `7_Questions_Summary`, `Hospitals_Infra`, `Competitor_Matrix`, `Financials_Tenders`, `Forecast_Data`. None of these exist in `Amecath_Dash.xlsx`. **`dash__1_.py` cannot currently load the real data at all** — treat its rendering logic as a rough UX reference only, never as a schema source. |
| Original plan's sheet inventory (9 sheets) | ⚠️ **Incomplete.** The real workbook has **11 sheets**: it's missing `KOLS` (full KOL directory — the `overview` sheet's `KOLs` field is only a *count*) and `Sources` (population/data citations). Both need schema entries — added in §1.2. |
| `Distributors` / `COMPETITORS` / `KOLS` sheet structure | ⚠️ **Correction needed.** These are **not** flat "Country column" tables as the original plan implied. Each is a stack of per‑country *blocks*: a lone country‑name row (e.g. `SAUDI ARABIA`), then a header row, then that country's data rows, repeated per country with no `Country` column. `tenders` and `procurement body`, by contrast, genuinely do have a per‑row `Country` column. This distinction changes the ETL step — see §3, Step 0. |
| `Hot Areas` structure | ✅ Confirmed: one column per country (flag+name header), rank rows underneath — matches original plan. |

**Net effect:** the original plan's *data model and field mappings are sound and reusable*; its *sheet
inventory and generic ETL description need the corrections above* before any parser code is written.

---

## 1. Data Model (Corrected)

### 1.1 Real workbook inventory (11 sheets)

| Sheet | Layout | Key Fields |
|---|---|---|
| `overview` | Flat, 1 row/country | `Country, Population 2026, Est. 2026 HD/PD, Annual Growth, total dialysis facilities, Hospital/Unit Growth, Nephrologists, Vascular Surgeons, Radiologists, HD Machines, Annual Catheter Demand, Market Value, coverage %, OOP share, Distributors (count), KOLs (count)` |
| `Hot Areas` | 1 column per country | `Rank`, then one cell per country with a free‑text city/detail string |
| `Distributors` | **Blocked by country** | `#, Distributor, Why relevant, Contact, Website` |
| `COMPETITORS` | **Blocked by country** | `Competitor, Market Share, Coverage, Weakness, Main Advantage, Specializes in, AMECATH Advantage` |
| `KOLS` *(missing from original plan)* | **Blocked by country** | `#, KOL, Specialty/relevance, Institution/route, Contact` |
| `tenders` | Flat, `Country` column | `Country, Tender Title, Ref/ID, Issuing Entity, Published, Closing, Value, Winner, Notes, Link` |
| `procurement body` | Flat, `Country` column | `Country, Primary Body, Secondary Buyers, Notes` |
| `our ASP` | Flat, 1 row/country | `Country, STD, Mid-Term, Tunneled` |
| `comp asp` | Flat, `Region`-grouped | `Company, Region, STD ASP, LTD ASP, Notes` (region ≠ single country — see §1.3) |
| `Revenue Forecast` | Free‑form exec block + rows | `Scenario, 2026‑2028 Revenue, Units, Comment` |
| `Sources` *(missing from original plan)* | Flat, 1 row/country | `Country, Population 2026, Source` |

### 1.2 Added types

```ts
// types/kol.ts
export interface KOL {
  id: string;
  countryId: string;
  name: string;
  specialty: string;
  institution: string;
  contact: string;
}

// types/source.ts
export interface DataSource {
  countryId: string;
  field: string;        // "population2026", etc.
  citation: string;      // raw citation text from the Sources sheet
}
```

Everything else in the original plan's `CountryRecord`, `CountryForecast`, `GlobalForecast`,
`FlashCard`, and `Insight` types (§2.1–2.3 of the v1 doc) is validated against real data and
**kept as‑is**. Field‑to‑tab mapping (§2.4 of v1) is also kept, with one addition:

| Field Group | Overview | Country Data | Flash Cards | Insights |
|---|---|---|---|---|
| `kols[]` (from new `KOLS` sheet) | — | ✅ Expandable KOL list per country | ✅ "Key opinion leader" spotlight card | — |
| `sources[]` (from new `Sources` sheet) | — | ✅ Footnote/citation panel | — | ✅ "Data confidence" note |

### 1.3 `comp asp` region caveat

`comp asp` rows are keyed by **region** (`"GCC (KSA, UAE, Qatar, Kuwait, Oman, Bahrain)"`,
`"Levant (Jordan, Lebanon)"`, `"Iraq"`), not by individual country. Do not attempt a 1:1
`countryId` join — instead add a `region` field on `CountryRecord` (already present) and join
`comp asp` rows to countries by region membership, exactly as the original plan's `region:
"GCC" | "Levant" | "Iraq"` field anticipates. This was actually handled correctly in the
original plan's type — just calling it out so the ETL code doesn't get written against a
false assumption of a per‑country `comp asp` row.

---

## 2. Corrected ETL — Block‑Structured Sheets

This is the concrete gap in the original plan. `Distributors`, `COMPETITORS`, and `KOLS` need a
different parser than `overview`, `tenders`, or `procurement body`.

```ts
// scripts/etl/parseBlockedSheet.ts
// Handles sheets shaped like:
//   [country name, null, null, ...]   <- block header (single non-empty cell)
//   [col1, col2, col3, ...]           <- column header row
//   [data...]
//   [data...]
//   [next country name, ...]          <- next block starts
//
// Used for: Distributors, COMPETITORS, KOLS

import { COUNTRY_NAME_TO_ID } from "../../src/data/countryLookup";

type Row = (string | number | null)[];

export interface BlockedRecord {
  countryId: string;
  row: Record<string, string | number | null>;
}

export function parseBlockedSheet(rows: Row[]): BlockedRecord[] {
  const out: BlockedRecord[] = [];
  let currentCountryId: string | null = null;
  let headers: string[] | null = null;

  for (const row of rows) {
    const nonEmpty = row.filter(c => c !== null && c !== "");

    // Block header: exactly one non-empty cell, and it matches a known country name
    if (nonEmpty.length === 1 && typeof row[0] === "string") {
      const id = COUNTRY_NAME_TO_ID[normalizeCountryName(row[0])];
      if (id) {
        currentCountryId = id;
        headers = null; // next row is the header row for this block
        continue;
      }
    }

    if (currentCountryId && headers === null) {
      headers = row.map(c => String(c ?? "").trim());
      continue;
    }

    if (currentCountryId && headers && nonEmpty.length > 0) {
      const record: Record<string, string | number | null> = {};
      headers.forEach((h, i) => { if (h) record[h] = row[i] ?? null; });
      out.push({ countryId: currentCountryId, row: record });
    }
  }
  return out;
}

function normalizeCountryName(raw: string): string {
  // Strips flag emoji / extra whitespace, upper/lower mismatches
  return raw.replace(/\p{Extended_Pictographic}/gu, "").trim().toUpperCase();
}
```

```ts
// src/data/countryLookup.ts
export const COUNTRY_NAME_TO_ID: Record<string, string> = {
  "SAUDI ARABIA": "SA", "UAE": "AE", "QATAR": "QA", "KUWAIT": "KW",
  "OMAN": "OM", "JORDAN": "JO", "LEBANON": "LB", "IRAQ": "IQ", "BAHRAIN": "BH",
};
```

Flat sheets (`overview`, `tenders`, `procurement body`, `our ASP`, `Sources`) parse with a
standard header‑row + `Country` column reader — no special‑casing needed; a plain
`XLSX.utils.sheet_to_json` (SheetJS) call is sufficient there.

---

## 3. Step‑by‑Step Build (Greenfield React/TS)

### Step 0 — One‑time data export (build‑time, not runtime)
Because this is a static, xlsx‑derived dataset (confirmed: no API/DB layer exists anywhere),
run the ETL **once at build time** with a Node script, not in the browser:

```
scripts/etl/
  parseBlockedSheet.ts
  parseFlatSheet.ts
  buildCountries.ts     // reads Amecath_Dash.xlsx -> writes src/data/countries.generated.ts
  buildKols.ts
  buildDistributors.ts
  buildCompetitors.ts
  buildTenders.ts
  buildSources.ts
```

Run via `npm run build:data` (wraps `ts-node scripts/etl/buildCountries.ts` etc.), committing
the generated `.generated.ts` files so the app has zero runtime dependency on `xlsx` parsing.
This directly replaces `dash__1_.py`'s `load_master_data()` + `@st.cache_data(ttl=300)` pattern
— there is no live re‑read requirement since Anthropic/AMECATH's own admission is this data
updates on a manual cadence, not in real time.

### Step 1 — Types (`src/types/*.ts`)
`country.ts`, `revenue.ts`, `insights.ts` exactly as in the original plan §2.1–2.3, plus
`kol.ts` and `source.ts` from §1.2 above.

### Step 2 — Generated data (`src/data/*.generated.ts`)
Output of Step 0. `countries.ts` re‑exports `COUNTRIES: CountryRecord[]` (9 entries, values
validated in §0 of this doc).

### Step 3 — Aggregations (`src/data/aggregations.ts`)
```ts
import { COUNTRIES } from "./countries.generated";

export function getGlobalTotals() {
  return {
    countryCount: COUNTRIES.length,
    totalPopulation: sum(COUNTRIES, c => c.population2026),
    totalPatients: sum(COUNTRIES, c => c.hdPatients2026 + c.pdPatients2026),
    totalCatheterDemand: sum(COUNTRIES, c => c.annualCatheterDemand),
    totalMarketValueUSD: sum(COUNTRIES, c => c.marketValueUSD),
    totalDistributors: sum(COUNTRIES, c => c.distributorCount),
    weightedAvgGrowth:
      sum(COUNTRIES, c => c.annualGrowthRate * c.marketValueUSD) /
      sum(COUNTRIES, c => c.marketValueUSD),
  };
}

function sum<T>(arr: T[], fn: (t: T) => number): number {
  return arr.reduce((s, x) => s + fn(x), 0);
}
```

### Step 4 — Context / centralized loader (`src/context/DataContext.tsx`)
```tsx
import React, { createContext, useContext, useEffect, useState } from "react";
import { COUNTRIES } from "../data/countries.generated";
import { CountryRecord } from "../types/country";

interface DataState {
  countries: CountryRecord[];
  status: "loading" | "ready" | "error";
  error?: string;
  selectedCountryId: string | null;      // null = global view (was hard-coded "SA")
  setSelectedCountryId: (id: string | null) => void;
}

const DataContext = createContext<DataState | undefined>(undefined);

export function DataProvider({ children }: { children: React.ReactNode }) {
  const [status, setStatus] = useState<DataState["status"]>("loading");
  const [error, setError] = useState<string>();
  const [selectedCountryId, setSelectedCountryId] = useState<string | null>(null); // ✅ global default

  useEffect(() => {
    try {
      if (!COUNTRIES.length) throw new Error("No country data generated — rerun `npm run build:data`.");
      setStatus("ready");
    } catch (e) {
      setError((e as Error).message);
      setStatus("error");
    }
  }, []);

  return (
    <DataContext.Provider value={{ countries: COUNTRIES, status, error, selectedCountryId, setSelectedCountryId }}>
      {children}
    </DataContext.Provider>
  );
}

export function useData() {
  const ctx = useContext(DataContext);
  if (!ctx) throw new Error("useData must be used within DataProvider");
  return ctx;
}
```
Loading/empty/error states are handled once here, not per‑tab — every tab consumes `status`
and renders a shared `<LoadingState />` / `<ErrorState />` / `<EmptyState />` primitive
(`src/components/ui/AsyncBoundary.tsx`) instead of each tab re‑implementing spinners, mirroring
(and improving on) `dash__1_.py`'s single `try/except FileNotFoundError` at the bottom of the
script.

### Step 5 — Tabs
`src/components/tabs/OverviewTab.tsx`, `CountryDataTab.tsx`, `FlashCardsTab.tsx`,
`InsightsTab.tsx` — structurally as in the original plan's Steps 4–7, consuming
`useData()` instead of props drilling. Two additions vs. the original plan:

- `CountryDataTab.tsx` gains an expandable **KOL panel** and a **Sources footnote** per
  country (per §1.2's new mapping row).
- `FlashCardsTab.tsx`'s card generator must **filter out** cards whose only content is a
  Saudi‑specific string with no global framing — this is now a lint‑able rule, not just a
  code‑review note (see §5 test list).

### Step 6 — App shell (`src/App.tsx`)
Identical to the original plan's Step 8 — tab nav array, `activeTab` state defaulting to
`"overview"`, no hard‑coded country in the header title or subtitle (this replaces
`dash__1_.py`'s `render_hero()` function, which currently prints
`"{country.upper()} — EXECUTIVE MARKET DOSSIER"` for whatever's in the sidebar selectbox —
that per‑country hero banner does not belong in the global Overview tab at all; keep a
per‑country hero only inside the Country Data tab's detail panel).

### Step 7 — Shared UI primitives
`KPICard.tsx`, `CountryMiniBar.tsx` as in the original plan's Step 9, plus `AsyncBoundary.tsx`
from Step 4.

---

## 4. Verification Plan

### Data integrity (build‑time, run in CI before every deploy)
```ts
// src/__tests__/etl.test.ts
import { COUNTRIES } from "../data/countries.generated";

test("exactly 9 countries, no Egypt", () => {
  expect(COUNTRIES.map(c => c.id).sort()).toEqual(
    ["AE", "BH", "IQ", "JO", "KW", "LB", "OM", "QA", "SA"]
  );
});

test("KOLS block-parser assigns every KOL a valid countryId", () => {
  // fails loudly if parseBlockedSheet mis-detects a block boundary
});

test("comp asp rows resolve to >=1 country via region, not by name match", () => {
  // guards against the region-vs-country join mistake flagged in §1.3
});
```

### Rendering / tab content
Same checklist as the original plan's §5 (9 country bars on Overview, sortable/filterable
Country Data table, ≥1 flash card per category, Insights "Source:" label per card) — kept
verbatim, still valid.

### Saudi‑removal audit (unchanged, still correct)
```bash
grep -r "Saudi Arabia" src/components/
grep -r "\"SA\"" src/context/
grep -r "saudi" src/ --include="*.ts" --include="*.tsx" -i
```
Expected: zero hits outside `src/data/*.generated.ts`.

### Accessibility / responsiveness
- Tab nav uses `role="tablist"` / `role="tab"` / `aria-selected`, keyboard arrow‑key
  navigation between tabs (Streamlit's `st.radio` sidebar nav had none of this).
- KPI cards and mini‑bars carry `aria-label` with the full spoken value (`"Total addressable
  market: 16.7 million dollars"`), not just the visual `$16.7M`.
- Country Data table: sortable headers need `aria-sort`; test with keyboard-only nav.
- Responsive breakpoints: 3‑column KPI/mini‑card grids collapse to 1‑column under 640px —
  visually check the Overview and Flash Cards tabs at 375px, 768px, 1280px.

---

## 5. Deployment — Repo Layout

```
amecath-dashboard/
├── data/
│   └── Amecath_Dash.xlsx              # source of truth, committed
├── scripts/etl/
│   ├── parseBlockedSheet.ts
│   ├── parseFlatSheet.ts
│   └── build*.ts                       # one per sheet family
├── src/
│   ├── types/  (country.ts, revenue.ts, insights.ts, kol.ts, source.ts)
│   ├── data/   (countries.generated.ts, aggregations.ts, ...other .generated.ts)
│   ├── context/DataContext.tsx
│   ├── components/
│   │   ├── tabs/ (OverviewTab.tsx, CountryDataTab.tsx, FlashCardsTab.tsx, InsightsTab.tsx)
│   │   └── ui/   (KPICard.tsx, CountryMiniBar.tsx, AsyncBoundary.tsx)
│   ├── App.tsx
│   └── main.tsx
├── package.json   (scripts: "build:data", "dev", "build", "test")
└── README.md      (documents that dash__1_.py is deprecated post-cutover, and why)
```

`dash__1_.py` should be moved to `legacy/` and its README note updated to point at the new
app, rather than deleted outright, in case any stakeholders are still bookmarking the
Streamlit URL during cutover.

---

## Summary of Corrections vs. the Original Plan

| Item | v1 plan | v2 (this doc) |
|---|---|---|
| Sheet count | 9 | **11** (adds `KOLS`, `Sources`) |
| `Distributors`/`COMPETITORS`/`KOLS` parsing | Implied flat "Country column" | **Block‑structured parser required** (`parseBlockedSheet.ts`) |
| `dash__1_.py` relationship | Not addressed | **Confirmed dead‑end schema** — cannot load real xlsx; treated as UX reference only, not a data contract |
| Country list | 9, no Egypt | **Validated** directly against `overview` sheet rows — correct as‑is |
| KOL / Sources data | Absent | New types + tab mapping added |
| Build process | Implicit | Explicit build‑time ETL (`npm run build:data`) replacing Streamlit's runtime `@st.cache_data` |
