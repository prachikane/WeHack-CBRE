import streamlit as st
from datetime import date
import time
from plotly import graph_objs as go
import pandas as pd
import prompt as pr
import random as rand


st.set_page_config(page_title="GameStock",initial_sidebar_state="expanded")
tables = ['vendors', 'assets', 'invoices']
currTable = st.selectbox("Choose Table ", tables)
results=[]


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


START = "2022-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

message_container = st.empty()
#display_message(f"{str(currLevel*30)} mins = 1 day" , message_container)

col1, col2, col3 = st.columns(3)
with col1:
    st.title('CBRE')
with col3:
    progress_text = "Level "+str(currTable)
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
    amount.text("Investment Margin:$"+str('10000'))

st.subheader("Reports")
report_container=st.empty()


#Q&A
st.sidebar.title("ChatBot")
with st.sidebar:
    user_question = st.text_input("Ask your question:")
    if user_question:
        prompt = pr.getAnswers(user_question)
        response,results,column_names = pr.chat_with_bot(prompt)
        df = pd.DataFrame(results)
        df.columns=column_names
        report_container.table(df)
        with st.chat_message("user"):
            st.markdown(user_question)
        with st.chat_message("assistant"):
            st.markdown(response)