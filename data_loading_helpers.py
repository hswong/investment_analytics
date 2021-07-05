from analytics_datafields import *
import pandas as pd

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

'''
Set the correct data types for analytics 
'''
def post_load_processing(transactions_df):
    transactions_df[TransactionDetails.TransactionDate.value] = pd.to_datetime(transactions_df[TransactionDetails.TransactionDate.value])
    transactions_df.sort_values(by=TransactionDetails.TransactionDate.value, inplace=True)

def enrich(transactions_df):
    transactions_df[AssetIdentifier.VALOREN.value] = transactions_df[AssetIdentifier.VALOREN.value].str.lstrip('0')
    transactions_df[AssetIdentifier.Identifier.value] = transactions_df[AssetIdentifier.ISIN.value]
    transactions_df[AssetIdentifier.Identifier.value] = transactions_df[AssetIdentifier.Identifier.value].\
        fillna(transactions_df[AssetIdentifier.VALOREN.value])
    transactions_df[AssetIdentifier.Identifier.value] = transactions_df[AssetIdentifier.Identifier.value].\
        combine_first(transactions_df[AssetIdentifier.VALOREN.value])

