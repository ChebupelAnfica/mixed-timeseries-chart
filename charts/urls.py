from django.urls import path

from charts import views

urlpatterns = [
    path("", views.chart_page, name="chart-page"),
    path("api/chart/", views.chart_api, name="chart-api"),
    path("api/chart/build/", views.chart_from_payload, name="chart-build"),
]
