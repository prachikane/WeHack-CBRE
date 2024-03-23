import pandas as pd
import yfinance as yf
import prophet as Prophet

def predict_stock_price_with_sentiment(stock_symbol, sentiment_data_path):
    # Define the time period for historical data
    start_date = "2020-01-01"
    end_date = "2023-12-31"

    # Fetch historical stock price data using yfinance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Load news sentiment data (you need to prepare your own dataset)
    news_sentiment_data = pd.read_csv(sentiment_data_path)

    # Merge stock price and sentiment data based on timestamps
    merged_data = pd.merge(stock_data, news_sentiment_data, on="Date", how="inner")

    # Prepare a DataFrame for Prophet with sentiment data
    data = merged_data[['Date', 'Adj Close', 'SentimentScore']]
    data.rename(columns={'Date': 'ds', 'Adj Close': 'y', 'SentimentScore': 'addl_feature'}, inplace=True)

    # Create and fit a Prophet model with additional features
    model = Prophet()
    model.add_regressor('addl_feature')
    model.fit(data)

    # Create a DataFrame for future dates with sentiment features
    future = model.make_future_dataframe(periods=365)  # Predict for one year into the future

    # Include additional features for future dates
    # You need to obtain or estimate sentiment scores for future dates
    # future['addl_feature'] = ...

    # Make predictions
    forecast = model.predict(future)

    # Extract the forecasted values for the next year
    forecasted_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    return forecasted_data

# Example usage:
stock_symbol = "AAPL"  # Change this to your desired stock symbol
sentiment_data_path = "news_sentiment_data.csv"  # Change this to the path of your sentiment data file
predictions = predict_stock_price_with_sentiment(stock_symbol, sentiment_data_path)
print(predictions)
