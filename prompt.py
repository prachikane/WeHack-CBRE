import google.generativeai as genai
import streamlit as st

# Load your API key from environment variables
apikey = "AIzaSyDatXnmrygAM9k3ttUrycJI7IngeLLt1FQ"


#GET PROMPT
# Create a function to interact with the ChatGPT API
def chat_with_bot(prompt):
    genai.configure(api_key=apikey)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    print(response.text)
    return response.text
    #   response = openai.Completion.create(S
     #       engine="text-davinci-002",
      #      prompt=prompt,
       #     max_tokens=50,  # Adjust as needed
        #)
    #return response.choices[0].text

# Create a function to get the prompt
def getPrompt(param):
    prompt = f"{param}"
    response = chat_with_bot(prompt)
    return response


# Define the function to answer questions
def getAnswers(question):
    prompt = f"{question}"
    return prompt

# # Initialize variables
# conversation = []  # Store the conversation history

# # Streamlit application

# # Input field for user questions
# user_question = st.text_input("Ask your question:")

# # Generate a prompt using getAnswers
# prompt = getAnswers(user_question)

# # Send the prompt to the chatbot and get the response
# response = chat_with_bot(prompt)

# # Add the conversation turn to the history
# conversation.append({"user": user_question, "bot": response})

# # Display the conversation
# for turn in conversation:
#     st.markdown(f"{turn['user']} > {turn['bot']}")

# # Clear the input field after each question
# st.empty()





#Yoy interpretation

#Understand the Axes:

#The horizontal (x-axis) typically represents time, with the most recent data on the right and older data on the left. The vertical (y-axis) represents the stock's price or another relevant metric, such as volume or a technical indicator. Identify the Stock Symbol and Timeframe:

#Ensure you know which stock you are analyzing and the chosen timeframe (e.g., daily, weekly, monthly). Analyze the Price Movement:

#Look at the overall direction of the stock's price movement. Is it trending up (bullish), down (bearish), or trading sideways? Pay attention to key price levels, such as support and resistance, which are levels at which the stock tends to bounce or reverse. Use Technical Indicators:

#If available on the graph, consider the use of technical indicators like moving averages, Relative Strength Index (RSI), or Moving Average Convergence Divergence (MACD) to get a more comprehensive view of the stock's trend and momentum. Volume Analysis:

#Analyze the volume bars or line on the graph to see if there are any notable spikes in trading volume. Higher volume often accompanies significant price moves and can indicate the strength of a trend. Chart Patterns:

#Look for chart patterns like head and shoulders, double tops, double bottoms, flags, or pennants. These patterns can suggest potential trend reversals or continuations. Divergences:

#Examine the relationship between price and technical indicators. Divergences, where the stock price moves in the opposite direction of an indicator, can be a signal of a potential trend change. Trendlines:

#Draw trendlines to help visualize the stock's trend direction. Uptrends have higher lows and higher highs, while downtrends have lower highs and lower lows.




#Industry Sector graph 

#To interpret an industry sector graph for investment decisions:

#Identify Trends: Look for sector trends; a rising sector may indicate investment opportunities.

#Compare to Benchmarks: Compare sector performance to broader market indices for relative strength.

#Fundamentals: Consider industry-specific factors and company financials when making decisions.

#Diversify: Diversify across sectors to manage risk and optimize your portfolio.

#Remember, sector analysis is just one part of a diversified investment strategy.
