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
df=[]
#df = pd.DataFrame()
#df.columns = location, 
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



# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### AGGREGATES')

# Define a column layout with appropriate widths and gap
col = st.columns((3, 3, 3), gap='medium')

# Display the header
with col[0]:
    count_value = df.shape[0]
    st.metric(label="Count", value=count_value)

if 'amount' in df.columns:
    with col[1]:
        sum_value = df['amount'].sum()
        st.metric(label="Sum", value=f"{sum_value:.2f}")
    with col[2]:
        avg_value = df['amount'].mean()
        st.metric(label="Average", value=f"{avg_value:.2f}")
else:
    with col[1]:
        sum_value = "N/A"
        st.metric(label="Sum", value=sum_value)
    with col[2]:
        avg_value = "N/A"
        st.metric(label="Average", value=avg_value)



import altair as alt
import plotly.express as px


def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale='Viridis',
                               range_color=(0, 100),
                               scope="usa",
                               labels={'count_per_state':'Assets'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth

# Define a column layout with appropriate widths and gap
col = st.columns((3, 3), gap='medium')

# Display the header for total population
with col[0]:
    st.markdown('#### Total Assets')
    
    df2 = df[['location', 'asset_id']]
    df2['state_code'] = df['location'].str.split(",").str[-1].str.strip().str.split().str[0]
    asset_counts = df2.groupby('state_code')['asset_id'].size().reset_index(name='count_per_state')
    df2 = df2.merge(asset_counts, on='state_code')

    
    # Create choropleth map for total population
    choropleth = make_choropleth(df2, 'state_code', 'count_per_state', 'Greens')
    st.plotly_chart(choropleth, use_container_width=True)
    

# Display the header for top states
with col[1]:
    st.markdown('#### Top States')

    st.dataframe(df,
                 hide_index=True,
                 width=None)




    
