"""Ledger Management Agent using OpenAI, LangChain, and Pandas."""

import os
from typing import Optional

import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


def initialize_agent():
    """Initialize the OpenAI model."""

    model = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        temperature=0.3
    )

    return model


def get_ledger_dataframe(ledger_data: Optional[dict] = None) -> pd.DataFrame:
    """Convert ledger data into a Pandas DataFrame."""

    if not ledger_data:
        return pd.DataFrame()

    try:
        return pd.DataFrame(ledger_data)
    except Exception:
        return pd.DataFrame()


def calculate_ledger_summary(ledger_data: Optional[dict] = None) -> dict:
    """Calculate basic ledger statistics using Pandas."""

    dataframe = get_ledger_dataframe(ledger_data)

    if dataframe.empty:
        return {
            "total_entries": 0,
            "total_debits": 0,
            "total_credits": 0,
            "balance": 0
        }

    total_debits = 0
    total_credits = 0

    if "debit" in dataframe.columns:
        total_debits = pd.to_numeric(
            dataframe["debit"],
            errors="coerce"
        ).fillna(0).sum()

    if "credit" in dataframe.columns:
        total_credits = pd.to_numeric(
            dataframe["credit"],
            errors="coerce"
        ).fillna(0).sum()

    balance = total_credits - total_debits

    return {
        "total_entries": len(dataframe),
        "total_debits": float(total_debits),
        "total_credits": float(total_credits),
        "balance": float(balance)
    }


def build_ledger_context(ledger_data: Optional[dict] = None) -> str:
    """Create a readable ledger context for the language model."""

    dataframe = get_ledger_dataframe(ledger_data)

    if dataframe.empty:
        return "No ledger transactions are currently available."

    summary = calculate_ledger_summary(ledger_data)

    transactions = dataframe.to_string(index=False)

    return f"""
Ledger Transactions:

{transactions}

Ledger Summary:

Total Entries: {summary["total_entries"]}
Total Debits: {summary["total_debits"]}
Total Credits: {summary["total_credits"]}
Balance: {summary["balance"]}
"""


def run_agent_with_input(
    agent,
    user_input: str,
    ledger_data: Optional[dict] = None
) -> str:
    """Process the user's request using the OpenAI model."""

    ledger_context = build_ledger_context(ledger_data)

    prompt = f"""
You are a Ledger Management Assistant.

Your responsibilities are:

- Record financial transactions.
- Explain ledger entries.
- Calculate balances.
- Summarize financial transactions.
- Analyze debit and credit information.
- Identify possible inconsistencies in the provided ledger data.

Use the ledger information provided below.

{ledger_context}

User Request:

{user_input}

Instructions:

Provide a clear and accurate response.
Use the available ledger data when answering.
Do not invent transactions or financial values.
If required information is missing, clearly state that it is missing.
"""

    try:
        response = agent.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)

    except Exception as error:
        return f"Error while processing the request: {error}"


if __name__ == "__main__":
    agent = initialize_agent()

    sample_ledger = {
        "date": ["2026-09-01", "2026-09-02"],
        "description": [
            "Office Supplies",
            "Customer Payment"
        ],
        "debit": [500, 0],
        "credit": [0, 1500]
    }

    response = run_agent_with_input(
        agent,
        "Give me a summary of my ledger and calculate the balance.",
        sample_ledger
    )

    print(response)
