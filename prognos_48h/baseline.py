import pandas as pd

def make_forecast(history, day):
    day = pd.Timestamp(day).normalize()
    # Calculate the date one week before day
    last_week = day - pd.Timedelta(days=7)

    # get the rows for that day
    dates = history["tid"].dt.normalize()
    mask = dates == last_week
    rows = history[mask].copy()

    # move the times one week forward
    rows["tid"] = rows["tid"] + pd.Timedelta(days=7)

    # return company, time, kw
    if rows.empty:
        raise ValueError(f"No data for {last_week.date()}")
    return rows

