# Mixed time-series chart (Django)

Тестовое задание: интерактивный график с **четырьмя** time-series последовательностями:

| Ключ | Тип | Стиль |
| --- | --- | --- |
| `area` | Area | Жёлтая заливка (Cost) |
| `spline` | Spline | Зелёная гладкая кривая (ROI confirmed) |
| `line` | Line | Фиолетовая линия с квадратными маркерами (Conversions) |
| `bar` | Column | Короткие синие столбцы (CPA) |

Бизнес-логика сборки графика — на **Python**. Django отдаёт страницу и JSON API. Highcharts только рендерит готовый options-объект в браузере.

## Быстрый старт

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Открой [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Инициализация с четырьмя последовательностями (Python)

```python
from charts.mixed_chart import create_mixed_chart

options = create_mixed_chart(
    dates=["2026-06-11", "2026-06-12", "2026-06-13"],
    area={"name": "Cost", "data": [25.85, 44.36, 55.65]},
    spline={"name": "ROI confirmed", "data": [180.5, 161.47, 56.33]},
    line={"name": "Conversions", "data": [30, 36, 70]},
    bar={"name": "CPA", "data": [0.86, 1.23, 0.79]},
)
```

Правила:

1. Длина каждого `data` = длина `dates`
2. Ключи серий строго: `area`, `spline`, `line`, `bar`
3. Опционально: `color` у серии, `height`, `bar_axis_padding`

## HTTP API

### Demo options

```bash
curl http://127.0.0.1:8000/api/chart/
```

### Собрать график из своих данных

```bash
curl -X POST http://127.0.0.1:8000/api/chart/build/ \
  -H "Content-Type: application/json" \
  -d "{
    \"dates\": [\"2026-06-11\", \"2026-06-12\", \"2026-06-13\"],
    \"series\": {
      \"area\":   {\"name\": \"Cost\", \"data\": [25.85, 44.36, 55.65]},
      \"spline\": {\"name\": \"ROI confirmed\", \"data\": [180.5, 161.47, 56.33]},
      \"line\":   {\"name\": \"Conversions\", \"data\": [30, 36, 70]},
      \"bar\":    {\"name\": \"CPA\", \"data\": [0.86, 1.23, 0.79]}
    }
  }"
```

## Структура

```
charts/
  mixed_chart.py     # Python API + валидация 4 серий
  demo_data.py       # демо-данные
  views.py           # Django views / API
  templates/charts/  # страница
  static/charts/     # CSS + тонкий JS-mount
config/              # settings, urls
manage.py
requirements.txt
```

## Тесты

```bash
python manage.py test charts
```

## Заметка по Highcharts

Для отрисовки используется Highcharts CDN. Для коммерческого продукта нужна их лицензия; для тестового/некоммерческого демо обычно достаточно evaluation terms.
