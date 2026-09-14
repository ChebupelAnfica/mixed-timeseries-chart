import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from charts.demo_data import build_demo_chart_options
from charts.mixed_chart import MixedChartData, build_highcharts_options


@require_GET
def chart_page(request):
    """Render the demo page; chart options are built in Python."""
    return render(
        request,
        "charts/index.html",
        {
            "chart_options": build_demo_chart_options(),
        },
    )


@require_GET
def chart_api(request):
    """JSON endpoint with the demo four-series payload."""
    return JsonResponse(build_demo_chart_options())


@csrf_exempt
@require_http_methods(["POST"])
def chart_from_payload(request):
    """
    Build chart options from a JSON body with four sequences.

    POST /api/chart/build/
    {
      "dates": ["2026-06-11", "2026-06-12"],
      "series": {
        "area":   {"name": "Cost", "data": [25.85, 44.36]},
        "spline": {"name": "ROI confirmed", "data": [180.5, 161.47]},
        "line":   {"name": "Conversions", "data": [30, 36]},
        "bar":    {"name": "CPA", "data": [0.86, 1.23]}
      }
    }
    """
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
        data = MixedChartData.from_dict(payload)
        return JsonResponse(build_highcharts_options(data))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return JsonResponse({"error": str(exc)}, status=400)
