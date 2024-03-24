import google.generativeai as genai
import streamlit as st
from dotenv import dotenv_values
from dbconn import send_sql_query
import re

# Load your API key from environment variables
env_vars = dotenv_values('.env')
results=[]
column_names=[]
data =[]
#GET PROMPT
# Create a function to interact with the ChatGPT API
def chat_with_bot(prompt):
    genai.configure(api_key=env_vars.get('apikey'))
    model = genai.GenerativeModel('gemini-pro')

    with open("db_schema.txt", "r") as file:
        # Read the content
        global data
        data = file.read()
    query_prompt='suppose you are given this scehma\n '+ data +'\n create a sqlite query for the statement ' + prompt +' and write the query in a single line without the use of new lines in between the query \n include primary column for all queries'
    print(query_prompt)
    response = model.generate_content(query_prompt)
    print(response)
    patterns = [
        r"```sql(.*?)```",
        r"```sql\n(.*?)\n```",
        r"```\n(.*?)\n```",
        r"```(.*?)```",
        r"``(.*?)``",
        r"`(.*?)`",
        r"(.*?)"
    ]
    for pattern in patterns:
        match = re.search(pattern, response.text)
        if match:
            break

    if match:
        sql=match.group(1)
        print("Sql query "+sql)
        global results
        global column_names
        results,column_names = send_sql_query(sql)
    else:
        results,column_names = send_sql_query(response.text)
    #print(results)
    #print(column_names)
    return response.text,results,column_names

# select 10 rows from vendors
# Define the function to answer questions
def getAnswers(question):
    prompt = f"{question}"
    return prompt