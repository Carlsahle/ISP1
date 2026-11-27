import pandas as pd

from baseline import make_forecast
from to_quarters import to_quarters

def forecast_48h(history, day):
    forecast = make_forecast(history, day)
    forecast["kw_p90"] = forecast["kw"] * 1.1
    forecast = to_quarters(forecast)
    forecast = forecast.rename(columns={"foretag": "company_id", "tid": "time", "kw": "power", "kw_p90": "w90"})
    return forecast