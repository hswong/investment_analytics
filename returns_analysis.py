import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Use Quandl to get adjusted close price
#quandl.ApiConfig.api_key = 'Enter Your Key'
#stocks = ['MSFT', 'AAPL', 'WMT', 'GE', 'KO', 'F', 'JNJ', 'BA', 'XOM']
#stockdata = quandl.get_table('WIKI/PRICES', ticker = stocks, paginate=True,
#                    qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
#                    date = { 'gte': '1995-1-1', 'lte': '2000-12-31' })

# Transform the Yahoo Finance data into the quandl data
stockdata = pd.read_csv("data/SPY.csv") 
stockdata = stockdata.rename(columns={"Date":"date"})
stockdata['ticker'] = 'SPY'

# Setting date as index with columns of tickers and adjusted closing 
# price
data1 = stockdata.set_index('date')
table = data1.pivot(columns='ticker')
#table.head()

# Daily and annual returns of the stocks
returns_daily = table.pct_change()
returns_daily.to_csv('daily_returns.csv')

# Annual Returns
#returns_yearly = table.asfreq('BA').pct_change()
returns_yearly = table.asfreq('BA')
returns_yearly.to_csv('annual_returns.csv')

# 5 Year returns
returns_5year=table.pct_change(periods=260*5)
returns_5year.to_csv('5_Years_Returns.csv')