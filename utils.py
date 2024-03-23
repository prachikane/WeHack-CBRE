import yfinance as yf
from datetime import date
def load_data(stock, stocks):
    START = "2022-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    data = yf.download(stocks[stock], START, TODAY)
    data.reset_index(inplace=True)
    return data

def load_fast_info(stock, stocks):
    data = yf.Ticker(stocks[stock])
    data = data.get_fast_info()
    # Create a table to display stock metrics
    data_table = {elem:data.get(elem) for elem in data}
    return data_table 

def metrics_detail(content):
    data_dict = {
    "currency": "The type of money in which the item's price is expressed, often using three-letter codes like USD for US Dollars.",
    "dayHigh": "The highest price at which the item was traded during a single trading day.",
    "dayLow": "The lowest price at which the item was traded during a single trading day.",
    "exchange": "The specific place or platform where the item is bought and sold, like a stock exchange or a cryptocurrency exchange.",
    "fiftyDayAverage": "The average price of the item over the past 50 trading days, which can help identify trends.",
    "lastPrice": "The most recent price at which the item was bought or sold in the most recent transaction.",
    "lastVolume": "The number of units of the item bought or sold in the last transaction, indicating trading activity.",
    "marketCap": "The total value of all units of the item in circulation, calculated by multiplying the item's price by the total number of units.",
    "open": "The price at which the item started trading at the beginning of the trading day.",
    "previousClose": "The price at which the item ended trading on the previous trading day, providing a reference point for comparison.",
    "quoteType": "The category or type of the financial item, such as stocks, bonds, or commodities.",
    "regularMarketPreviousClose": "The last price of the item when the market closed during regular trading hours.",
    "shares": "The total number of units or shares of this item available for trading.",
    "tenDayAverageVolume": "The average number of units of the item bought or sold over the past ten trading days, indicating recent trading activity.",
    "threeMonthAverageVolume": "The average number of units of the item bought or sold over the past three months, giving a broader perspective on trading activity.",
    "timezone": "The time zone in which the market where the item is traded is located, affecting trading hours and timestamps.",
    "twoHundredDayAverage": "The average price of the item over the past 200 trading days, providing a longer-term perspective on price trends.",
    "yearChange": "How much the item's price has changed in the past year, often expressed as a percentage.",
    "yearHigh": "The highest price the item has reached in the past year, indicating its peak value during that period.",
    "yearLow": "The lowest price the item has reached in the past year, showing its minimum value during that period."
    }

    return data_dict[content]
