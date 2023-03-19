from pandas_datareader import data as pdr

import yfinance as yf

yf.pdr_override()  # <== that's all it takes :-)

# download dataframe
data = pdr.get_data_yahoo("SPY", start="2000-01-01", end="2022-01-01")

print(len(data))
data.to_csv("spy.csv", index=False)
