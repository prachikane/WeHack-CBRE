import yfinance as yf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def predict_stock_price(stock_symbol):
    # Define the time period for historical data
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    # Fetch historical stock price data using yfinance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    
    # Extract the 'Adj Close' prices
    historical_prices = stock_data['Adj Close']
    
    # Create an ARIMA model
    model = ARIMA(historical_prices, order=(5,1,0))  # You can tune the order parameter
    
    # Fit the model to the historical data
    model_fit = model.fit()
    
    # Make predictions for the next 5 days
    forecasted = model_fit.forecast(steps=5)
    
    # Get the current stock details
    current_stock_data = yf.Ticker(stock_symbol)
    current_price = current_stock_data.history(period="1d")["Close"].values[0]
    
    # Calculate predicted prices for the next 5 days based on the forecast
    predicted_prices = [current_price] + list(forecasted)
    
    # Create a DataFrame to store the results
    date_range = pd.date_range(start=stock_data.index[-1] + pd.DateOffset(days=1), periods=6)
    predicted_df = pd.DataFrame({'Date': date_range, 'Predicted Price': predicted_prices})

    return predicted_df

# Example usage:
stock_symbol = "AAPL"  # Change this to your desired stock symbol
predicted_prices = predict_stock_price(stock_symbol)
print(predicted_prices)
