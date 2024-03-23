import streamlit as st
from datetime import date
import portfolio as pf
import time
import utils as ut
from plotly import graph_objs as go
import pie
import pandas as pd
import prompt as pr
import random as rand
import newssentiment as ns
st.set_page_config(page_title="GameStock",initial_sidebar_state="collapsed")
Level = [1, 2, 3, 4, 5]
currLevel = st.selectbox("Choose Level ", Level)
investment = pf.getInvest()
def display_message(message, message_container):
	    # Create the message-shaped background with text
        message_container.write('<div class="message">'+message+'</div>', unsafe_allow_html=True)
        time.sleep(3)
        message_container.empty()
#styles
style = """
	<style>
	.message {
		background-color: #f5f5f5; /* Off-white background color */
		padding: 10px;
		border: 2px solid #000; /* Black border */
		border-radius: 10px;
		font-weight: bold; /* Bold text */
		color: #000; /* Black text color */
	}
	</style>
	"""
	# Apply the CSS style
st.write(style, unsafe_allow_html=True)
#
START = "2022-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

message_container = st.empty()
display_message(f"{str(currLevel*30)} mins = 1 day" , message_container)
col1, col2, col3 = st.columns(3)
with col1:
    st.title('GameStock')
with col3:
    progress_text = "Level "+str(currLevel)
    my_bar = st.progress(rand.randint(30,80), text=progress_text)
    with open("TradeReport.pdf", "rb") as file:
        btn = st.download_button(
            label="Download Progress Report",
            data=file,
            file_name="TradeReport.pdf"
          )
col1, col2 = st.columns([1,2])
with col1:
    amount = st.empty()
    amount.text("Investment Margin:$"+str(investment))
st.subheader("Portfolio")
portfolio_container = st.empty()
portfolio_container.table(pf.getPortfolio())
stocks={}
if currLevel == 1:
    stocks = {"Google":'GOOG', "Apple":'AAPL', "Microsoft":'MSFT', "Amazon":'AMZN'}
elif currLevel == 2:
    stocks = {
    "Google": 'GOOG',
    "Apple": 'AAPL',
    "Microsoft": 'MSFT',
    "Amazon": 'AMZN',
    "Facebook": 'META',
    "Tesla": 'TSLA',
    "Netflix": 'NFLX'
}
elif currLevel == 3:
    stocks = {
    "Google": 'GOOG',
    "Apple": 'AAPL',
    "Microsoft": 'MSFT',
    "Amazon": 'AMZN',
    "Facebook": 'META',
    "Tesla": 'TSLA',
    "Netflix": 'NFLX',
    "Alphabet": 'GOOGL',
    "Visa": 'V',
    "JP Morgan Chase": 'JPM',
    "Walmart": 'WMT'
}

else:
     stocks = {
    "Google": 'GOOG',
    "Apple": 'AAPL',
    "Microsoft": 'MSFT',
    "Amazon": 'AMZN',
    "FaceBook": 'META',
    "Tesla": 'TSLA',
    "Netflix": 'NFLX',
    "Alphabet": 'GOOGL',
    "Visa": 'V',
    "JP Morgan Chase": 'JPM',
    "Walmart": 'WMT',
    "Johnson & Johnson": 'JNJ',
    "Procter & Gamble": 'PG',
    "Abbott Laboratories": 'ABT',
    "Ford": 'F'
}




metrics_data = None
col1, col2 = st.columns([1, 2])
with col1:
    selected_stock = st.selectbox('Choose stock', stocks.keys())
    #Display a message 
    if currLevel==1:
        st.info('The horizontal (x-axis) typically represents time, with the most recent data on the right and older data on the left. The vertical (y-axis) represents the stock price or another relevant metric, such as volume or a technical indicator. Identify the Stock Symbol and Timeframe:Ensure you know which stock you are analyzing and the chosen timeframe (e.g., daily, weekly, monthly). Analyze the Price Movement: Look at the overall direction of the stocks price movement.',icon='🤖' )   
    message_container = st.empty()
    if currLevel==2:
        metrics_message = st.empty()
    if currLevel >= 3:
         pie.setPie(st)

# Plot raw data
def plot_raw_data(data):
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Performace Chart of '+selected_stock, xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)

with col2:
    data = ut.load_data(selected_stock, stocks)
    plot_raw_data(data)
    if currLevel == 3:
        sectorMessageContainer = st.info("Sector-wise performance analysis is a crucial aspect of stock profitability assessment, with investors using it to gauge economic prospects. Top-down and sector rotation approaches are common strategies, with the former emphasizing macroeconomic conditions in the search for outperforming companies. Continuous monitoring of major sector trends, involving market capitalization changes and the count of advancing and declining stocks, allows investors to identify promising sectors for investment based on varying economic conditions and investment periods.", icon='🤖')
    if currLevel >=4:
     newsData = ns.get_mean_sentiment_score(stocks[selected_stock])
     col1, col2, col3, col4 = st.columns(4)
     col1.markdown("News Analytics")
     col2.metric("Mean sentiment score", "", newsData[0])
     col3.metric(newsData[1][0], "", newsData[1][1])
     col4.metric(newsData[2][0],"" , newsData[2][1])

    
if currLevel >= 2:
    st.subheader("Stock Metrics")
    data_table = ut.load_fast_info(selected_stock, stocks)
    st.table(data_table)
    metrics_data = data_table
if currLevel == 2:
    for tab in st.tabs(metrics_data.keys()):
         with tab:
               content = int(str(tab).split("RunningCursor(_parent_path=(10, ")[1].split(")")[0])
               st.info(ut.metrics_detail(list(metrics_data.keys())[content]), icon="🤖")
            

action = st.selectbox("Action", ["Buy", "Sell"])
symbol = st.text(selected_stock)
shares = st.number_input("Shares", min_value=1)

# Perform the action
if st.button("Execute"):
    if action == "Buy":
        investment -=pf.buy_stock(stocks[selected_stock], shares)
        pf.setInvest(investment)
        amount.text("Investment:$"+str(investment))
        with st.spinner('Wait for it...'):
            portfolio_container.table(pf.getPortfolio())
            time.sleep(5)
        
    elif action == "Sell":
        investment += pf.sell_stock(stocks[selected_stock], shares)
        pf.setInvest(investment)
        amount.text("Investment:$"+str(investment))
        with st.spinner('Wait for it...'):
            portfolio_container.table(pf.getPortfolio())
            time.sleep(5)

#Q&A
with st.sidebar:
    user_question = st.text_input("Ask your question:")
    if user_question:
        prompt = pr.getAnswers(user_question)
        response = pr.chat_with_bot(prompt)
        with st.chat_message("user"):
             st.markdown(user_question)
        with st.chat_message("assistant"):
             st.markdown(response)

