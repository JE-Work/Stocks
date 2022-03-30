#!/bin/usr/env python3

#
# This script fetches stock price data for the specified time period.
# It calculates the On-balance Volume Indicator
# https://school.stockcharts.com/doku.php?id=technical_indicators:on_balance_volume_obv
# It plots the stock price in one panel with OBV in another panel below.
#

import datetime as dt
import mplfinance as mpf
import numpy as np
import pandas as pd
from pandas_datareader import data as web

# PARAMETER VALUES
TICKER = 'MSFT'
START_DATE = dt.datetime(2021, 10, 27)
TODAY = dt.datetime.today()

# FETCH PRICE DATA FROM YAHOO
df = web.DataReader(TICKER, 'yahoo', START_DATE, TODAY)
df.index.name = 'Date'

#CALCULATE OBV
obv_cond = np.where(df['Close'] < df['Close'].shift(1), -df['Volume'], df['Volume'])
obv = pd.Series(obv_cond, index=df['Close'].index).cumsum()

# CHART SETTINGS
setup = dict(type='candle',figscale=1.25)
mc = mpf.make_marketcolors(up='black',down='r',edge='inherit')
s = mpf.make_mpf_style(marketcolors=mc)
                       
# PLOT PRICE AND OBV
add_obv = [ mpf.make_addplot(obv,color='black',panel=1) ]
mpf.plot(df,**setup,style=s,addplot=add_obv)
