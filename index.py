import logging

import streamlit as st
from llm_provider import LLMProvider

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

st.set_page_config(page_title = "LLM Powered Chat Assistance", page_icon = "🤖")
st.title(body = "🤖 LLM Powered Chat Assistance")

# Reset conversation
if st.button("🎲 Reset Conversation"):
    st.session_state.messages = [{"role": "assistant", "content": "Conversation reset. How can I assist you?"}]
    st.rerun()

# Declaring LLM
llm = "openai"

# Initializing Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Initializing LLM Provider
provider = LLMProvider(provider = llm, messages = st.session_state.messages)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here ..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = provider.run_gemini_llm() if llm == "gemini" else provider.run_openai_llm()
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
    
    except Exception as e:
        logging.exception(f"Unexpected Error Occurred: {e}")
        st.write("Unexpected Error Occurred, while calling the LLM")