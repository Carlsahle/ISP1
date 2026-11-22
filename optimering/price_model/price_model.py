"""The 2-day price model of SE3"""

import datetime

import numpy as np
import pandas as pd

from pathlib import Path

from optimering.price_model.get_grid_price import SWEDISH_TZ, load_prices, update_price_file
from optimering.price_model.get_weather import (fetch_weather_forecast, load_weather,
                                    to_quarters, update_weather_file)

# The base and the weather means use the 7 days before day D.
BASE_DAYS = 7
PROCESSED_DIR = Path(__file__).parent.parent.parent / "data" / "processed"

def compute_base(prices, day):
    """Calculate the average price for each quarter using the previous 7 days
    Returns a Series with day D's quarters as index and the base price in SEK/kWh
    """

    # Define the period used to calculate the base price
    first_day = day - datetime.timedelta(days=BASE_DAYS)
    last_day = day - datetime.timedelta(days=1)

    # Get the electricity prices from the selected period
    week = prices.loc[first_day.isoformat():last_day.isoformat(), "SEK_per_kWh"]
    if week.empty:
        raise ValueError(f"No prices between {first_day} and {last_day}")

    # Calculate the average electricity price for each quarter of the day
    mean_per_clock_time = week.groupby(week.index.strftime("%H:%M")).mean()

    # Define the start and end timestamps for day D
    start = pd.Timestamp(day.isoformat(), tz=SWEDISH_TZ)
    end = pd.Timestamp((day + datetime.timedelta(days=1)).isoformat(), tz=SWEDISH_TZ)

    # Create timestamps for every 15-minute interval of day D
    quarters = pd.date_range(start, end, freq="15min", inclusive="left", name="time")

    # Match the average prices to the corresponding quarters of day D
    base_values = mean_per_clock_time.reindex(quarters.strftime("%H:%M")).to_numpy()

    return pd.Series(base_values, index=quarters, name="base")

def weather_deviation(weather, day):
    """Calculate wind and temperature deviations from the previous 7-day average
    Returns a DataFrame with day D's timestamps as index and columns for wind and temperature deviations
    """

    # Define the period used to calculate the average weather
    first_day = day - datetime.timedelta(days=BASE_DAYS)
    last_day = day - datetime.timedelta(days=1)

    # Get weather data from the previous 7 days
    week = weather.loc[first_day.isoformat():last_day.isoformat()]

    # Get weather data for day D
    day_d = weather.loc[day.isoformat():day.isoformat()]
    # A partial week would give a mean over other days than the base uses.
    days_in_week = len(set(week.index.date))
    if days_in_week < BASE_DAYS or day_d.empty:
        raise ValueError(f"Weather missing for {day} or the 7 days before")

    # Calculate wind and temperature deviation from the previous 7-day average
    deviation = pd.DataFrame(index=day_d.index)
    deviation["wind_deviation"] = day_d["wind_speed_100m"] - week["wind_speed_100m"].mean()
    deviation["temp_deviation"] = day_d["temperature_2m"] - week["temperature_2m"].mean()

    return deviation

def fit_coefficients(prices, weather):
    """Use linear regression to calculate how wind and temperature deviations affect electricity prices.
    The coefficients are found using the least squares method, which minimizes the squared differences between predicted and actual price deviations.
    Returns two coefficients: a for wind speed and b for temperature.
    """

    # Get all unique dates with price data
    all_days = sorted(set(prices.index.date))
    day_tables = []

    # Loop through all days after the first 7 days
    for day in all_days[BASE_DAYS:]:
        # Calculate base prices and weather deviations, skip days with missing data
        try:
            base = compute_base(prices, day)
            day_table = weather_deviation(weather, day)
        except ValueError:
            continue

        # Get the actual electricity prices for the day
        actual = prices.loc[day.isoformat():day.isoformat(), "SEK_per_kWh"]

        # Calculate the difference between actual prices and base prices and store the data for this day
        day_table["price_deviation"] = actual - base
        day_tables.append(day_table)

    # Combine all days into one DataFrame and remove rows with missing values
    data = pd.concat(day_tables).dropna()


    x = data[["wind_deviation", "temp_deviation"]].to_numpy()
    y = data["price_deviation"].to_numpy()

    # Calculate the coefficients using least squares regression
    (a, b), *_ = np.linalg.lstsq(x, y, rcond=None)
    return float(a), float(b)


def forecast_price_2d(day):
    """
       Forecast electricity prices for day D using a linear regression model.

       The model uses the average price from the previous 7 days as a base
       and adjusts it based on wind and temperature deviations.

       Formula: P(t) = B(t) + a * dW(t) + b * dT(t)

       P(t)  = Predicted electricity price
       B(t)  = Base price from the previous 7 days
       dW(t) = Wind speed deviation from the 7-day average
       dT(t) = Temperature deviation from the 7-day average
       a, b  = Coefficients calculated using linear regression

        Returns a DataFrame with predicted prices for each 15-minute interval, the forecast is also saved to a CSV file.
       """

    update_price_file()
    prices = load_prices()

    # Check that electricity prices for the day before D are available
    day_before = (day - datetime.timedelta(days=1)).isoformat()
    if prices.loc[day_before:day_before].empty:
        raise ValueError(f"Prices for {day_before} are not published yet (after 13:00)")

    # Update historical weather data and train the linear regression model
    update_weather_file()
    a, b = fit_coefficients(prices, to_quarters(load_weather()))

    # Fetch the weather forecast and calculate wind and temperature deviations for day D
    deviation = weather_deviation(to_quarters(fetch_weather_forecast(day)), day)

    # Predict electricity prices by adjusting the base price with weather deviations
    base = compute_base(prices, day)
    price = base + a * deviation["wind_deviation"] + b * deviation["temp_deviation"]

    # Check that the forecast contains no missing values
    if price.isna().any():
        raise ValueError(f"Forecast for {day} has missing quarters")
    price = price.clip(lower=0)  # negative forecasts are set to 0

    # Create a DataFrame with timestamps, forecast horizon and predicted prices
    forecast = pd.DataFrame({
        "ts": [t.isoformat() for t in price.index],
        "horizon": "2d",
        "price_sek_kwh": price.to_numpy(),
    })

    # Create the output directory and save the forecast as a CSV file
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    forecast.to_csv(PROCESSED_DIR / f"price_2d_{day.isoformat()}.csv", index=False)
    return forecast

