"""Streamlit app for Ledger Agent."""
import streamlit as st
import os
from dotenv import load_dotenv
from agent import initialize_agent, run_agent_with_input

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Ledger Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = initialize_agent()
    st.session_state.messages = []
    st.session_state.ledger_data = {}

# Title
st.title("📊 Ledger Management Agent")
st.markdown("---")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    st.write("**Agent Configuration**")
    show_debug = st.checkbox("Show Debug Info", value=False)

    # Clear history button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.ledger_data = {}
        st.success("Chat history cleared!")

# Main chat area
st.subheader("Chat with Ledger Agent")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask me about your ledger or transactions...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Get agent response
    with st.spinner("Processing..."):
        response = run_agent_with_input(
            st.session_state.agent,
            user_input,
            st.session_state.ledger_data
        )

    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # Display assistant response
    with st.chat_message("assistant"):
        st.write(response)

    # Show debug info if enabled
    if show_debug:
        st.divider()
        st.caption("**Debug Info**")
        st.json({
            "message_count": len(st.session_state.messages),
            "ledger_entries": len(st.session_state.ledger_data)
        })

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.9rem;">
        Ledger Agent • Powered by LangGraph & Streamlit
    </div>
""", unsafe_allow_html=True)
