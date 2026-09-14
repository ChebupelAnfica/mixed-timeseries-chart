import Highcharts from 'highcharts'
import {
  DEFAULT_COLORS,
  type MixedChartOptions,
  type MixedChartSeries,
  type SeriesInput,
  type SeriesKind,
} from './types'

function assertAligned(options: MixedChartOptions): void {
  const { dates, series } = options
  const kinds: SeriesKind[] = ['area', 'spline', 'line', 'bar']
  for (const kind of kinds) {
    const len = series[kind].data.length
    if (len !== dates.length) {
      throw new Error(
        `series.${kind}.data length (${len}) must equal dates length (${dates.length})`,
      )
    }
  }
}

function formatTooltipDate(raw: string | number): string {
  const d = new Date(raw)
  if (Number.isNaN(d.getTime())) return String(raw)
  const dd = String(d.getDate()).padStart(2, '0')
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const yyyy = d.getFullYear()
  return `${dd}.${mm}.${yyyy}`
}

function formatValue(value: number | null | undefined): string {
  if (value == null || Number.isNaN(value)) return '—'
  if (Number.isInteger(value)) return String(value)
  return value.toFixed(2)
}

/**
 * Creates a mixed time-series chart (area + spline + line + bar)
 * styled after the reference dashboard chart.
 *
 * @returns Highcharts.Chart instance — call `chart.destroy()` to tear down.
 */
export function createMixedChart(
  container: string | HTMLElement,
  options: MixedChartOptions,
): Highcharts.Chart {
  assertAligned(options)

  const {
    dates,
    series,
    height = 320,
    barAxisPadding = 8,
  } = options

  const categories = dates.map((d) => formatTooltipDate(d))
  const barMax = Math.max(...series.bar.data, 0.0001) * barAxisPadding

  const color = (kind: SeriesKind) =>
    series[kind].color ?? DEFAULT_COLORS[kind]

  // Tooltip row order matches the reference: Cost, CPA, ROI, Conversions
  const tooltipOrder: SeriesKind[] = ['area', 'bar', 'spline', 'line']

  return Highcharts.chart(container, {
    chart: {
      backgroundColor: 'transparent',
      height,
      spacing: [12, 12, 8, 12],
      style: {
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
        cursor: 'pointer',
      },
    },
    title: { text: undefined },
    credits: { enabled: false },
    legend: { enabled: false },
    xAxis: {
      categories,
      lineWidth: 0,
      tickLength: 0,
      labels: { enabled: false },
      crosshair: {
        width: 1,
        color: 'rgba(0,0,0,0.06)',
      },
    },
    yAxis: [
      {
        title: { text: undefined },
        gridLineWidth: 0,
        gridLineColor: 'transparent',
        lineWidth: 0,
        tickLength: 0,
        labels: { enabled: false },
        softMin: 0,
      },
      {
        title: { text: undefined },
        gridLineWidth: 0,
        gridLineColor: 'transparent',
        lineWidth: 0,
        tickLength: 0,
        labels: { enabled: false },
        softMin: 0,
        max: barMax,
        opposite: false,
        visible: false,
      },
    ],
    tooltip: {
      shared: true,
      useHTML: true,
      backgroundColor: '#ffffff',
      borderColor: 'rgba(0,0,0,0.08)',
      borderRadius: 8,
      borderWidth: 1,
      shadow: {
        color: 'rgba(0,0,0,0.18)',
        offsetX: 0,
        offsetY: 4,
        opacity: 1,
        width: 12,
      },
      padding: 12,
      style: {
        fontSize: '13px',
        color: '#2a2a2a',
      },
      headerFormat: '',
      formatter: function () {
        const points = this.points ?? []
        const byName = new Map(points.map((p) => [p.series.name, p]))
        const header = categories[this.x as number] ?? String(this.x)

        const rows = tooltipOrder
          .map((kind) => {
            const name = series[kind].name
            const point = byName.get(name)
            if (!point) return ''
            const c = color(kind)
            return `<div class="mts-tip-row">
              <span class="mts-tip-dot" style="background:${c}"></span>
              <span class="mts-tip-label">${name}:</span>
              <span class="mts-tip-value">${formatValue(point.y)}</span>
            </div>`
          })
          .join('')

        return `<div class="mts-tip">
          <div class="mts-tip-date">${header}</div>
          ${rows}
        </div>`
      },
    },
    plotOptions: {
      series: {
        animation: { duration: 450 },
        states: {
          hover: {
            enabled: true,
            lineWidthPlus: 0,
          },
          inactive: {
            opacity: 1,
          },
        },
      },
      area: {
        fillOpacity: 0.95,
        lineWidth: 1,
        marker: {
          enabled: false,
          symbol: 'circle',
          radius: 4,
          fillColor: '#ffffff',
          lineWidth: 2,
          states: {
            hover: {
              enabled: true,
              radius: 5,
            },
          },
        },
        states: {
          hover: {
            halo: {
              size: 10,
              opacity: 0.25,
            },
          },
        },
      },
      spline: {
        lineWidth: 2.25,
        marker: {
          enabled: false,
          symbol: 'circle',
          radius: 4,
          fillColor: '#ffffff',
          lineWidth: 2,
          states: {
            hover: {
              enabled: true,
              radius: 5,
            },
          },
        },
        states: {
          hover: {
            halo: {
              size: 14,
              opacity: 0.22,
            },
          },
        },
      },
      line: {
        lineWidth: 2,
        marker: {
          enabled: true,
          symbol: 'square',
          radius: 4,
          lineWidth: 0,
          states: {
            hover: {
              enabled: true,
              radius: 5,
              lineWidth: 2,
              fillColor: '#ffffff',
            },
          },
        },
        states: {
          hover: {
            halo: {
              size: 14,
              opacity: 0.22,
            },
          },
        },
      },
      column: {
        borderWidth: 0,
        borderRadius: 3,
        pointPadding: 0.28,
        groupPadding: 0.12,
        states: {
          hover: {
            brightness: 0.05,
            halo: { size: 0 },
          },
        },
      },
    },
    series: [
      {
        type: 'area',
        name: series.area.name,
        data: series.area.data,
        color: color('area'),
        fillColor: color('area'),
        lineColor: Highcharts.color(color('area')).brighten(-0.08).get() as string,
        yAxis: 0,
        zIndex: 1,
        marker: { lineColor: color('area') },
      },
      {
        type: 'column',
        name: series.bar.name,
        data: series.bar.data,
        color: color('bar'),
        yAxis: 1,
        zIndex: 2,
      },
      {
        type: 'spline',
        name: series.spline.name,
        data: series.spline.data,
        color: color('spline'),
        yAxis: 0,
        zIndex: 3,
        marker: { lineColor: color('spline') },
      },
      {
        type: 'line',
        name: series.line.name,
        data: series.line.data,
        color: color('line'),
        yAxis: 0,
        zIndex: 4,
        marker: {
          fillColor: color('line'),
          lineColor: color('line'),
        },
      },
    ],
  })
}

export type {
  MixedChartOptions,
  MixedChartSeries,
  SeriesInput,
  SeriesKind,
}
export { DEFAULT_COLORS }
