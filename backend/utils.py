"""Utility functions for the Ledger Agent backend."""

import os

from dotenv import load_dotenv


def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()


def get_api_key():
    """Get the Anthropic API key from environment."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return api_key
