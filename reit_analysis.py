# Load in 
import pandas as pd
from pandas import DataFrame
from tabulate import tabulate
import matplotlib.pyplot as plt

def price_div_ratio(price, ratio):
    return price/ratio


# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
div_data = pd.read_csv("data/A17U.SI_div.csv") 
price_data = pd.read_csv("data/A17U.SI.csv") 

#print(price_data.head)

div_data.Date = pd.to_datetime(div_data.Date, format = '%Y-%m-%d')
per = div_data['Date'].dt.to_period("Y") 
# convert amounts to floats
div_data['Dividends'] = pd.to_numeric(div_data['Dividends'])

div_data.index = div_data['Date']
div_data = div_data.drop('Date', axis=1)

# resample the dataframe every 1 day (D) and sum ovr each day
div_data = div_data.resample('Y').sum()
div_data["year"] = pd.DatetimeIndex(div_data.index).year

# Transform the Price data to find min and max per year
price_data.Date = pd.to_datetime(price_data.Date, format = '%Y-%m-%d')

price_data['Close'] = pd.to_numeric(price_data['Close'])

#price_data.index = price_data.Date
#price_data = price_data.drop('Date', axis=1)

# resample the dataframe every 1 day (D) and sum ovr each day
#map={'min_close':min, 'max_close':max}
#for key,value in map.items():
#    print(key,value)
#    price_data[key]=price_data.groupby(price_data.Date.dt.year)['Close'].transform(func=value)

#price_data = price_data.resample('Y')
price_data['year'] = pd.DatetimeIndex(price_data['Date']).year
price_data['min_close'] = price_data['Close'].groupby(price_data.year).transform('min')
price_data['max_close'] = price_data['Close'].groupby(price_data.year).transform('max')
price_data['min_close'] = pd.to_numeric(price_data['min_close'])
price_data['max_close'] = pd.to_numeric(price_data['max_close'])
price_data['dividend'] = div_data['Dividends']

selected_columns = price_data[["year","min_close", "max_close"]]
price_data_final = selected_columns.copy()
#price_data_final.index = price_data.year
price_data_final.drop('year', axis=1)
price_data_final = price_data_final.drop_duplicates()

print(tabulate(div_data, headers = 'keys', tablefmt = 'psql'))
print(tabulate(price_data_final, headers = 'keys', tablefmt = 'psql'))

df = price_data_final.merge(div_data)

df['max_div_yield'] = df.apply(lambda row : price_div_ratio(row['Dividends'], row['min_close']), axis = 1)
df['min_div_yield'] = df.apply(lambda row : price_div_ratio(row['Dividends'], row['max_close']), axis = 1)
print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

df.to_csv(r'A17.SI_dividend_yield.csv', index = False)

plt.close()
df = df.cumsum()
plt.figure()
df.plot()
    
#print(tabulate(gb, headers = 'keys', tablefmt = 'psql'))