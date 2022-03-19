#!/usr/bin/env python

# A script using the yfinance package to fetch the specified price history 
# data for a given ticker.

import yfinance as yf
import pandas as pd

# PARAMETERS FOR PRICE HISTORY
PERIOD = "1y"
INTERVAL = "1wk"
TICKER = "MSFT"

def price_data(ticker):
    try:
        symbol = yf.Ticker(ticker)
        data = symbol.history(period=PERIOD, threading=False, interval=INTERVAL)	
        data = data[['Open', 'High', 'Low', 'Close']]
        data.to_csv(f'price-data.csv')
    except:
        print(f"Unable to retrieve the data for {TICKER}")

def main():

    price_data(TICKER)

if __name__ == "__main__":
    main()
