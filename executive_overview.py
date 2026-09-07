"""Executive Overview page foundation."""

import streamlit as st

from components.executive import render_executive_banner, render_source_badge
from utils.pricing import calculate_fair_price


def render(data: dict) -> None:
    macro = data["macro"]
    competitors = data["competitors"]
    tenders = data["tenders"]
    pricing = data["pricing"]

    total_tam = macro["market_value_usd_m"].sum()
    total_hd = macro["hd_patients_2026"].sum()
    total_demand = macro["annual_catheter_demand"].sum()
    critical_tenders = (tenders["priority"] == "Critical").sum()

    top_market = macro.sort_values("market_value_usd_m", ascending=False).iloc[0]
    fastest_market = macro.sort_values("annual_growth", ascending=False).iloc[0]

    render_executive_banner(
        "CEO Decision Summary",
        [
            f"{top_market['country']} is the largest market in the current seed dataset at ${top_market['market_value_usd_m']:.2f}M TAM.",
            f"{fastest_market['country']} has the highest annual growth assumption at {fastest_market['annual_growth']:.1%}.",
            f"{critical_tenders} critical tender opportunities are currently represented in the pipeline.",
        ],
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Regional TAM", f"${total_tam:.2f}M")
    c2.metric("HD Patients", f"{total_hd:,.0f}")
    c3.metric("Annual Catheter Demand", f"{total_demand:,.0f}")
    c4.metric("Critical Tenders", f"{critical_tenders}")

    st.subheader("Market Priority Snapshot")
    snapshot = macro[[
        "country", "market_value_usd_m", "hd_patients_2026",
        "annual_catheter_demand", "annual_growth"
    ]].copy()
    snapshot["annual_growth"] = snapshot["annual_growth"].map(lambda x: f"{x:.1%}")
    snapshot = snapshot.sort_values("market_value_usd_m", ascending=False)
    st.dataframe(snapshot, use_container_width=True, hide_index=True)

    st.subheader("Pricing Normalization — Fair Hospital Price")
    ame = pricing[
        (pricing["company"] == "AMECATH") &
        (pricing["product_type"] == "Tunneled")
    ].iloc[0]
    competitor = pricing[
        (pricing["company"] != "AMECATH") &
        (pricing["product_type"] == "Tunneled")
    ].iloc[0]

    margin_pct = st.slider(
        "Distributor → hospital normalization margin",
        min_value=20,
        max_value=60,
        value=35,
        step=5,
        format="%d%%",
    )
    fair_price = calculate_fair_price(ame["asp_usd"], margin_pct / 100)

    p1, p2, p3 = st.columns(3)
    p1.metric("AMECATH Distributor ASP", f"${ame['asp_usd']:.2f}")
    p2.metric("Estimated Hospital ASP", f"${fair_price:.2f}")
    p3.metric(
        "Competitor Hospital ASP",
        f"${competitor['asp_usd']:.2f}",
    )

    render_source_badge(
        "AMECATH workbook / pricing benchmark",
        "Internal source — replace with validated source URL",
        "AMECATH price is distributor ex-factory. Competitor benchmark is hospital/end-user. "
        "Fair hospital estimate = AMECATH distributor price × (1 + selected margin).",
    )
