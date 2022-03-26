#!/bin/usr/env python3

#
# The task here was to combine the MACD Indicator and Moving Average Indicator to 
# alert to a buy signal.
# The final work was requested to be the same code as two videos that were supplied (not ideal):
# https://www.youtube.com/watch?app=desktop&v=kz_NJERCgm8&ab_channel=ComputerScience
# https://www.youtube.com/watch?app=desktop&v=rO_cqa4x60o&ab_channel=ComputerScience
# The Specifications were:
# MACD
# Buy signal should only be executed when the two lines cross and the values for the 
# lines are below a certain level (an example value of .02 was provided).
# Moving Average
# Buy signal would be when the Moving Average is above the stock price with a difference
# of a certain value. A value of greater than 1 was given, so if the price was 10.70 and the moving
# average is 12 the differnce is 1.30 a buy signal would be genrated. 
#

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use('fivethirtyeight')

# STORE THE DATA INTO A VARIABLE 
df = pd.read_csv('AAPL.csv')

# SET THE INDEX
df = df.set_index(pd.DatetimeIndex(df['Date'].values))

# CALCULATE THE MACD ADN SIGNAL LINE INDICATORS
# CALCULATE THE SHORT TERM EXPONENTIAL MOVING AVERAGE (EMA)
ShortEMA = df.Close.ewm(span=12, adjust=False).mean()
# CALCUALATE THE LONG TERM EXPONENTIAL MOVING AVERAGE 
LongEMA = df.Close.ewm(span=26, adjust=False).mean()
# CALCULATE THE MACD LINE
MACD = ShortEMA - LongEMA
# CALCULATE THE SIGNAL LINE
signal = MACD.ewm(span=9, adjust=False).mean()

# CALCULATE THE SHORT/FAST EXPONENTIAL MOVING AVERAGE
ema = df.Close.ewm(span=21, adjust = False).mean()

# CREATE NEW COLUMNS FOR THE DATA
df['MACD'] = MACD
df['Signal Line'] = signal
df['EMA'] = ema

# CREATE A FUNCTION TO SIGNAL WHEN TO BUY AND SELL
def buy_signal(signal):
    Buy = []
    flag = -1

    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal Line'][i]:
            if flag != 1:
                if signal['MACD'][i] < .02 and df['EMA'][i] > df['Close'][i] and df['EMA'][i] - df['Close'][i] > 1:
                    Buy.append(signal['Close'][i])
                    flag = 1
                else:
                    Buy.append(np.nan)
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal Line'][i]:
            Buy.append(np.nan)
            if flag != 0:
                flag = 0 
        else:
            Buy.append(np.nan)

    return Buy

# ADD THE BUY AND SELL SIGNALS TO THE DATA SET
df['Buy'] = buy_signal(df)

# VISUAL SHOW THE STOCK BUY AND SELL SIGNALS
plt.figure(figsize=(12.2, 4.5))
plt.title('Buy and Sell Plot', fontsize = 18)
plt.plot(df['Close'], label= 'Close Price', color = 'blue', alpha = 0.35)
plt.plot(ema, label = 'EMA', color = 'red', alpha = 0.35)
plt.scatter(df.index, df['Buy'], color = 'green', marker='^', alpha = 1)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Close Price', fontsize = 18)
plt.show()
