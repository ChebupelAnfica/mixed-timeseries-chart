(function () {
  function formatValue(value) {
    if (value == null || Number.isNaN(value)) return "—";
    if (Number.isInteger(value)) return String(value);
    return Number(value).toFixed(2);
  }

  function mountChart(containerId, options) {
    const meta = (options.tooltip && options.tooltip.mtsMeta) || {};
    const categories = meta.categories || [];
    const tooltipOrder = meta.tooltipOrder || ["area", "bar", "spline", "line"];
    const names = meta.names || {};
    const colors = meta.colors || {};

    const chartOptions = Object.assign({}, options, {
      tooltip: Object.assign({}, options.tooltip, {
        headerFormat: "",
        formatter: function () {
          const points = this.points || [];
          const byName = new Map(points.map((p) => [p.series.name, p]));
          const header = categories[this.x] || String(this.x);

          const rows = tooltipOrder
            .map((kind) => {
              const name = names[kind];
              const point = byName.get(name);
              if (!point) return "";
              const color = colors[kind] || "#999";
              return (
                '<div class="mts-tip-row">' +
                '<span class="mts-tip-dot" style="background:' +
                color +
                '"></span>' +
                '<span class="mts-tip-label">' +
                name +
                ":</span>" +
                '<span class="mts-tip-value">' +
                formatValue(point.y) +
                "</span>" +
                "</div>"
              );
            })
            .join("");

          return (
            '<div class="mts-tip"><div class="mts-tip-date">' +
            header +
            "</div>" +
            rows +
            "</div>"
          );
        },
      }),
    });

    // Highcharts does not need our helper metadata
    if (chartOptions.tooltip) {
      delete chartOptions.tooltip.mtsMeta;
    }

    return Highcharts.chart(containerId, chartOptions);
  }

  document.addEventListener("DOMContentLoaded", function () {
    const node = document.getElementById("chart-options");
    if (!node) return;
    const options = JSON.parse(node.textContent);
    mountChart("chart", options);
  });

  window.mountMixedChart = mountChart;
})();
