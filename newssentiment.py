##FINAL FUNCTION


import requests
import pandas as pd
# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'VHHZUBY5JU3VSJYZ'
def get_mean_sentiment_score(tickers):
    # Define the constant parameters
    function = 'NEWS_SENTIMENT'
    topics = 'technology,ipo'
    time_from = '20220410T0130'
    sort = 'RELEVANCE'
    limit = 10

    # Construct the API request URL
    url = f'https://www.alphavantage.co/query?function={function}&tickers={tickers}&topics={topics}&time_from={time_from}&sort={sort}&limit={limit}&apikey={api_key}'

    # Send the API request
    r = requests.get(url)

    # Check if the request was successful
    if r.status_code == 200:
        # Parse the JSON response
        data = r.json()
        print(data) 
        # Create a DataFrame
        df = pd.DataFrame(data)
        
        
        # Explode the 'feed' column into individual rows
        df = pd.json_normalize(df['feed'])
        df1 = df[['summary','overall_sentiment_score']]
        df1  = df1.sort_values(by='overall_sentiment_score', ascending=False)
        summary1, overallscore1 = df1.iloc[0]
        summary2, overallscore2 = df1.iloc[-1]
        # Calculate the mean sentiment score
        mean_sentiment_score = df["overall_sentiment_score"].mean()

        return mean_sentiment_score,(summary1, overallscore1),(summary2, overallscore2)
    else:
        return None  # Return None in case of an error
