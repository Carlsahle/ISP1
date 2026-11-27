#Fetch and store hourly weather data from Open-Meteo for the price model


import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import requests

# Same first day as the prices, so weather and prices cover the same period.
from optimering.price_model.get_grid_price import FIRST_DAY

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_FILE = Path(__file__).parent.parent.parent / "data" / "raw" / "weather.csv"
SWEDISH_TZ = ZoneInfo("Europe/Stockholm")

# The archive's last days are preliminary; stop this many days before today.
ARCHIVE_LAG_DAYS = 5

# Averaging several places gives a better picture of the weather that drives the SE3 price than one single place.
LOCATIONS = {
    "Vargarda": (57.98, 12.81),
    "Stockholm": (59.33, 18.07),
    "Goteborg": (57.71, 11.97),
}

def fetch_weather_history(start, end):
    """Fetch hourly wind and temperature from the archive for all locations. Start and end are datetime.date and both included
    Returns a DataFrame with one row per location and hour.
    """

    # Prepare API parameters to fetch weather data for each location
    one_day = datetime.timedelta(days=1)
    all_locations = []
    for name, (latitude, longitude) in LOCATIONS.items():
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": (start - one_day).isoformat(),
            "end_date": (end + one_day).isoformat(),
            "hourly": "wind_speed_100m,temperature_2m", #get wind speed 100m above ground and temperature 2m above ground
            "wind_speed_unit": "ms",  # default is km/h, the model uses m/s
            "timezone": "GMT",
        }

        # Fetch weather data from the API and check for errors
        response = requests.get(ARCHIVE_URL, params=params, timeout=60)
        response.raise_for_status()

        # Process weather data and store it for each location
        weather = pd.DataFrame(response.json()["hourly"])
        weather["time"] = pd.to_datetime(weather["time"], utc=True).dt.tz_convert(SWEDISH_TZ)
        weather.insert(1, "location", name)
        all_locations.append(weather)

    return pd.concat(all_locations, ignore_index=True)

def update_weather_file():
    """Fetch the whole weather history and overwrite data/raw/weather.csv
    Returns the number of rows saved (one per location and hour)
    """

    # Fetch historical weather data between 2025-10-01 and the days where the data is real is not a part of a weather forecast
    today = datetime.datetime.now(SWEDISH_TZ).date()
    end = today - datetime.timedelta(days=ARCHIVE_LAG_DAYS)
    weather = fetch_weather_history(FIRST_DAY, end)

    # Save the time
    weather["time"] = weather["time"].map(pd.Timestamp.isoformat)
    weather.to_csv(WEATHER_FILE, index=False)
    return len(weather)

def load_weather():
    """Read the weather file and return hourly weather per location.
    Returns a DataFrame with the same columns as fetch_weather_history(): time, location, wind_speed_100m and temperature_2m.
    """
    weather = pd.read_csv(WEATHER_FILE)

    #Fixes that the file contains both winter and summer times
    times = pd.to_datetime(weather["time"], utc=True)
    weather["time"] = times.dt.tz_convert(SWEDISH_TZ)
    return weather

def fetch_weather_forecast(day):
    """Fetch the last 7 days and the forecast up to day D for all locations.
    Returns a DataFrame in the same format as fetch_weather_history().
    """
    
    # Calculate the number of forecast days needed
    today = datetime.datetime.now(SWEDISH_TZ).date()
    forecast_days = (day - today).days + 2
    
    # Prepare API parameters to fetch weather data for each location
    all_locations = []
    for name, (latitude, longitude) in LOCATIONS.items():
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "past_days": 7,
            "forecast_days": forecast_days,
            "hourly": "wind_speed_100m,temperature_2m",
            "wind_speed_unit": "ms",  # default is km/h, the model uses m/s
            "timezone": "GMT",  # same reason as in fetch_weather_history
        }
        
        # Fetch weather data from the API and check for errors
        response = requests.get(FORECAST_URL, params=params, timeout=60)
        response.raise_for_status()
        
        # Process weather data and store it for each location
        weather = pd.DataFrame(response.json()["hourly"])
        weather["time"] = pd.to_datetime(weather["time"], utc=True).dt.tz_convert(SWEDISH_TZ)
        weather.insert(1, "location", name)
        all_locations.append(weather)

    return pd.concat(all_locations, ignore_index=True)

def to_quarters(weather):
    """Calculate the average across all locations and convert hourly data to 15-minute intervals
    Returns a DataFrame with the quarter's start time as index and the columns wind_speed_100m and temperature_2m.
    """

    # Calculate the average weather values across all locations for each hour
    hourly = weather.groupby("time")[["wind_speed_100m", "temperature_2m"]].mean()


    # Create timestamps at 15-minute intervals
    quarter_times = pd.date_range(hourly.index[0], hourly.index[-1], freq="15min", name="time")

    # Add rows for each 15-minute interval, leaving missing values empty
    quarters = hourly.reindex(quarter_times)

    return quarters.interpolate(method="linear")
