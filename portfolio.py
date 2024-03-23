import pandas as pd
import yfinance as yf
investment = {'amount':100000}
portfolio = {}

def getInvest():
    return investment['amount']

def setInvest(val):
    investment['amount'] = val
def getPortfolio(): 
    # Create a DataFrame from the data
    for key in portfolio:
        portfolio[key]["Current Value"] = yf.Ticker(key).history(period="1d")["Close"][0]
    df = pd.DataFrame(portfolio)
    return df.T

def buy_stock(symbol, shares):
    stock_data = yf.Ticker(symbol)
    if symbol not in portfolio:
        portfolio[symbol] = {'Shares': 0, 'Average Price': 0.0, "Current Value": 0.0}
    current_shares = portfolio[symbol]['Shares']
    current_avg_price = portfolio[symbol]['Average Price']
    new_shares = current_shares + shares
    current_value = stock_data.history(period="1d")["Close"][0]
    new_avg_price = (
        (current_avg_price * current_shares + current_value * shares)
        / new_shares
    )
    portfolio[symbol]['Shares'] = new_shares
    portfolio[symbol]['Average Price'] = new_avg_price
    return current_value*shares

# Function to sell stocks
def sell_stock(symbol, shares):
    if symbol in portfolio and shares <= portfolio[symbol]['Shares']:
        stock_data = yf.Ticker(symbol)
        current_shares = portfolio[symbol]['Shares']
        current_avg_price = portfolio[symbol]['Average Price']
        current_value = stock_data.history(period="1d")["Close"][0]
        portfolio[symbol]['Shares'] = current_shares - shares
        portfolio[symbol]['Average Price'] = current_avg_price
        return current_value*shares


    