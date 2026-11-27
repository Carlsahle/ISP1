"""Fetch and store SE3 electrical grid prices from elprisetjustnu.se and stores them in data/raw/spot_price_SE3.csv one row per quarter from 2025-10-01 and forward.
From 2025-10-01 beacuse this is when the nordic power markets changed from hoours to quarters."""

import datetime
import time

from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import requests

API_URL = "https://www.elprisetjustnu.se/api/v1/prices/{year}/{month_day}_SE3.json"
PRICE_FILE = Path(__file__).parent.parent.parent / "data" / "raw" / "spot_price_SE3.csv"

# Real quarter-hour prices only exist from this day.
FIRST_DAY = datetime.date(2025, 10, 1)
SWEDISH_TZ = ZoneInfo("Europe/Stockholm")


def fetch_price_day(day):
    """Fetch the electrical grid prices for one day in SE3.
    Returns a list with one dict per quarter, each dictionary with the keys: time_start, time_end and SEK_per_kWh (excl. VAT)
    Returns empty list if prices not published
    """

    #get URL and response
    url = API_URL.format(year=day.year, month_day=day.strftime("%m-%d"))
    response = requests.get(url, timeout=30)

    # If not price not published, return empty list
    if response.status_code == 404:
        return []
    response.raise_for_status()

    #create a list of dictionaries of the given day
    rows = []
    for item in response.json():
        rows.append({
            "time_start": item["time_start"],
            "time_end": item["time_end"],
            "SEK_per_kWh": item["SEK_per_kWh"],
        })
    return rows

def update_price_file():
    """Fetch all missing days and save them in data/raw/spot_price_SE3.csv.
    Checks every day from FIRST_DAY up to and including tomorrow. Days already in the file are skipped
    Returns the number of days that were fetched.
    """


    if PRICE_FILE.exists():
        #Read older grid prices
        old_prices = pd.read_csv(PRICE_FILE, dtype={"time_start": str, "time_end": str})
    else:
        #If file not exist, create empty DataFrame
        old_prices = pd.DataFrame(columns=["time_start", "time_end", "SEK_per_kWh"])

    #Store all unique dates
    days_in_file = set(old_prices["time_start"].str[:10])

    #get date of tomorrow:
    tomorrow = datetime.datetime.now(SWEDISH_TZ).date() + datetime.timedelta(days=1)

    #update grid price data
    new_rows = []
    days_fetched = 0
    day = FIRST_DAY
    while day <= tomorrow:
        if day.isoformat() not in days_in_file:
            try:
                #Get price
                rows = fetch_price_day(day)
                time.sleep(0.3)  #don't send all requests at once

            #If network error catch the error and end the loop while saving what has already been fetched.
            except requests.RequestException as error:
                print(f"Stopped at {day}: {error}. Run again to continue.")
                break  # save what we have so far

            if rows:
                new_rows.extend(rows)
                days_fetched += 1
        day += datetime.timedelta(days=1)

    #If there are new rows add them in and sort according to time, save everything in PRICE_FILE
    if new_rows:
        all_prices = pd.concat([old_prices, pd.DataFrame(new_rows)], ignore_index=True)
        all_prices = all_prices.sort_values(
            "time_start", key=lambda times: pd.to_datetime(times, utc=True)
        )
        all_prices.to_csv(PRICE_FILE, index=False)
    return days_fetched

def load_prices():
    """Read the price file and return one price per quarter.
    Returns a DataFrame with the quarter's start time as index and one column, SEK_per_kWh.
    """

   #Get prices from price file
    prices = pd.read_csv(PRICE_FILE, usecols=["time_start", "SEK_per_kWh"])


   #Convert timestamps to Swedish time, handling the switches from winter/summer time correctly
    times = pd.to_datetime(prices["time_start"], utc=True) #convert to UTC
    prices["time_start"] = times.dt.tz_convert(SWEDISH_TZ) # convert back to swedish timezone,

    return prices.set_index("time_start")
