from dotenv import  load_dotend
import streamlit as st 
import os 
from google.generativeai import genai 

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_geminipro_response(question):
    response=chat.send_message(question,stream=True)
    return response 


## initilise our streamlit app

st.set_page_config(page_title="Q&A Demo")
st.header("Gemini Conversational Q&A App")


## initialise session state for the chat history if it doesn't exist

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

input=st.text_input("Input:",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=get_geminipro_response(input)
    st.session_state['chat_history'].append("You",input)
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append("Bot",chunk.text)

st.subheader("The Chat History is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")