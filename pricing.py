"""Pricing Engine page."""

import streamlit as st

from components.executive import render_executive_banner, render_source_badge
from utils.pricing import calculate_fair_price


def render(data: dict) -> None:
    pricing = data["pricing"]

    render_executive_banner(
        "Pricing Decision",
        [
            "Do not compare AMECATH distributor ex-factory prices directly with competitor hospital prices.",
            "Normalize AMECATH prices using the selected downstream margin before judging price competitiveness.",
        ],
    )

    margin = st.slider(
        "Hospital margin assumption",
        min_value=20,
        max_value=60,
        value=35,
        step=5,
        format="%d%%",
    )

    rows = []
    for _, row in pricing[pricing["company"] == "AMECATH"].iterrows():
        fair = calculate_fair_price(row["asp_usd"], margin / 100)
        rows.append({
            "Country": row["country"],
            "Product": row["product_type"],
            "AMECATH Distributor ASP": row["asp_usd"],
            "Estimated Hospital ASP": fair,
        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
        column_config={
            "AMECATH Distributor ASP": st.column_config.NumberColumn(format="$%.2f"),
            "Estimated Hospital ASP": st.column_config.NumberColumn(format="$%.2f"),
        },
    )

    render_source_badge(
        "Pricing methodology",
        "Internal calculation",
        "Estimated Hospital Price = Distributor Price × (1 + margin_pct). "
        "Allowed dynamic margin range: 20%–60%; default: 35%.",
    )
