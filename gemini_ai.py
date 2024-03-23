import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyDatXnmrygAM9k3ttUrycJI7IngeLLt1FQ")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)