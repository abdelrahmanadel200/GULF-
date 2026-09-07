"""Centralized structured data layer.

These DataFrames are intentionally small seed datasets. Replace/extend them with
validated workbook/API extracts without changing downstream page components.
"""

from __future__ import annotations

import pandas as pd


MACRO_MARKETS = pd.DataFrame(
    [
        ["Saudi Arabia", "SA", 35_165_787, 30_000, 360, 77_530, 9.30, 0.09],
        ["UAE", "AE", 11_574_682, 3_000, 60, 7_638, 0.99, 0.08],
        ["Qatar", "QA", 3_173_559, 1_200, 18, 3_207, 0.42, 0.056],
        ["Kuwait", "KW", 5_102_773, 2_156, 25, 5_728, 0.72, 0.06],
        ["Oman", "OM", 5_494_691, 2_500, 20, 6_365, 0.76, 0.07],
        ["Jordan", "JO", 11_589_532, 6_400, 50, 16_127, 1.61, 0.05],
        ["Lebanon", "LB", 5_897_467, 4_730, 85, 12_067, 1.21, 0.03],
        ["Iraq", "IQ", 48_007_437, 10_721, 130, 27_320, 2.46, 0.05],
        ["Bahrain", "BH", 1_675_572, 4_547, 14, 11_885, 1.43, 0.05],
    ],
    columns=[
        "country", "iso", "population_2026", "hd_patients_2026",
        "dialysis_facilities", "annual_catheter_demand",
        "market_value_usd_m", "annual_growth",
    ],
)


COMPETITOR_PROFILES = pd.DataFrame(
    [
        ["Saudi Arabia", "Fresenius Medical Care", 19.0, "Nationwide", "Bundled ecosystem", "Dialysis ecosystem"],
        ["Saudi Arabia", "B. Braun", 13.0, "Nationwide", "Diversified portfolio", "HD catheters / vascular access"],
        ["Saudi Arabia", "Medtronic", 11.0, "Nationwide", "Premium pricing", "HD / PD catheters"],
        ["UAE", "BD", 18.0, "Major private / tertiary", "Premium positioning", "Vascular access"],
        ["UAE", "Teleflex", 14.0, "Tertiary hospitals", "Premium pricing", "Vascular access"],
        ["Qatar", "BD", 20.0, "HMC / tertiary", "Premium positioning", "Vascular access"],
    ],
    columns=["country", "competitor", "market_share_pct", "coverage", "key_gap", "specialty"],
)


ACTIVE_TENDERS = pd.DataFrame(
    [
        ["Saudi Arabia", "NUPCO", "Medical Supplies – Jazan Health Cluster", "Open", "$100K–$400K", "High"],
        ["UAE", "DAHC", "Medical Consumables – AJCH Blanket", "Active", "$1M–$3M/year", "Critical"],
        ["Iraq", "Kimadia / MOH", "CVC & Other Catheters", "Active", "$500K–$2M/year", "Critical"],
        ["Kuwait", "MOH Kuwait", "Dialysis Consumables & Equipment", "Active", "$400K–$1.2M/year", "High"],
        ["Jordan", "MOH Jordan", "Dialysis Machines – Yarmouk Hospital", "Open", "$300K–$700K", "High"],
    ],
    columns=["country", "authority", "tender", "status", "estimated_value", "priority"],
)


CATHETER_PRICING_BENCHMARKS = pd.DataFrame(
    [
        ["Saudi Arabia", "AMECATH", "Distributor Ex-Factory", "STD", 19.0],
        ["Saudi Arabia", "AMECATH", "Distributor Ex-Factory", "Mid", 25.0],
        ["Saudi Arabia", "AMECATH", "Distributor Ex-Factory", "Tunneled", 85.0],
        ["Saudi Arabia", "BD", "Hospital / End-User", "STD", 110.0],
        ["Saudi Arabia", "BD", "Hospital / End-User", "Tunneled", 220.0],
        ["UAE", "AMECATH", "Distributor Ex-Factory", "STD", 20.0],
        ["UAE", "AMECATH", "Distributor Ex-Factory", "Mid", 27.0],
        ["UAE", "AMECATH", "Distributor Ex-Factory", "Tunneled", 90.0],
        ["UAE", "BD", "Hospital / End-User", "STD", 120.0],
        ["UAE", "BD", "Hospital / End-User", "Tunneled", 240.0],
    ],
    columns=["country", "company", "price_basis", "product_type", "asp_usd"],
)


DIALYSIS_CENTER_DENSITIES = pd.DataFrame(
    [
        ["Saudi Arabia", "Riyadh", 39, "High"],
        ["Saudi Arabia", "Jeddah", 12, "High"],
        ["Saudi Arabia", "Makkah", 12, "High"],
        ["UAE", "Dubai", 7, "High"],
        ["UAE", "Abu Dhabi", 5, "High"],
        ["Qatar", "Doha", 10, "High"],
        ["Kuwait", "Kuwait City", 8, "High"],
        ["Oman", "Muscat", 4, "Medium"],
        ["Jordan", "Amman", 5, "High"],
        ["Lebanon", "Greater Beirut", 20, "High"],
        ["Iraq", "Baghdad", 11, "High"],
        ["Bahrain", "Manama / Riffa", 6, "High"],
    ],
    columns=["country", "area", "center_count", "density_band"],
)
