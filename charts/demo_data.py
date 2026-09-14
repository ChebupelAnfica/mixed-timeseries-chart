"""Demo dataset reconstructed from the reference GIF trajectories."""

from charts.mixed_chart import create_mixed_chart

DEMO_DATES = [
    "2026-06-08",
    "2026-06-09",
    "2026-06-10",
    "2026-06-11",
    "2026-06-12",
    "2026-06-13",
    "2026-06-14",
]

DEMO_SERIES = {
    "area": {
        "name": "Cost",
        "data": [4.2, 6.8, 2.04, 25.85, 44.36, 55.65, 61.2],
    },
    "spline": {
        "name": "ROI confirmed",
        "data": [210.4, 198.2, 192.0, 180.5, 161.47, 56.33, 72.1],
    },
    "line": {
        "name": "Conversions",
        "data": [10, 16, 22, 30, 36, 70, 78],
    },
    "bar": {
        "name": "CPA",
        "data": [0.92, 1.05, 0.88, 0.86, 1.23, 0.79, 0.84],
    },
}


def build_demo_chart_options() -> dict:
    return create_mixed_chart(DEMO_DATES, **DEMO_SERIES)
