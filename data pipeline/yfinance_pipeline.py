#Function
import yfinance as yf
import pandas as pd

def stock_info_to_csv (tickerStrings, file_name):
    df_list = list()
    for ticker in tickerStrings:
        data = yf.download(ticker, group_by="Ticker", period='5y')
        data['Ticker'] = ticker  #add column with ticker
        df_list.append(data)
        
    #combine all dataframes into a single dataframe
    df = pd.concat(df_list)
    
    #save to csv
    df.to_csv(file_name)

    
#Comprehensive webscrape of U.S. News-Stocks Under $10 with Selenium
from selenium import webdriver
import collections
from bs4 import BeautifulSoup as soup
import re

#download chromedriver
d = webdriver.Chrome('/Users/owner/chromedriver')
d.get('https://money.usnews.com/investing/stocks/stocks-under-10')
s = soup(d.page_source, 'lxml')
while True:
  try:
    d.find_element_by_link_text("Load More").click() #get all data
  except:
    break
company = collections.namedtuple('company', ['name', 'abbreviation', 'description', 'stats'])
headers = [['a', {'class':'search-result-link'}], 
           ['a', {'class':'text-muted'}], 
           ['p', {'class':'text-small show-for-medium-up ellipsis'}], 
           ['dl', {'class':'inline-dl'}], 
           ['span', {'class':'stock-trend'}], 
           ['div', {'class':'flex-row'}]]

#formatting in reference to page source code
final_data = [[getattr(i.find(a, b), 'text', None) for a, b in headers] 
              for i in soup(d.page_source, 'html.parser').find_all('div', {'class':'search-result flex-row'})]

new_data = [[i[0], i[1], re.sub('\n+\s{2,}', '', i[2]), 
             [re.findall('[\$\w\.%/]+', d) for d in i[3:]]] for i in final_data]

final_results = [i[:3]+[dict(zip(['Price', 'Daily Change', 'Percent Change'], 
                                 filter(lambda x:re.findall('\d', x), i[-1][0])))] for i in new_data]

#all info iterated by company into list
new_results = [company(*i) for i in final_results]

#grab tickers into a list
abbrevs = [i.abbreviation for i in new_results]

#Output stock info to csv with yfinance
stock_info_to_csv(abbrevs, 'ticker_under10.csv')


#Webscraping Yahoo! Finance-Most Active Stocks with Beautiful Soup
from bs4 import BeautifulSoup
import requests

url = 'https://finance.yahoo.com/most-active'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
         }
response = requests.get(url, headers=header)
soup = BeautifulSoup(response.content, 'lxml')

#iterate over dataframe and append tickers to list
symbols = list()
for item in soup.select('.simpTblRow'):
    symbols.append(item.select('[aria-label=Symbol]')[0].get_text())

#Output stock info to csv with yfinance
stock_info_to_csv(symbols, 'ticker_active.csv')


#DOW 30 dataframe from wikipedia
df = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')[1]
#grab tickers into a list
tickers = df.Symbol.to_list()

#Output stock info to csv with yfinance
stock_info_to_csv(tickers, 'ticker_dow.csv')


