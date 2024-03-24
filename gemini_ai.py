
import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyDatXnmrygAM9k3ttUrycJI7IngeLLt1FQ")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Generate a SQL Query to do the operation")
print(response.text)


