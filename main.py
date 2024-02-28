import streamlit as st
import os
import google.generativeai as genai
from docx import Document

# Initialize Gemini-Pro 
genai.configure(api_key="AIzaSyAUapxNs5faAro8S-GyhypH5p_m3rJZVp0")
model = genai.GenerativeModel('gemini-pro')

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

def extract_text_from_docx():
    doc = Document("./file.docx")
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    extra_knowledge = extract_text_from_docx()
    st.session_state.chat = model.start_chat(history = [])
    response = st.session_state.chat.send_message(f"This is some knowledge i provide you initally, i want you to answere quetions that user aks from this knowledge, if the question is related to this knowledge that i provide you should should create a marketing strategy plan for that product based on this knowledge and keeping in mind the princple this knowledge base provides you, for now just reply you got me if you get me. KNOWLEDGE:{extra_knowledge}")  


# Display Form Title
st.title("Advizer AI")

# Display chat messages from history above current input box
for message in st.session_state.chat.history[2:]:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

st.chat_message("assistant").markdown("Hello! I am Advizer AI.")
st.chat_message("assistant").markdown("What is the name of the product you want to create a marketing strategy for? Cost of Marketing? And the country you want to market it in?")

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("I possess a well of knowledge. What would you like to know?"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)
    
    # Send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(prompt) 
    
    # Display last 
    with st.chat_message("assistant"):
        st.markdown(response.text)