from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Mapping, Sequence


SERIES_KINDS = ("area", "spline", "line", "bar")

DEFAULT_COLORS: dict[str, str] = {
    "area": "#F5E19A",
    "spline": "#1F800E",
    "line": "#B010E8",
    "bar": "#3870FE",
}


@dataclass(frozen=True, slots=True)
class SeriesInput:
    name: str
    data: tuple[float, ...]
    color: str | None = None

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> SeriesInput:
        if "name" not in payload or "data" not in payload:
            raise ValueError("Each series requires 'name' and 'data'")
        data = tuple(float(v) for v in payload["data"])
        color = payload.get("color")
        return cls(name=str(payload["name"]), data=data, color=str(color) if color else None)


@dataclass(frozen=True, slots=True)
class MixedChartData:
    """Four aligned time-series sequences for the mixed chart."""

    dates: tuple[str, ...]
    area: SeriesInput
    spline: SeriesInput
    line: SeriesInput
    bar: SeriesInput
    height: int = 320
    bar_axis_padding: float = 8.0

    def __post_init__(self) -> None:
        expected = len(self.dates)
        if expected == 0:
            raise ValueError("dates must not be empty")
        for kind in SERIES_KINDS:
            series: SeriesInput = getattr(self, kind)
            if len(series.data) != expected:
                raise ValueError(
                    f"series.{kind}.data length ({len(series.data)}) "
                    f"must equal dates length ({expected})"
                )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> MixedChartData:
        series = payload.get("series") or {}
        missing = [kind for kind in SERIES_KINDS if kind not in series]
        if missing:
            raise ValueError(f"Missing series keys: {', '.join(missing)}")

        dates = tuple(_normalize_date(d) for d in payload["dates"])
        return cls(
            dates=dates,
            area=SeriesInput.from_mapping(series["area"]),
            spline=SeriesInput.from_mapping(series["spline"]),
            line=SeriesInput.from_mapping(series["line"]),
            bar=SeriesInput.from_mapping(series["bar"]),
            height=int(payload.get("height", 320)),
            bar_axis_padding=float(payload.get("bar_axis_padding", 8)),
        )

    def color(self, kind: str) -> str:
        series: SeriesInput = getattr(self, kind)
        return series.color or DEFAULT_COLORS[kind]

    def categories(self) -> list[str]:
        return [_format_tooltip_date(d) for d in self.dates]


def _normalize_date(value: str | date | datetime) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    # Accept already-ISO or DD.MM.YYYY
    if len(text) == 10 and text[2] == "." and text[5] == ".":
        dd, mm, yyyy = text.split(".")
        return f"{yyyy}-{mm}-{dd}"
    # Validate ISO-like
    datetime.fromisoformat(text)
    return text


def _format_tooltip_date(raw: str) -> str:
    parsed = datetime.fromisoformat(raw).date()
    return parsed.strftime("%d.%m.%Y")


def _brighten_hex(hex_color: str, amount: float = -0.08) -> str:
    color = hex_color.lstrip("#")
    if len(color) != 6:
        return hex_color
    rgb = [int(color[i : i + 2], 16) for i in (0, 2, 4)]
    if amount < 0:
        factor = 1 + amount
        rgb = [max(0, min(255, int(c * factor))) for c in rgb]
    else:
        rgb = [max(0, min(255, int(c + (255 - c) * amount))) for c in rgb]
    return "#" + "".join(f"{c:02x}" for c in rgb)


def build_highcharts_options(data: MixedChartData) -> dict[str, Any]:
    """
    Build a Highcharts options object from four sequences.

    The frontend only mounts Highcharts with this payload — all series
    wiring and validation happens in Python.
    """
    categories = data.categories()
    bar_max = max(data.bar.data + (0.0001,)) * data.bar_axis_padding
    colors = {kind: data.color(kind) for kind in SERIES_KINDS}

    return {
        "chart": {
            "backgroundColor": "transparent",
            "height": data.height,
            "spacing": [12, 12, 8, 12],
            "style": {
                "fontFamily": (
                    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, '
                    "Helvetica, Arial, sans-serif"
                ),
                "cursor": "pointer",
            },
        },
        "title": {"text": None},
        "credits": {"enabled": False},
        "legend": {"enabled": False},
        "xAxis": {
            "categories": categories,
            "lineWidth": 0,
            "tickLength": 0,
            "labels": {"enabled": False},
            "crosshair": {"width": 1, "color": "rgba(0,0,0,0.06)"},
        },
        "yAxis": [
            {
                "title": {"text": None},
                "gridLineWidth": 0,
                "gridLineColor": "transparent",
                "lineWidth": 0,
                "tickLength": 0,
                "labels": {"enabled": False},
                "softMin": 0,
            },
            {
                "title": {"text": None},
                "gridLineWidth": 0,
                "gridLineColor": "transparent",
                "lineWidth": 0,
                "tickLength": 0,
                "labels": {"enabled": False},
                "softMin": 0,
                "max": bar_max,
                "opposite": False,
                "visible": False,
            },
        ],
        "tooltip": {
            "shared": True,
            "useHTML": True,
            "backgroundColor": "#ffffff",
            "borderColor": "rgba(0,0,0,0.08)",
            "borderRadius": 8,
            "borderWidth": 1,
            "shadow": {
                "color": "rgba(0,0,0,0.18)",
                "offsetX": 0,
                "offsetY": 4,
                "opacity": 1,
                "width": 12,
            },
            "padding": 12,
            "style": {"fontSize": "13px", "color": "#2a2a2a"},
            # Custom formatter lives in static JS; we pass metadata here.
            "mtsMeta": {
                "categories": categories,
                "tooltipOrder": ["area", "bar", "spline", "line"],
                "names": {
                    "area": data.area.name,
                    "bar": data.bar.name,
                    "spline": data.spline.name,
                    "line": data.line.name,
                },
                "colors": colors,
            },
        },
        "plotOptions": {
            "series": {
                "animation": {"duration": 450},
                "states": {
                    "hover": {"enabled": True, "lineWidthPlus": 0},
                    "inactive": {"opacity": 1},
                },
            },
            "area": {
                "fillOpacity": 0.95,
                "lineWidth": 1,
                "marker": {
                    "enabled": False,
                    "symbol": "circle",
                    "radius": 4,
                    "fillColor": "#ffffff",
                    "lineWidth": 2,
                    "states": {"hover": {"enabled": True, "radius": 5}},
                },
                "states": {"hover": {"halo": {"size": 10, "opacity": 0.25}}},
            },
            "spline": {
                "lineWidth": 2.25,
                "marker": {
                    "enabled": False,
                    "symbol": "circle",
                    "radius": 4,
                    "fillColor": "#ffffff",
                    "lineWidth": 2,
                    "states": {"hover": {"enabled": True, "radius": 5}},
                },
                "states": {"hover": {"halo": {"size": 14, "opacity": 0.22}}},
            },
            "line": {
                "lineWidth": 2,
                "marker": {
                    "enabled": True,
                    "symbol": "square",
                    "radius": 4,
                    "lineWidth": 0,
                    "states": {
                        "hover": {
                            "enabled": True,
                            "radius": 5,
                            "lineWidth": 2,
                            "fillColor": "#ffffff",
                        }
                    },
                },
                "states": {"hover": {"halo": {"size": 14, "opacity": 0.22}}},
            },
            "column": {
                "borderWidth": 0,
                "borderRadius": 3,
                "pointPadding": 0.28,
                "groupPadding": 0.12,
                "states": {
                    "hover": {"brightness": 0.05, "halo": {"size": 0}},
                },
            },
        },
        "series": [
            {
                "type": "area",
                "name": data.area.name,
                "data": list(data.area.data),
                "color": colors["area"],
                "fillColor": colors["area"],
                "lineColor": _brighten_hex(colors["area"], -0.08),
                "yAxis": 0,
                "zIndex": 1,
                "marker": {"lineColor": colors["area"]},
            },
            {
                "type": "column",
                "name": data.bar.name,
                "data": list(data.bar.data),
                "color": colors["bar"],
                "yAxis": 1,
                "zIndex": 2,
            },
            {
                "type": "spline",
                "name": data.spline.name,
                "data": list(data.spline.data),
                "color": colors["spline"],
                "yAxis": 0,
                "zIndex": 3,
                "marker": {"lineColor": colors["spline"]},
            },
            {
                "type": "line",
                "name": data.line.name,
                "data": list(data.line.data),
                "color": colors["line"],
                "yAxis": 0,
                "zIndex": 4,
                "marker": {
                    "fillColor": colors["line"],
                    "lineColor": colors["line"],
                },
            },
        ],
    }


def create_mixed_chart(
    dates: Sequence[str | date | datetime],
    *,
    area: Mapping[str, Any],
    spline: Mapping[str, Any],
    line: Mapping[str, Any],
    bar: Mapping[str, Any],
    height: int = 320,
    bar_axis_padding: float = 8.0,
) -> dict[str, Any]:
    """
    Public Python API: pass four sequences and get Highcharts options.

    Example:
        options = create_mixed_chart(
            dates=["2026-06-11", "2026-06-12"],
            area={"name": "Cost", "data": [25.85, 44.36]},
            spline={"name": "ROI confirmed", "data": [180.5, 161.47]},
            line={"name": "Conversions", "data": [30, 36]},
            bar={"name": "CPA", "data": [0.86, 1.23]},
        )
    """
    data = MixedChartData.from_dict(
        {
            "dates": list(dates),
            "series": {
                "area": area,
                "spline": spline,
                "line": line,
                "bar": bar,
            },
            "height": height,
            "bar_axis_padding": bar_axis_padding,
        }
    )
    return build_highcharts_options(data)
