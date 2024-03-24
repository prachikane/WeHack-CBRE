import google.generativeai as genai
import streamlit as st
from dotenv import dotenv_values
from dbconn import send_sql_query
import re

# Load your API key from environment variables
env_vars = dotenv_values('.env')
results=[]
column_names=[]

#GET PROMPT
# Create a function to interact with the ChatGPT API
def chat_with_bot(prompt):
    genai.configure(api_key=env_vars.get('apikey'))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content('create a sql query for the statement ' + prompt)
    print(response)
    match = re.search(r'```sql\n(.*?)\n```', response.text)
    if match:
        sql=match.group(1)
        print("Sql query "+sql)
        global results
        global column_names
        results,column_names = send_sql_query(sql)
    else:
        print("no match found")
    #print(results)
    #print(column_names)
    return response.text,results,column_names

# select 10 rows from vendors
# Define the function to answer questions
def getAnswers(question):
    prompt = f"{question}"
    return prompt