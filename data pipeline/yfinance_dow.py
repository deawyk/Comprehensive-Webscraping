#DOW 30
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#scrape dataframe from wikipedia
df = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')[1]
#grab tickers into a list
tickers = df.Symbol.to_list()


#Output stock info to csv with yfinance
tickerStrings = tickers
df_list = list()
for ticker in tickerStrings:
    data = yf.download(ticker, group_by="Ticker", period='5y')
    data['Ticker'] = ticker  #add column with ticker
    df_list.append(data)

#combine all dataframes into a single dataframe
df = pd.concat(df_list)

#save to csv
df.to_csv('ticker_dow.csv')

