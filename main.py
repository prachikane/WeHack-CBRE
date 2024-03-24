import streamlit as st
from datetime import date
import time
from plotly import graph_objs as go
import pandas as pd
import prompt as pr
import random as rand
import altair as alt
import plotly.express as px


st.set_page_config(page_title="CBRE Dashboard",initial_sidebar_state="expanded")

results=[]
ans=""
df = pd.DataFrame()
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

col1, col2 = st.columns(2)
with col1:
    st.title('CBRE')
with col2:
    with open("TradeReport.pdf", "rb") as file:
        btn = st.download_button(
            label="Download Progress Report",
            data=file,
            file_name="TradeReport.pdf"
          )
col1, col2 = st.columns([1,2])
with col1:
    amount = st.empty()

st.subheader("Reports")
report_container=st.empty()


#Q&A
st.sidebar.title("ChatBot")
with st.sidebar:
    user_question = st.text_input("Ask your question:")
    if user_question:
        prompt = pr.getAnswers(user_question)
        response,results,column_names = pr.chat_with_bot(prompt)
        if len(results)>0:
            df = pd.DataFrame(results)
            df.columns=column_names
            print(df)
        else:
            ans="no results found"
        #report_container.table(df)
        with st.chat_message("user"):
            st.markdown(user_question)
        with st.chat_message("assistant"):
            st.markdown(response)



# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Aggregates')

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



def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, df2[input_column].max()),
                               scope="usa",
                               labels={'count_per_state':'Assets'}
                              )
    
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor=f'rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=300
    )
    return choropleth

# Define a column layout with appropriate widths and gap
col = st.columns(1)

# Display the header for total population
if 'location' in df.columns and 'asset_id' in df.columns:
    with col[0]:
        st.markdown('#### Total Assets')
        
        df2 = df[['location', 'asset_id']]
        df2['state_code'] = df['location'].str.split(",").str[-1].str.strip().str.split().str[0]
        asset_counts = df2.groupby('state_code')['asset_id'].size().reset_index(name='count_per_state')
        df2 = df2.merge(asset_counts, on='state_code')

        
        # Create choropleth map for total population
        choropleth = make_choropleth(df2, 'state_code', 'count_per_state', 'greens')
        st.plotly_chart(choropleth, use_container_width=True)
            

    # Display the header for top states
    with col[0]:
        st.markdown('#### Top Assets')

        st.dataframe(df,
                    hide_index=True,
                    width=None)
elif 'invoice_id' and 'amount' in df.columns:
    with col[0]:
        fig = px.line(df, x='invoice_date', y='amount', title='Bar Graph')
        st.plotly_chart(fig)
    
    with col[0]:
        st.markdown('Display Table')

        st.dataframe(df,hide_index=True,width=None)
   

elif 'vendor_id' in df.columns:
    with col[0]:
        st.markdown('Vendors Table')

        #x_column = df.columns[0]
        #y_column = df.columns[1]

        fig = px.bar(df, x='vendor_id', y='total_cost', labels={'Amount': 'Total Costs ($)'},title='Total Costs by Vendor ')
        fig.update_xaxes(title='Vendor Id')
        fig.update_yaxes(title='Cost')
        fig.update_layout(xaxis=dict(type='category'))  
        st.plotly_chart(fig, use_container_width=True)
    with col[0]:
        st.markdown('Display Table')

        st.dataframe(df,hide_index=True,width=None)

else:
    st.markdown('Run a query to display statistics')
    
    

        












        