# 48-hour forecast

Forecasts each company's power demand (kW) per hour for a production day,
made 48 hours in advance.

## Current method: baseline

`baseline.py` contains `make_forecast(history, day)`. Each hour of the
production day is forecast as the same hour one week earlier.
## Input

- `history`: a pandas DataFrame in long format, one row per company and hour:

  | foretag | tid                 | kw     |
  |---------|---------------------|--------|
  | A       | 2024-03-06 00:00:00 | 107.62 |

  `tid` must be a datetime column, not text.
- `day`: the production day as a `pd.Timestamp`, e.g. `pd.Timestamp("2024-03-13")`.

## Output

A DataFrame with the same columns (`foretag`, `tid`, `kw`) and 24 rows per
company for the production day.

## Usage

```python
import pandas as pd
from prognos_48h.baseline import make_forecast

forecast = make_forecast(history, pd.Timestamp("2024-03-13"))
forecast.to_csv("data/processed/forecast_48h.csv", index=False)
```

When reading the CSV, convert `tid` back to datetime:

```python
forecast = pd.read_csv("data/processed/forecast_48h.csv", parse_dates=["tid"])
```