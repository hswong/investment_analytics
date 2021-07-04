from enum import Enum

'''
The following are standardized labels used for the dataframes being analyzed so that it is easier to maintain the codebase.
'''
class AssetIdentifier(Enum):
    ISIN = "isin"
    VALOREN = "valoren"
    Symbol = "symbol"
    Identifier = "identifier" # identifier for this asset
    Name = "name"

class TransactionType(Enum):
    Buy = "buy"
    Sell = "sell"
    Split = "split"

class TransactionDetails(Enum):
    UserID = "user id"
    Asset = "asset" # (AssetIdentifier)
    TransactionDate = "transaction_date" #(Date)
    TradeDateTime = "trade datetime" #(Datetime)
    Quantity = "quantity"
    TransactionType = "transaction_type" #(TransactionType)
    CostPrice = "cost price"
    Reference1 = "reference1" # Order ID or other FI reference

    
class HoldingDetailField(Enum):
    Quantity = "quantity"
    Asset = "Asset" # (AssetIdentifier)
    AdjustedCostPerUnit = "adjusted cost per unit"
    TotalGrossCostBasis = "total gross cost" # Total Gross Cost (excludes fees & charges)
    TotalNetCostBasis = "total net cross" # Total Net Cost (includes fees & charges)
    TradeDateTime = "trade datetime"
    TradeDate = "trade_date" #(Date)


'''
This class holds all the details related to a valued holding. Some holdings may not be valued and in those cases we use HoldingDetailField instead

'''
class ValuedHoldingDetailsField(Enum):
    MarketPrice = "market price"
    ValuationDate = "valuation date" #(Date)
    Valuation = "valuation" #(Amount)
