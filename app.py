"""
Cambridge Accelerate LLM Workshop
Minimal Chat Interface for Testing vLLM
"""

import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="Cambridge LLM Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Cambridge LLM Chat")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    api_url = st.text_input(
        "API Base URL",
        value="http://your-server:8000/v1",
        help="Enter the vLLM API endpoint"
    )
    
    api_key = st.text_input(
        "API Key",
        value="EMPTY",
        type="password",
        help="Enter your API key"
    )
    
    model_name = st.text_input(
        "Model Name",
        value="meta-llama/Llama-3.1-8B-Instruct",
        help="Model to use"
    )
    
    max_tokens = st.slider("Max Tokens", 50, 1000, 500)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Initialize OpenAI client
            client = OpenAI(
                api_key=api_key,
                base_url=api_url,
                timeout=120.0
            )
            
            # Call the API with streaming
            full_response = ""
            
            with st.spinner("Thinking..."):
                stream = client.chat.completions.create(
                    model=model_name,
                    messages=st.session_state.messages,
                    max_tokens=max_tokens,
                    stream=True
                )
                
                # Stream the response
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
