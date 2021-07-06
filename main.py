import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import yfinance as yf
import pandas_market_calendars as mcal
import csv
from data_loading_helpers import *
from data_transformation_helpers import *

txn_df = pd.read_csv('data/Account_Extract.YHD6sYsXqtpIh9RB.user.securities.transactions.csv', thousands=',')

# TODO - change this to trigger off correct mapper depending on source files
load_mapper_orovault(txn_df)

post_load_processing(txn_df)
enrich(txn_df)

# Create the dataset of days and instruments with position changes
positions_df = create_position_deltas(txn_df)

# TODO - debug code to be removed
txn_df.to_csv('transactions.csv')

#txn_df['Open date'] = pd.to_datetime(txn_df['Open date'])