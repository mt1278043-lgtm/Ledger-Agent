"""Ledger data management and operations."""

from typing import Optional

import pandas as pd


def get_ledger(ledger_data: Optional[dict] = None) -> pd.DataFrame:
    """Get ledger data as a pandas DataFrame."""
    if not ledger_data:
        return pd.DataFrame()

    try:
        return pd.DataFrame(ledger_data)
    except Exception:
        return pd.DataFrame()


def validate_ledger(ledger_data: Optional[dict] = None) -> dict:
    """Validate ledger balances and consistency."""
    df = get_ledger(ledger_data)

    if df.empty:
        return {
            "is_balanced": True,
            "total_debits": 0,
            "total_credits": 0,
            "difference": 0,
            "message": "No ledger data to validate"
        }

    total_debits = 0
    total_credits = 0

    if "debit" in df.columns:
        total_debits = pd.to_numeric(
            df["debit"],
            errors="coerce"
        ).fillna(0).sum()

    if "credit" in df.columns:
        total_credits = pd.to_numeric(
            df["credit"],
            errors="coerce"
        ).fillna(0).sum()

    difference = abs(total_debits - total_credits)
    is_balanced = difference < 0.01

    return {
        "is_balanced": is_balanced,
        "total_debits": float(total_debits),
        "total_credits": float(total_credits),
        "difference": float(difference),
        "message": "Ledger is balanced" if is_balanced else f"Imbalance detected: {difference}"
    }


def format_ledger_for_analysis(ledger_data: Optional[dict] = None) -> str:
    """Format ledger data for AI analysis."""
    df = get_ledger(ledger_data)

    if df.empty:
        return "No ledger transactions available for analysis."

    validation = validate_ledger(ledger_data)
    table_str = df.to_string(index=False)

    return f"""
Ledger Transactions:
{table_str}

Validation Status:
- Is Balanced: {validation['is_balanced']}
- Total Debits: {validation['total_debits']}
- Total Credits: {validation['total_credits']}
- Imbalance: {validation['difference']}
- Status Message: {validation['message']}
"""
