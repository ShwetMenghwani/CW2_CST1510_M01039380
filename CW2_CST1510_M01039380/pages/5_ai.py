import streamlit as st
from openai import OpenAI

st.title("🤖 AI Assistant")

# Create OpenAI client using Streamlit Secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input box
user_msg = st.chat_input("Ask something...")

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    ai_reply = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    with st.chat_message("assistant"):
        st.write(ai_reply)