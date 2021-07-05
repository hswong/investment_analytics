from numpy.core.numeric import normalize_axis_tuple
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import yfinance as yf
import pandas_market_calendars as mcal
import csv
from analytics_datafields import *


credit_transaction_types = [
    TransactionType.Buy
]

debit_transaction_types = [
    TransactionType.Sell
]

def position_adjust(position_deltas, transaction):
    identifier = transaction[AssetIdentifier.Identifier.value]

    if transaction[TransactionDetails.TransactionType.value] in debit_transaction_types:
        transaction_type = 'debit'
        remaining_quantity = -transaction[HoldingDetailField.Quantity.value]
    elif transaction[TransactionDetails.TransactionType.value] in credit_transaction_types:
        transaction_type = 'credit'
        remaining_quantity = transaction[HoldingDetailField.Quantity.value]
    else:
        raise TypeError('Not yet configured transaction type:'+transaction[TransactionDetails.TransactionType.value])

    for position in position_deltas[AssetIdentifier.Identifier.value].iterrows():
        if remaining_quantity > 0 and position[1][HoldingDetailField.OpenQuantity.value] < 0:
            quantity_to_close = remaining_quantity if abs(position[1][HoldingDetailField.OpenQuantity.value]) > remaining_quantity\
                 else -position[1][HoldingDetailField.OpenQuantity.value]
            remaining_quantity = remaining_quantity - quantity_to_close
        elif remaining_quantity < 0 and position[1][HoldingDetailField.OpenQuantity.value] > 0:
            quantity_to_close = remaining_quantity if position[1][HoldingDetailField.OpenQuantity.value] > abs(remaining_quantity)\
                 else position[1][HoldingDetailField.OpenQuantity.value]
            remaining_quantity = remaining_quantity + quantity_to_close

    if remaining_quantity:
        transaction[HoldingDetailField.OpenQuantity.value] = transaction[HoldingDetailField.Quantity.value]
    else:
        transaction[HoldingDetailField.OpenQuantity.value] = -transaction[HoldingDetailField.Quantity.value]

    position_deltas.append(transaction)


'''
Takes a list of transactions and create a list of dates 
where the positions have changed
'''
def create_position_deltas(transactions_df):
    position_deltas = pd.DataFrame()
    for transaction in transactions_df.iterrows():
        position_adjust(position_deltas, transaction[1])
    return position_deltas
    
