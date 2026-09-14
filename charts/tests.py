from django.test import Client, SimpleTestCase, TestCase

from charts.mixed_chart import MixedChartData, create_mixed_chart


class MixedChartApiTests(SimpleTestCase):
    def test_create_mixed_chart_builds_four_series(self):
        options = create_mixed_chart(
            dates=["2026-06-11", "2026-06-12", "2026-06-13"],
            area={"name": "Cost", "data": [25.85, 44.36, 55.65]},
            spline={"name": "ROI confirmed", "data": [180.5, 161.47, 56.33]},
            line={"name": "Conversions", "data": [30, 36, 70]},
            bar={"name": "CPA", "data": [0.86, 1.23, 0.79]},
        )

        types = [series["type"] for series in options["series"]]
        self.assertEqual(types, ["area", "column", "spline", "line"])
        self.assertEqual(options["xAxis"]["categories"][0], "11.06.2026")

    def test_mismatched_lengths_raise(self):
        with self.assertRaises(ValueError):
            MixedChartData.from_dict(
                {
                    "dates": ["2026-06-11", "2026-06-12"],
                    "series": {
                        "area": {"name": "Cost", "data": [1]},
                        "spline": {"name": "ROI", "data": [1, 2]},
                        "line": {"name": "Conv", "data": [1, 2]},
                        "bar": {"name": "CPA", "data": [1, 2]},
                    },
                }
            )


class ChartViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_page_ok(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="chart"')

    def test_api_ok(self):
        response = self.client.get("/api/chart/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["series"]), 4)

    def test_build_endpoint(self):
        response = self.client.post(
            "/api/chart/build/",
            data={
                "dates": ["2026-06-11", "2026-06-12"],
                "series": {
                    "area": {"name": "Cost", "data": [10, 20]},
                    "spline": {"name": "ROI confirmed", "data": [100, 90]},
                    "line": {"name": "Conversions", "data": [5, 8]},
                    "bar": {"name": "CPA", "data": [1.1, 0.9]},
                },
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["series"][0]["data"], [10.0, 20.0])
