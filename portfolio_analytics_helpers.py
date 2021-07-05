#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import yfinance as yf
import pandas_market_calendars as mcal
import csv
from plotly.offline import init_notebook_mode, plot
init_notebook_mode(connected=True)

'''
Create a list of market open dates and return the list
'''
def create_market_cal(start_period, end_period):
    nyse = mcal.get_calendar('NYSE')
    schedule = nyse.schedule(start_period, end_period)
    market_cal = mcal.date_range(schedule, frequency='1D')
    market_cal = market_cal.tz_localize(None)
    market_cal = [i.replace(hour=0) for i in market_cal]
    return market_cal

def calculate_sortino_ratio(portfolio_df, risk_free_rate):
    # Create a downside return series with the negative returns only
    target = 0 
    downside_returns = portfolio_df.loc[portfolio_df['pf_returns'] < target]

    # Calculate expected return and std dev of downside
    expected_return = portfolio_df['pf_returns'].mean()
    down_stdev = downside_returns['pf_returns'].std()

    # Calculate the sortino ratio
    sortino_ratio = (expected_return - risk_free_rate)/down_stdev

    # Print the results
    print("Expected return  : ", expected_return*100)
    print("Downside risk   : ", down_stdev*100)
    print("Sortino ratio : ", sortino_ratio)
