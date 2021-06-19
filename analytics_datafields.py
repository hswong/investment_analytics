from enum import Enum

class AssetIdentifier(Enum):
    ISIN = "isin"
    Symbol = "symbol"
    Name = "name"

class TransactionType(Enum):
    
class TransactionDetails(Enum):
    Asset = "Asset" # (AssetIdentifier)
    TradeDate = "trade_date" #(Date)
    TradeDateTime = "trade_date_time" #(Datetime)
    Quantity = "quantity"
    TransactionType = "transaction_type" #(TransactionType)
    
class HoldingDetails(Enum):
    Quantity = "quantity"

