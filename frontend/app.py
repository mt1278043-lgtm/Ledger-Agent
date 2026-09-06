"""Streamlit app for Ledger Agent."""

import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend import (
    initialize_agent,
    run_agent_with_input,
    run_ledger_analysis,
    record_transaction,
    calculate_balances,
    detect_inconsistencies,
    get_ledger_validation,
    get_ledger,
)


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


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Chat",
    "Ledger Analysis",
    "Record Transaction",
    "Balance Check",
    "Validate Ledger"
])

with tab1:
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

with tab2:
    st.subheader("Ledger Analysis")
    if st.button("Analyze Ledger"):
        with st.spinner("Analyzing ledger..."):
            df = get_ledger(st.session_state.ledger_data)
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                analysis = run_ledger_analysis(
                    st.session_state.agent,
                    st.session_state.ledger_data
                )
                st.write(analysis)
            else:
                st.info("No ledger data available. Please enter transactions first.")

with tab3:
    st.subheader("Record Transaction")
    transaction_request = st.text_area(
        "Describe the transaction you want to record:"
    )
    if st.button("Record Transaction"):
        with st.spinner("Recording transaction..."):
            response = record_transaction(
                st.session_state.agent,
                transaction_request,
                st.session_state.ledger_data
            )
            st.write(response)

with tab4:
    st.subheader("Balance Calculation")
    if st.button("Calculate Balances"):
        with st.spinner("Calculating balances..."):
            balances = calculate_balances(
                st.session_state.agent,
                st.session_state.ledger_data
            )
            st.write(balances)

with tab5:
    st.subheader("Validate Ledger")
    if st.button("Validate"):
        with st.spinner("Validating ledger..."):
            validation = get_ledger_validation(
                st.session_state.ledger_data
            )

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Is Balanced", validation["is_balanced"])
                st.metric("Total Debits", validation["total_debits"])
            with col2:
                st.metric("Total Credits", validation["total_credits"])
                st.metric("Imbalance", validation["difference"])

            st.info(validation["message"])

            inconsistencies = detect_inconsistencies(
                st.session_state.agent,
                st.session_state.ledger_data
            )
            st.subheader("Inconsistency Detection")
            st.write(inconsistencies)


st.divider()


st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 0.9rem;">
        Ledger Agent | Powered by Claude AI, LangGraph, Pandas and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
