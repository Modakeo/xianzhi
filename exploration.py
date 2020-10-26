# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: xianzhi
#     language: python
#     name: xianzhi
# ---

# +
# pip install alpaca_trade_api
import alpaca_trade_api as tradeapi
import pandas as pd
import datetime
import numpy as np
import pandas_market_calendars as mcal

# myPackage
import keys

pd.set_option("display.max_rows", 400)
pd.set_option("display.min_rows", 30)
# -

api = tradeapi.REST(
    keys.api_key["key_id"], keys.api_key["secret_key"], keys.api_key["base_url"]
)


def get_six_months_data_for_one_stock(
    api,
    symbol,
    interval="1Min",
    start="2020-04-01T09:30:00-04:00",
    end="2020-10-23T16:00:00-04:00",
):
    """
    Using Alpaca to get roughly 6 months data.
    Note: Only valid for summer time
          Only valid for 1min so far
          Only valid for NASDAQ

    :param symbols: The parameter symbols can be either a comma-split
        string or a list of string. Each symbol becomes the key of the
        returned value.

    :param interval: One of minute, 1Min, 5Min, 15Min, day or 1D. minute
        is an alias of 1Min. Similarly, day is of 1D.

    :param limit: The maximum number of bars per symbol. It can be between
        1 and 1000. Default is 100.

    :param start or end: ISO Format str, ex: '2019-04-15T09:30:00-04:00' or
        '2019-04-15'
        start='2020-04-01T09:30:00-04:00', end='2020-04-01T16:00:00-04:00'
    """
    tmp_df = api.get_barset(symbols=symbol, timeframe=interval, start=start, end=end)[
        symbol
    ].df
    tmp_df.index = tmp_df.index + datetime.timedelta(minutes=1)
    tmp_df["Time"] = tmp_df.index.time
    tmp_df["Date"] = tmp_df.index.date

    # Get the business dates and hours from 3rd-party package
    NASDAQ = mcal.get_calendar("NASDAQ")
    tmp_schedule = NASDAQ.schedule(start_date=start, end_date=end)
    business_datetime = mcal.date_range(tmp_schedule, frequency=interval).tz_convert(
        "America/New_York"
    )

    # Merge Alpaca data to full datetime
    base_df = pd.DataFrame(index=business_datetime)
    base_df = base_df.merge(tmp_df, how="left", left_index=True, right_index=True)

    return base_df


# For example, get Apple data from 2020-04-01 to 10-23
df = get_six_months_data_for_one_stock(
    api,
    "AAPL",
    interval="1Min",
    start="2020-04-01T09:30:00-04:00",
    end="2020-10-23T16:00:00-04:00",
)

df[df.close.isnull()]


