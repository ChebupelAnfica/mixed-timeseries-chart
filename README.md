# Mixed time-series chart

Interactive chart that renders **four** time-series sequences as:

| Key | Type | Style in the demo |
| --- | --- | --- |
| `area` | Area | Pale yellow filled area (Cost) |
| `spline` | Spline | Smooth green curve (ROI confirmed) |
| `line` | Line | Purple polyline with square markers (Conversions) |
| `bar` | Column bars | Short blue bars along the baseline (CPA) |

Hover shared tooltip shows the date (`DD.MM.YYYY`) and all four values with color dots — matching the reference GIF behavior.

## Quick start

```bash
npm install
npm run dev
```

Open the local URL printed by Vite (usually `http://localhost:5173`).

Production build:

```bash
npm run build
npm run preview
```

## Initialize with four sequences

```ts
import { createMixedChart } from './src/chart'

const chart = createMixedChart(document.getElementById('chart')!, {
  dates: [
    '2026-06-11',
    '2026-06-12',
    '2026-06-13',
  ],
  series: {
    area: {
      name: 'Cost',
      data: [25.85, 44.36, 55.65],
    },
    spline: {
      name: 'ROI confirmed',
      data: [180.5, 161.47, 56.33],
    },
    line: {
      name: 'Conversions',
      data: [30, 36, 70],
    },
    bar: {
      name: 'CPA',
      data: [0.86, 1.23, 0.79],
    },
  },
})

// later…
// chart.destroy()
```

### Rules

1. `dates.length` must equal every `series.*.data.length`.
2. Series keys must be exactly: `area`, `spline`, `line`, `bar`.
3. Optional per-series `color` overrides the defaults.
4. Optional `height` (px) and `barAxisPadding` (how short the bars stay relative to their values).

### Defaults

```ts
import { DEFAULT_COLORS } from './src/chart'
// {
//   area:   '#F5E19A',
//   spline: '#1F800E',
//   line:   '#B010E8',
//   bar:    '#3870FE',
// }
```

## Project layout

```
src/
  chart/
    createMixedChart.ts   # public API
    types.ts
    index.ts
  demo/
    sampleData.ts         # GIF-inspired demo dataset
  main.ts                 # demo page
  style.css
```

## License note

Demo uses [Highcharts](https://www.highcharts.com/) via npm. Highcharts requires a license for commercial products; free for non-commercial / evaluation use. See their licensing terms before shipping.
