"""Reusable Executive Decision Engine UI components."""

from __future__ import annotations

import html
from typing import Sequence

import streamlit as st

from config import THEME


def inject_theme_css() -> None:
    """Inject the enterprise dark executive theme once per page."""
    st.markdown(
        f"""
        <style>
        :root {{
            --amecath-bg: {THEME.background};
            --amecath-card: {THEME.card};
            --amecath-gold: {THEME.gold};
            --amecath-blue: {THEME.blue};
            --amecath-text: {THEME.text};
            --amecath-muted: {THEME.muted};
            --amecath-border: {THEME.border};
        }}

        .stApp {{
            background: var(--amecath-bg);
            color: var(--amecath-text);
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}

        .amecath-brand {{
            color: var(--amecath-gold);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }}

        .amecath-page-title {{
            color: var(--amecath-text);
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.35rem;
        }}

        .amecath-subtitle {{
            color: var(--amecath-muted);
            font-size: 0.95rem;
            margin-bottom: 1.4rem;
        }}

        .executive-banner {{
            background: linear-gradient(135deg, #0e2343 0%, #13274c 100%);
            border: 1px solid rgba(245,158,11,.45);
            border-left: 5px solid var(--amecath-gold);
            border-radius: 14px;
            padding: 1.1rem 1.25rem;
            margin: 0 0 1.25rem 0;
            box-shadow: 0 12px 30px rgba(0,0,0,.22);
        }}

        .executive-banner h3 {{
            margin: 0 0 .65rem 0;
            color: #ffffff;
            font-size: 1rem;
            font-weight: 800;
        }}

        .executive-banner ul {{
            margin: 0;
            padding-left: 1.15rem;
        }}

        .executive-banner li {{
            color: var(--amecath-text);
            margin: .32rem 0;
            font-size: .9rem;
            line-height: 1.45;
        }}

        .source-badge {{
            display: inline-flex;
            align-items: center;
            gap: .4rem;
            padding: .28rem .55rem;
            border-radius: 999px;
            background: rgba(59,130,246,.10);
            border: 1px solid rgba(59,130,246,.35);
            color: #bfdbfe;
            font-size: .72rem;
            font-weight: 700;
        }}

        .source-dot {{
            width: .42rem;
            height: .42rem;
            border-radius: 50%;
            background: var(--amecath-blue);
            display: inline-block;
        }}

        .decision-card {{
            background: var(--amecath-card);
            border: 1px solid var(--amecath-border);
            border-radius: 14px;
            padding: 1rem;
            min-height: 115px;
        }}

        .decision-label {{
            color: var(--amecath-muted);
            font-size: .72rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            font-weight: 800;
        }}

        .decision-value {{
            color: #ffffff;
            font-size: 1.55rem;
            font-weight: 850;
            margin-top: .35rem;
        }}

        .decision-note {{
            color: #93c5fd;
            font-size: .78rem;
            margin-top: .3rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_executive_banner(title: str, points: list[str]) -> None:
    """Render a reusable CEO-level strategic decision banner."""
    safe_title = html.escape(str(title))
    safe_points = [html.escape(str(p)) for p in list(points)[:3]]

    bullets = "".join(f"<li>{point}</li>" for point in safe_points)
    st.markdown(
        f"""
        <section class="executive-banner" aria-label="Executive decision summary">
            <h3>{safe_title}</h3>
            <ul>{bullets}</ul>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_source_badge(
    source_name: str,
    url: str,
    calculation_note: str | None = None,
) -> None:
    """Render a compact verifiable source badge with optional methodology expander."""
    safe_name = html.escape(str(source_name))
    safe_url = html.escape(str(url), quote=True)

    st.markdown(
        f"""
        <span class="source-badge">
            <span class="source-dot"></span>
            Source: {safe_name}
        </span>
        """,
        unsafe_allow_html=True,
    )

    if calculation_note:
        with st.expander("Methodology / calculation"):
            st.write(calculation_note)
            st.caption(f"Reference: {safe_url}")
    else:
        st.caption(f"Reference: {url}")
