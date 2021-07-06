from numpy.core.numeric import normalize_axis_tuple
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import yfinance as yf
import pandas_market_calendars as mcal
import csv
import math
from analytics_datafields import *


credit_transaction_types = [
    TransactionType.Buy.value
]

debit_transaction_types = [
    TransactionType.Sell.value
]

def position_adjust(position_deltas, transaction):
    identifier = transaction[AssetIdentifier.Identifier.value]

    print (str(transaction[HoldingDetailField.Quantity.value]))
    if math.isnan(transaction[HoldingDetailField.Quantity.value]):
        # Ignore since we do not know what the quantity is
        return

    if transaction[TransactionDetails.TransactionType.value].lower() in debit_transaction_types:
        transaction_type = 'debit'
        print (transaction[HoldingDetailField.Quantity.value])
        remaining_quantity = -transaction[HoldingDetailField.Quantity.value].to_numeric()
    elif transaction[TransactionDetails.TransactionType.value].lower() in credit_transaction_types:
        transaction_type = 'credit'
        print (transaction[HoldingDetailField.Quantity.value])
        remaining_quantity = transaction[HoldingDetailField.Quantity.value].to_numeric()
    else:
        print('Not yet configured transaction type:'+transaction[TransactionDetails.TransactionType.value].lower())
        return
#        raise TypeError('Not yet configured transaction type:'+transaction[TransactionDetails.TransactionType.value].lower())

    if position_deltas.size:
        positions_same_security = position_deltas[position_deltas[AssetIdentifier.Identifier.value] == identifier]
        for position in positions_same_security:
            if remaining_quantity > 0 and position[1][HoldingDetailField.OpenQuantity.value] < 0:
                quantity_to_close = remaining_quantity if abs(position[1][HoldingDetailField.OpenQuantity.value]) > remaining_quantity\
                    else -position[1][HoldingDetailField.OpenQuantity.value]
                remaining_quantity = remaining_quantity - quantity_to_close
            elif remaining_quantity < 0 and position[1][HoldingDetailField.OpenQuantity.value] > 0:
                quantity_to_close = remaining_quantity if position[1][HoldingDetailField.OpenQuantity.value] > abs(remaining_quantity)\
                    else position[1][HoldingDetailField.OpenQuantity.value]
                remaining_quantity = remaining_quantity + quantity_to_close

    if remaining_quantity: # Leftover quantity so let's add a new position record
        transaction[HoldingDetailField.OpenQuantity.value] = transaction[HoldingDetailField.Quantity.value]
        position_deltas.append(transaction)
    else:
        transaction[HoldingDetailField.OpenQuantity.value] = 0-transaction[HoldingDetailField.Quantity.value]


'''
Takes a list of transactions and create a list of dates 
where the positions have changed
'''
def create_position_deltas(transactions_df):
    position_deltas = pd.DataFrame()
    for transaction in transactions_df.iterrows():
        position_adjust(position_deltas, transaction[1])
    return position_deltas
    
