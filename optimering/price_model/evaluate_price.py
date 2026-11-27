"""Evaluate the 2-day price model by comparing it with two simpler forecasts.

Three forecasts are compared for every day in the period:
- model:     base + weather adjustment (the real 2-day model in price_model.py)
- base_only: the 7-day base without weather adjustment, shows what the weather adds
- baseline:  the price at the same clock time one week earlier. A naive guess that
             needs no model at all; the model is only useful if it beats this.

Measures: MAE (mean error per quarter) and the share of the possible saving when
load is moved to the N cheapest quarters of each day.
"""

import datetime

import pandas as pd

from optimering.price_model.get_grid_price import SWEDISH_TZ, load_prices
from optimering.price_model.get_weather import ARCHIVE_LAG_DAYS, load_weather, to_quarters
from optimering.price_model.price_model import compute_base, fit_coefficients, weather_deviation


N_CHEAPEST = 16  # Number of quarters per day that flexible load is assumed to be moved to
FORECASTS = ["model", "base_only", "baseline"]


def baseline_last_week(prices, day):
    """Naive forecast: each quarter of day D gets the actual price from the same clock time on D-7.
        This is the reference the model is measured against. It needs no calculation,
        only last week's prices, so a model that doesn't beat it adds nothing.
        """

    week_ago = (day - datetime.timedelta(days=7)).isoformat()
    last_week = prices.loc[week_ago:week_ago, "SEK_per_kWh"]

    if last_week.empty:
        raise ValueError(f"No prices for {week_ago}")

    price_per_clock_time = last_week.groupby(last_week.index.strftime("%H:%M")).mean()

    start = pd.Timestamp(day.isoformat(), tz=SWEDISH_TZ)
    end = pd.Timestamp((day + datetime.timedelta(days=1)).isoformat(), tz=SWEDISH_TZ)
    quarters = pd.date_range(start, end, freq="15min", inclusive="left", name="time")

    values = price_per_clock_time.reindex(quarters.strftime("%H:%M")).to_numpy()
    return pd.Series(values, index=quarters, name="baseline")


def model_forecast(prices, weather, a, b, day):
    """Calculate the model forecast without fetching or saving data."""

    base = compute_base(prices, day)
    deviation = weather_deviation(weather, day)

    price = base + a * deviation["wind_deviation"] + b * deviation["temp_deviation"]
    return price.clip(lower=0)


def daily_savings(predicted, actual):
    """Calculate actual savings and maximum possible savings."""

    day_mean = actual.mean()

    # Savings using the forecast
    chosen = predicted.nsmallest(N_CHEAPEST).index
    actual_saving = day_mean - actual.loc[chosen].mean()

    # Savings if we knew the actual prices
    possible_saving = day_mean - actual.nsmallest(N_CHEAPEST).mean()

    return float(actual_saving), float(possible_saving)


def summarize(results):
    """Calculate MAE and savings for each forecast."""

    summary = {}

    for name in FORECASTS:
        daily_share = results[f"{name}_saving"] / results["possible_saving"]

        summary[name] = {
            "mae": results[f"{name}_abs_error"].sum() / results["quarters"].sum(),
            "share_of_possible_saving": results[f"{name}_saving"].sum() / results["possible_saving"].sum(),
            "median_daily_share": daily_share.median(),
        }

    return pd.DataFrame(summary).T


def evaluate(start, end):
    """Evaluate the three forecasts between start and end."""

    # Check that historical weather data is available
    latest_end = datetime.datetime.now(SWEDISH_TZ).date() - datetime.timedelta(days=ARCHIVE_LAG_DAYS)

    if end > latest_end:
        raise ValueError(f"end must be at most {latest_end}")

    # Load data and train the model using data before the evaluation period
    prices = load_prices()
    weather = to_quarters(load_weather())

    before_start = (start - datetime.timedelta(days=1)).isoformat()
    a, b = fit_coefficients(prices.loc[:before_start], weather.loc[:before_start])

    rows = []
    skipped_days = 0

    # Evaluate each day
    for day in pd.date_range(start, end, freq="D").date:
        try:
            model = model_forecast(prices, weather, a, b, day)
            base_only = compute_base(prices, day)
            baseline = baseline_last_week(prices, day)

        except ValueError:
            skipped_days += 1
            continue

        # Get actual prices and compare with forecasts
        actual = prices.loc[day.isoformat():day.isoformat(), "SEK_per_kWh"]

        table = pd.DataFrame({
            "actual": actual,
            "model": model,
            "base_only": base_only,
            "baseline": baseline
        })

        if actual.empty or table.isna().any().any():
            skipped_days += 1
            continue

        # Calculate errors and savings for each forecast
        row = {
            "day": day,
            "quarters": len(table),
            "actual_sum": table["actual"].sum()
        }

        for name in FORECASTS:
            row[f"{name}_abs_error"] = (table[name] - table["actual"]).abs().sum()
            row[f"{name}_saving"], row["possible_saving"] = daily_savings(table[name], table["actual"])

        rows.append(row)

    # Calculate final results
    results = pd.DataFrame(rows)
    summary = summarize(results)
    mean_price = results["actual_sum"].sum() / results["quarters"].sum()

    # Print results
    print(f"Period: {start} to {end}")
    print(f"Days used: {len(rows)}")
    print(f"Days skipped: {skipped_days}")
    print(f"Mean price: {mean_price:.4f} SEK/kWh")
    print(f"a: {a:.4f}, b: {b:.4f}")
    print(f"Cheapest quarters: {N_CHEAPEST}")
    print(summary.round(4).to_string())
    print("Weather: historical data, not forecasts (result somewhat better than live)")

    return summary