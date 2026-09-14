/** One of the four series kinds rendered by the mixed chart. */
export type SeriesKind = 'area' | 'spline' | 'line' | 'bar'

export interface SeriesInput {
  /** Display name in the tooltip (e.g. "Cost"). */
  name: string
  /** Values aligned 1:1 with `dates`. */
  data: number[]
  /** Optional override of the default series color. */
  color?: string
}

export interface MixedChartSeries {
  area: SeriesInput
  spline: SeriesInput
  line: SeriesInput
  bar: SeriesInput
}

export interface MixedChartOptions {
  /**
   * ISO dates (`YYYY-MM-DD`) or any parseable date strings.
   * Shown in the tooltip as `DD.MM.YYYY`.
   */
  dates: string[]
  /** Four time-series sequences. Length of each `data` must match `dates`. */
  series: MixedChartSeries
  /** Chart height in pixels. Default: 320. */
  height?: number
  /** Soft-max multiplier for the bar axis so bars stay short. Default: 8. */
  barAxisPadding?: number
}

export const DEFAULT_COLORS: Record<SeriesKind, string> = {
  area: '#F5E19A',
  spline: '#1F800E',
  line: '#B010E8',
  bar: '#3870FE',
}
