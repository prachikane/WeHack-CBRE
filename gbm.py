import numpy as np
import pandas as pd
import yfinance as yf

def predict_stock_prices(stock_symbol, start_date, end_date):
    # Define parameters for GBM
    mu = 0.1  # Drift (average rate of return)
    sigma = 0.2  # Volatility (standard deviation)
    S0 = 100  # Initial stock price
    T = 5  # Time period in days
    N = 5  # Number of days for prediction
    dt = T / N  # Time step

    # Fetch historical stock price data using yfinance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Calculate the daily returns from historical data
    stock_data['Returns'] = stock_data['Adj Close'].pct_change().dropna()

    # Calculate the mean and standard deviation of daily returns
    mean_return = stock_data['Returns'].mean()
    std_return = stock_data['Returns'].std()

    # Generate daily returns using GBM
    np.random.seed(42)
    daily_returns = np.random.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), N)

    # Calculate predicted stock prices for the next 5 days based on GBM
    predicted_prices = [S0]
    for i in range(N):
        S_t = predicted_prices[-1]
        S_t_plus_1 = S_t * (1 + mu * dt + sigma * np.sqrt(dt) * daily_returns[i])
        predicted_prices.append(S_t_plus_1)

    # Create a DataFrame to store the results
    date_range = pd.date_range(start=stock_data.index[-1] + pd.DateOffset(days=1), periods=N)
    predicted_df = pd.DataFrame({'Date': date_range, 'Predicted Price': predicted_prices[1:]})

    return predicted_df

# Example usage:
stock_symbol = "META"  # Change this to your desired stock symbol
start_date = "2023-01-01"
end_date = "2023-12-31"
predicted_prices = predict_stock_prices(stock_symbol, start_date, end_date)
print(predicted_prices)
