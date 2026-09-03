"""
dash.py  ─  AMECATH Market Intelligence Dashboard
═══════════════════════════════════════════════════
Run with:  streamlit run app.py

Pages (sidebar navigation):
  1. 🏠 Overview          – headline KPIs + total market snapshot
  2. 🌍 Country Analysis  – per-country comparison tables & charts
  3. 📈 Revenue Forecast  – 3-scenario revenue & units view
  4. 💲 Pricing Intel     – AMECATH ASP vs competitor ASP
  5. 📋 Tenders           – active tender pipeline by country
  6. 🏆 Hot Areas         – ranked geographic hotspots
  7. 📅 Exhibitions       – conference & congress calendar
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.data_loader import (
    load_overview_kpis,
    load_macro_summary,
    load_forecast,
    load_exec_forecast,
    load_asp,
    load_competitor_aspiration,
    load_tenders,
    load_hot_areas,
    load_exhibitions,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AMECATH Market Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand colours ─────────────────────────────────────────────────────────────
AMECATH_BLUE   = "#1A4A8A"
AMECATH_TEAL   = "#0D9B8A"
AMECATH_ORANGE = "#E87722"
COLOUR_SEQ     = [AMECATH_BLUE, AMECATH_TEAL, AMECATH_ORANGE,
                  "#6C3B8A", "#C0392B", "#16A085", "#F39C12", "#8E44AD", "#2C3E50"]

COUNTRY_COLOURS = {
    c: COLOUR_SEQ[i % len(COLOUR_SEQ)]
    for i, c in enumerate([
        "Saudi Arabia","UAE","Qatar","Kuwait",
        "Oman","Jordan","Lebanon","Iraq","Bahrain"
    ])
}

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.image(
    "https://via.placeholder.com/200x60/1A4A8A/FFFFFF?text=AMECATH",
    use_container_width=True,
)
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio(
    "",
    [
        "🏠 Overview",
        "🌍 Country Analysis",
        "📈 Revenue Forecast",
        "💲 Pricing Intel",
        "📋 Tenders",
        "🏆 Hot Areas",
        "📅 Exhibitions",
    ],
)
st.sidebar.markdown("---")
st.sidebar.caption("Data source: Amecath_Dash.xlsx · © 2026 AMECATH")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.title("🩺 AMECATH — Market Intelligence Dashboard")
    st.markdown(
        "**9-country HD/PD catheter market intelligence** across the GCC & Levant region — 2026 edition."
    )
    st.divider()

    # Load data
    kpi  = load_overview_kpis()
    macro = load_macro_summary()

    # ── KPI row ──────────────────────────────────────────────────────────────
    cols = st.columns(4)
    metrics = [
        ("Total Population", f"{kpi['total_population']:,.0f}",          "9 markets"),
        ("HD Patients 2026",  f"{kpi['hd_patients']:,}",                  "Est."),
        ("Annual Catheter Demand", f"{kpi['annual_catheter_demand']:,}",  "Units/year"),
        ("Market Value",      f"${kpi['market_value_usd_m']:.1f} M",     "USD 2026"),
    ]
    for col, (label, val, delta) in zip(cols, metrics):
        col.metric(label, val, delta)

    cols2 = st.columns(4)
    metrics2 = [
        ("PD Patients 2026",      f"{kpi['pd_patients']:,}",          "Est."),
        ("Dialysis Facilities",   f"{kpi['dialysis_facilities']:,}",   "Centers"),
        ("HD Machines",           f"{kpi['hd_machines']:,}",           "Units"),
        ("Distributors / KOLs",   f"{kpi['distributors']} / {kpi['kols']}", "contacts"),
    ]
    for col, (label, val, delta) in zip(cols2, metrics2):
        col.metric(label, val, delta)

    st.divider()

    # ── Two charts side by side ───────────────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Annual Catheter Demand by Country")
        fig = px.bar(
            macro.sort_values("Annual Catheter Demand", ascending=True),
            x="Annual Catheter Demand",
            y="Country",
            orientation="h",
            color="Country",
            color_discrete_map=COUNTRY_COLOURS,
            labels={"Annual Catheter Demand": "Units"},
            template="plotly_white",
        )
        fig.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Market Value Distribution (USD M)")
        fig2 = px.pie(
            macro,
            values="Market Value",
            names="Country",
            color="Country",
            color_discrete_map=COUNTRY_COLOURS,
            hole=0.45,
            template="plotly_white",
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        fig2.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Summary table ─────────────────────────────────────────────────────────
    st.subheader("Country Macro Summary")
    display_cols = [
        "Country", "Population 2026", "Est. 2026 HD", "Est. 2026 PD",
        "Annual Catheter Demand", "Market Value", "total dialysis facilities",
        "HD Machines", "Annual Growth",
    ]
    disp = macro[[c for c in display_cols if c in macro.columns]].copy()
    disp.rename(columns={
        "Population 2026": "Population",
        "Est. 2026 HD": "HD Patients",
        "Est. 2026 PD": "PD Patients",
        "Annual Catheter Demand": "Catheter Demand",
        "Market Value": "Mkt Value ($M)",
        "total dialysis facilities": "Centers",
        "Annual Growth": "Growth Rate",
    }, inplace=True)
    st.dataframe(disp, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2 — COUNTRY ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🌍 Country Analysis":
    st.title("🌍 Country-Level Analysis")
    macro = load_macro_summary()

    # Country selector
    selected = st.multiselect(
        "Select countries to compare",
        options=sorted(macro["Country"].unique()),
        default=sorted(macro["Country"].unique()),
    )
    if not selected:
        st.warning("Please select at least one country.")
        st.stop()

    filt = macro[macro["Country"].isin(selected)]

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("HD vs PD Patients")
        fig = go.Figure()
        fig.add_bar(name="HD Patients", x=filt["Country"], y=filt["Est. 2026 HD"],
                    marker_color=AMECATH_BLUE)
        fig.add_bar(name="PD Patients", x=filt["Country"], y=filt["Est. 2026 PD"],
                    marker_color=AMECATH_TEAL)
        fig.update_layout(barmode="group", template="plotly_white", height=380,
                          legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Dialysis Facilities & HD Machines")
        fig2 = go.Figure()
        fig2.add_bar(name="Centers", x=filt["Country"],
                     y=filt["total dialysis facilities"], marker_color=AMECATH_ORANGE)
        fig2.add_scatter(name="HD Machines ÷ 10", x=filt["Country"],
                         y=filt["HD Machines"] / 10,
                         mode="markers+lines",
                         marker=dict(size=9, color=AMECATH_BLUE))
        fig2.update_layout(template="plotly_white", height=380,
                           legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Annual Growth Rate by Country")
    fig3 = px.bar(
        filt.sort_values("Annual Growth", ascending=False),
        x="Country", y="Annual Growth",
        color="Country",
        color_discrete_map=COUNTRY_COLOURS,
        text_auto=".1%",
        template="plotly_white",
        labels={"Annual Growth": "Growth Rate"},
    )
    fig3.update_layout(showlegend=False, height=320)
    fig3.update_yaxes(tickformat=".1%")
    st.plotly_chart(fig3, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 3 — REVENUE FORECAST
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📈 Revenue Forecast":
    st.title("📈 Revenue Forecast — 2026‑2028")

    exec_fc = load_exec_forecast()
    country_fc = load_forecast()

    # ── Exec summary cards ───────────────────────────────────────────────────
    st.subheader("Executive Scenario Summary")
    scen_cols = st.columns(3)
    colours = {
        "Conservative": "#6C757D",
        "Base Case":    AMECATH_BLUE,
        "Upside":       AMECATH_TEAL,
    }
    for col, (_, row) in zip(scen_cols, exec_fc.iterrows()):
        with col:
            st.markdown(
                f"<div style='background:{colours.get(row['Scenario'], '#eee')};"
                f"padding:16px;border-radius:10px;color:white'>"
                f"<h4>{row['Scenario']}</h4>"
                f"<p style='font-size:22px;font-weight:bold'>"
                f"${row['3-Year Revenue ($)']:,.0f}</p>"
                f"<p>3-Year Total</p>"
                f"<hr style='border-color:rgba(255,255,255,.4)'>"
                f"<p>2026: ${row['2026 Revenue ($)']:,.0f}</p>"
                f"<p>2027: ${row['2027 Revenue ($)']:,.0f}</p>"
                f"<p>2028: ${row['2028 Revenue ($)']:,.0f}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Revenue trend per scenario ───────────────────────────────────────────
    st.subheader("Revenue Trend by Scenario")
    years = ["2026", "2027", "2028"]
    rev_cols = ["2026 Revenue ($)", "2027 Revenue ($)", "2028 Revenue ($)"]
    fig = go.Figure()
    line_styles = {"Conservative": "dash", "Base Case": "solid", "Upside": "dot"}
    for _, row in exec_fc.iterrows():
        fig.add_scatter(
            x=years,
            y=[row[c] for c in rev_cols],
            name=row["Scenario"],
            mode="lines+markers",
            line=dict(dash=line_styles[row["Scenario"]], width=3),
        )
    fig.update_layout(template="plotly_white", height=380,
                      yaxis_tickprefix="$", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

    # ── Country bottom-up ────────────────────────────────────────────────────
    st.subheader("Base Case — Revenue by Country (2026‑2028)")
    fig2 = go.Figure()
    for yr, col, clr in [
        ("2026", "2026 Revenue ($)", AMECATH_BLUE),
        ("2027", "2027 Revenue ($)", AMECATH_TEAL),
        ("2028", "2028 Revenue ($)", AMECATH_ORANGE),
    ]:
        fig2.add_bar(
            name=yr,
            x=country_fc["Country"],
            y=country_fc[col],
            marker_color=clr,
        )
    fig2.update_layout(barmode="group", template="plotly_white", height=420,
                       yaxis_tickprefix="$", yaxis_tickformat=",",
                       legend=dict(orientation="h", y=1.05))
    st.plotly_chart(fig2, use_container_width=True)

    # ── Underlying table ─────────────────────────────────────────────────────
    with st.expander("📊 Country Bottom-Up Detail Table"):
        show_cols = [
            "Country", "2026 Demand", "2027 Demand", "2028 Demand",
            "Blended ASP", "2026 Share",
            "2026 Revenue ($)", "2027 Revenue ($)", "2028 Revenue ($)",
        ]
        st.dataframe(
            country_fc[[c for c in show_cols if c in country_fc.columns]],
            use_container_width=True,
            hide_index=True,
        )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 4 — PRICING INTELLIGENCE
# ═════════════════════════════════════════════════════════════════════════════
elif page == "💲 Pricing Intel":
    st.title("💲 Pricing Intelligence")

    asp = load_asp()
    comp = load_competitor_aspiration()

    # ── AMECATH ASP table ────────────────────────────────────────────────────
    st.subheader("AMECATH ASP by Country & Product Type (USD)")
    fig = go.Figure()
    for prod, clr in [
        ("Short-Term / STD",        AMECATH_BLUE),
        ("Mid-Term",                AMECATH_TEAL),
        ("Long-Term / Tunneled LTD", AMECATH_ORANGE),
    ]:
        fig.add_bar(name=prod, x=asp["Country"], y=asp[prod], marker_color=clr)
    fig.update_layout(
        barmode="group", template="plotly_white", height=380,
        yaxis_title="USD", legend=dict(orientation="h", y=1.05),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(asp, use_container_width=True, hide_index=True)

    st.divider()

    # ── Competitor ASP ───────────────────────────────────────────────────────
    st.subheader("Competitor ASP vs AMECATH — GCC Region")
    comp_gcc = comp[comp["Region"].str.contains("GCC", na=False)].copy()

    # Build a comparison scatter
    fig2 = go.Figure()
    fig2.add_scatter(
        x=comp_gcc["Company"],
        y=comp_gcc.get(
            "Short-Term HD Catheter Kit ASP (USD)",
            comp_gcc.get("Short-Term HD Catheter Kit ASP (USD)", pd.Series(dtype=float))
        ),
        name="Competitor Short-Term ASP (mid-range)",
        mode="markers",
        marker=dict(size=12, color="#C0392B"),
    )

    # AMECATH KSA short-term ASP reference line
    amecath_std = asp.loc[asp["Country"] == "Saudi Arabia", "Short-Term / STD"].values
    if len(amecath_std):
        fig2.add_hline(
            y=float(amecath_std[0]),
            line_dash="dash",
            line_color=AMECATH_BLUE,
            annotation_text=f"AMECATH STD KSA: ${amecath_std[0]}",
        )
    fig2.update_layout(template="plotly_white", height=360,
                       yaxis_title="ASP (USD)", xaxis_title="Competitor")
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📋 Full Competitor ASP Table"):
        st.dataframe(comp, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 5 — TENDERS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📋 Tenders":
    st.title("📋 Tender Pipeline")

    tenders = load_tenders()

    # Filter
    countries_t = sorted(tenders["Country"].dropna().unique())
    sel_country = st.multiselect(
        "Filter by country", countries_t, default=countries_t
    )
    filt_t = tenders[tenders["Country"].isin(sel_country)]

    st.metric("Active Tender Records", len(filt_t))
    st.divider()

    # Count per country bar
    counts = filt_t["Country"].value_counts().reset_index()
    counts.columns = ["Country", "Count"]
    fig = px.bar(
        counts, x="Country", y="Count",
        color="Country", color_discrete_map=COUNTRY_COLOURS,
        template="plotly_white",
        title="Tender Count by Country",
    )
    fig.update_layout(showlegend=False, height=320)
    st.plotly_chart(fig, use_container_width=True)

    # Table
    show_cols_t = [
        "Country", "Tender Title (Short)", "Issuing Entity",
        "Published", "Closing Date", "Tender Value (USD)", "Link",
    ]
    st.dataframe(
        filt_t[[c for c in show_cols_t if c in filt_t.columns]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Link": st.column_config.LinkColumn("Link", display_text="Open 🔗")
        },
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 6 — HOT AREAS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Hot Areas":
    st.title("🏆 Geographic Hot Areas")
    st.markdown("Top-ranked dialysis hubs per country.")

    hot = load_hot_areas()
    countries_h = sorted(hot["Country"].unique())
    sel_h = st.selectbox("Select Country", countries_h)

    filt_h = hot[hot["Country"] == sel_h].sort_values("Rank")
    st.subheader(f"Hot Areas — {sel_h}")
    for _, row in filt_h.iterrows():
        area_text = str(row["Area"])
        # Clean up citations like [Expert Judgment]
        area_clean = area_text.split("[")[0].split("(")[0].strip()
        st.markdown(f"**#{row['Rank']}** — {area_clean}")

    st.divider()
    st.subheader("Number of Ranked Areas per Country")
    area_counts = hot.groupby("Country").size().reset_index(name="Ranked Areas")
    fig = px.bar(
        area_counts.sort_values("Ranked Areas", ascending=False),
        x="Country", y="Ranked Areas",
        color="Country", color_discrete_map=COUNTRY_COLOURS,
        template="plotly_white",
    )
    fig.update_layout(showlegend=False, height=340)
    st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 7 — EXHIBITIONS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📅 Exhibitions":
    st.title("📅 Medical Exhibitions & Congresses")
    exh = load_exhibitions()

    search = st.text_input("🔍 Search by event name, city, or focus area")
    if search:
        mask = exh.apply(
            lambda r: search.lower() in str(r).lower(), axis=1
        )
        exh = exh[mask]

    show_cols_e = [
        "Event Name", "Dates", "City / Country",
        "Focus Area", "Target Audience", "Official Website",
    ]
    st.dataframe(
        exh[[c for c in show_cols_e if c in exh.columns]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Official Website": st.column_config.LinkColumn(
                "Website", display_text="Visit 🔗"
            )
        },
    )
    st.caption(f"Showing {len(exh)} events.")
