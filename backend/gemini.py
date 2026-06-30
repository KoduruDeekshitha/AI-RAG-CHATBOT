import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model=genai.GenerativeModel("gemini-2.5-flash")
SYSTEM_PROMPT=""" you are DEEkshitha AI .
if the user wants to send an email, response only in json.
example:
{
_"tool":"send_email","receiver":"abc@gmail.com","subject":"Meeting","body":"Meeting tomorrow at 10 AM." }
 For normal question, reply normally.
 """
def generate_answer(prompt):
    response=model.generate_content(prompt)
    return response.text
