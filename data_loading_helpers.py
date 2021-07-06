from analytics_datafields import *
import pandas as pd
import re
import math
'''
Renames the columns of the dataset into a standardised format
'''
def load_mapper_orovault(transactions_df):
    transactions_df.rename(columns={
        'Transaction Date':TransactionDetails.TransactionDate.value,
        'Transaction Type':TransactionDetails.TransactionType.value,
        'Amount/Qty':TransactionDetails.Quantity.value,
        'ISIN': AssetIdentifier.ISIN.value,
        'Valoren': AssetIdentifier.VALOREN.value
        }, errors='raise', inplace=True)

def __determine_quantity_type__(quantity):
    if type(quantity) == float and math.isnan(quantity):
        return quantity
    if quantity.startswith('FW.oz'):
        return QuantityType.Ounce
    if re.match("^[A-Z]{3}",quantity):
        # Currency Type
        return QuantityType.Nominal.value
    return QuantityType.Share.value

def __extract_quantity__(quantity):
    if type(quantity) == float and math.isnan(quantity):
        return quantity
    if quantity.startswith('FW.oz'):
        return quantity[5:].lstrip()
    if re.match("^[A-Z]{3}",quantity):
        # Currency Type
        return quantity[3:].lstrip()
    return quantity

'''
Set the correct data types for analytics 
'''
def post_load_processing(transactions_df):
    transactions_df[TransactionDetails.TransactionDate.value] = pd.to_datetime(transactions_df[TransactionDetails.TransactionDate.value])
    transactions_df[TransactionDetails.QuantityType.value] = transactions_df[TransactionDetails.Quantity.value].map(__determine_quantity_type__)
    transactions_df[TransactionDetails.Quantity.value] = transactions_df[TransactionDetails.Quantity.value].map(__extract_quantity__)
    transactions_df[TransactionDetails.Quantity.value] = transactions_df[TransactionDetails.Quantity.value].str.replace(',', '').astype(float)
    transactions_df[TransactionDetails.Quantity.value] = pd.to_numeric(transactions_df[TransactionDetails.Quantity.value])

    transactions_df.sort_values(by=TransactionDetails.TransactionDate.value, inplace=True)

def enrich(transactions_df):
    transactions_df[AssetIdentifier.VALOREN.value] = transactions_df[AssetIdentifier.VALOREN.value].str.lstrip('0')
    transactions_df[AssetIdentifier.Identifier.value] = transactions_df[AssetIdentifier.ISIN.value]
    transactions_df[AssetIdentifier.Identifier.value] = transactions_df[AssetIdentifier.Identifier.value].\
        fillna(transactions_df[AssetIdentifier.VALOREN.value])
    transactions_df[AssetIdentifier.Identifier.value] = transactions_df[AssetIdentifier.Identifier.value].\
        combine_first(transactions_df[AssetIdentifier.VALOREN.value])

