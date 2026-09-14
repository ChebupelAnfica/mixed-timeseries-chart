import './style.css'
import { createMixedChart } from './chart'
import { demoOptions } from './demo/sampleData'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <main class="page">
    <header class="page-header">
      <h1>Mixed time-series chart</h1>
      <p>Area · Spline · Line · Bar — hover to inspect values</p>
    </header>

    <section class="chart-shell">
      <aside class="metric-rail" aria-hidden="true">
        <span class="metric-rail__label">Tdy</span>
        <span>0%</span>
        <span>$0</span>
        <span>$0</span>
        <span>0</span>
        <span>0</span>
        <span class="metric-rail__dash">—</span>
      </aside>

      <div class="chart-panel">
        <button class="edit-btn" type="button" title="Edit" aria-label="Edit">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M12 20h9"/>
            <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>
          </svg>
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
            <path d="m6 9 6 6 6-6"/>
          </svg>
        </button>
        <div class="chart-frame">
          <div id="chart"></div>
        </div>
      </div>
    </section>

    <section class="howto">
      <h2>Initialize with your data</h2>
      <pre><code>import { createMixedChart } from './chart'

createMixedChart('chart', {
  dates: ['2026-06-11', '2026-06-12', '2026-06-13'],
  series: {
    area:   { name: 'Cost', data: [25.85, 44.36, 55.65] },
    spline: { name: 'ROI confirmed', data: [180.5, 161.47, 56.33] },
    line:   { name: 'Conversions', data: [30, 36, 70] },
    bar:    { name: 'CPA', data: [0.86, 1.23, 0.79] },
  },
})</code></pre>
    </section>
  </main>
`

createMixedChart('chart', demoOptions)
