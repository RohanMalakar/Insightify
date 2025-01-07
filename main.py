import requests
import json
import streamlit as st
from dotenv import load_dotenv
import os
import pyperclip

# Load environment variables
load_dotenv()
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")

ENDPOINT = "analysis"
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a429dc71-ad2c-4b98-b5b3-08779b951c6a"
FLOW_ID = "b2965fbd-2779-4c01-b07d-3961555143c6"
ENDPOINT = "social_media" # The endpoint name of the flow

# Function to run the flow
def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Main function
def main():
    st.markdown(
    """
    <style>
    .stButton>button:hover {
        background-color: #1b0e4a; 
        color: white; 
    }
    
    .stApp {
        background-color: #1b0e4a; 
    }
    
    
    [data-testid="stSidebar"] {
        background-color: #302a47; 
    }
    header {
        background-color: #1b0e4a !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)
    st.sidebar.title(''' **Insightly** : A Social Media Performance App ''')
    

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Input field for the user
    message = st.sidebar.text_area("", placeholder="How can we assist you today?")

    # Button to send the query
    if st.sidebar.button("Give Insights"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            with st.spinner("Thinking of That ...."):
                response = run_flow(message)
                
                response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]

            # Append user message and response to chat history
            st.session_state["messages"].append({"user": message, "bot": response_text})

        except Exception as e:
            st.error(str(e))

    # Display chat history
    st.subheader("Chat History")
    st.write("--------")
    bot_color='#6af778'
    user_color='#f4fa57'
    for chat in st.session_state["messages"]:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<h5 ><strong style='color:{user_color};'>You:</strong> {chat['user']}</h5>",unsafe_allow_html=True)
            st.markdown(f"<h5><strong style='color:{bot_color};'>Bot:</strong> {chat['bot']}</h5>",unsafe_allow_html=True)
        
        with col2:
            if st.button(f"Copy", key=chat['bot'],):
                pyperclip.copy(chat['bot'])  # Copy the bot's message to clipboard
                st.success("Copied!")
                  # Adds a divider for better readability
        st.divider()
if __name__ == "__main__":
    main()
