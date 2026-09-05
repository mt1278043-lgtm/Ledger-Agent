"""Streamlit app for Ledger Agent."""

import streamlit as st
from dotenv import load_dotenv

from agent import initialize_agent, run_agent_with_input


load_dotenv()


st.set_page_config(
    page_title="Ledger Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }

    .stTitle {
        color: #2c3e50;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if "agent" not in st.session_state:
    st.session_state.agent = initialize_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ledger_data" not in st.session_state:
    st.session_state.ledger_data = {}


st.title("Ledger Management Agent")
st.markdown("---")


with st.sidebar:
    st.header("Settings")

    show_debug = st.checkbox(
        "Show Debug Information",
        value=False
    )

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.ledger_data = {}
        st.success("Chat history cleared.")


st.subheader("Chat with Ledger Agent")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_input = st.chat_input(
    "Ask about your ledger or transactions..."
)


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.write(user_input)


    with st.chat_message("assistant"):

        with st.spinner("Processing..."):

            try:
                response = run_agent_with_input(
                    st.session_state.agent,
                    user_input,
                    st.session_state.ledger_data
                )

            except Exception as error:
                response = (
                    "An error occurred while processing "
                    f"your request: {error}"
                )

        st.write(response)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


    if show_debug:

        st.divider()

        st.caption("Debug Information")

        st.json(
            {
                "message_count": len(
                    st.session_state.messages
                ),
                "ledger_entries": len(
                    st.session_state.ledger_data
                )
            }
        )


st.divider()


st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 0.9rem;">
        Ledger Agent | Powered by Claude AI, LangGraph, Pandas and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
