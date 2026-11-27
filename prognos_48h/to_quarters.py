import pandas as pd

def to_quarters(forecast):
    forecast = forecast.reset_index(drop=True)

    step = forecast["tid"].drop_duplicates().sort_values().diff().min()
    if step == pd.Timedelta(minutes=15):
        return forecast

    quarters = forecast.loc[forecast.index.repeat(4)].copy()
    offsets = [0, 15, 30, 45] * len(forecast)
    quarters["tid"] = quarters["tid"] + pd.to_timedelta(offsets, unit="min")
    return quarters.reset_index(drop=True)
