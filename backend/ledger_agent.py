"""Ledger analysis agent using Claude AI."""

from typing import Optional

from .agent import initialize_agent
from .ledger_data import format_ledger_for_analysis, validate_ledger
from .ledger_prompt import (
    get_ledger_analysis_prompt,
    get_transaction_recording_prompt,
    get_balance_calculation_prompt,
    get_inconsistency_detection_prompt,
)


def run_ledger_analysis(agent, ledger_data: Optional[dict] = None) -> str:
    """Run comprehensive ledger analysis using Claude AI."""
    ledger_formatted = format_ledger_for_analysis(ledger_data)
    prompt = get_ledger_analysis_prompt(ledger_formatted)

    try:
        response = agent.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(response, "content") and response.content:
            return response.content[0].text

        return str(response)

    except Exception as error:
        return f"Error during ledger analysis: {error}"


def record_transaction(
    agent,
    user_request: str,
    ledger_data: Optional[dict] = None
) -> str:
    """Help user record a transaction."""
    ledger_formatted = format_ledger_for_analysis(ledger_data)
    prompt = get_transaction_recording_prompt(ledger_formatted, user_request)

    try:
        response = agent.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(response, "content") and response.content:
            return response.content[0].text

        return str(response)

    except Exception as error:
        return f"Error recording transaction: {error}"


def calculate_balances(agent, ledger_data: Optional[dict] = None) -> str:
    """Calculate and analyze ledger balances."""
    ledger_formatted = format_ledger_for_analysis(ledger_data)
    prompt = get_balance_calculation_prompt(ledger_formatted)

    try:
        response = agent.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(response, "content") and response.content:
            return response.content[0].text

        return str(response)

    except Exception as error:
        return f"Error calculating balances: {error}"


def detect_inconsistencies(agent, ledger_data: Optional[dict] = None) -> str:
    """Detect inconsistencies in ledger data."""
    ledger_formatted = format_ledger_for_analysis(ledger_data)
    prompt = get_inconsistency_detection_prompt(ledger_formatted)

    try:
        response = agent.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(response, "content") and response.content:
            return response.content[0].text

        return str(response)

    except Exception as error:
        return f"Error detecting inconsistencies: {error}"


def get_ledger_validation(ledger_data: Optional[dict] = None) -> dict:
    """Get ledger validation status without AI."""
    return validate_ledger(ledger_data)
