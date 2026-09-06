"""Prompt templates for ledger analysis using Claude AI."""


LEDGER_ANALYSIS_PROMPT = """
You are a financial ledger analyst AI. Analyze the following ledger transactions and provide insights.

Ledger Data:
{ledger_data}

Tasks:
1. Identify if the debits equal credits.
2. Highlight any imbalances or potential errors.
3. Provide a summary of the ledger status and any patterns you observe.
4. List any recommendations for ledger management.

Please provide a clear, professional analysis."""


TRANSACTION_RECORDING_PROMPT = """
You are a ledger assistant helping to record financial transactions.

Current Ledger:
{ledger_data}

User Request: {user_request}

Help the user by:
1. Confirming the transaction details they want to record.
2. Suggesting the appropriate debit and credit accounts.
3. Providing a summary of how this transaction affects the ledger.

Be concise and professional."""


BALANCE_CALCULATION_PROMPT = """
You are a financial analyst calculating ledger balances.

Ledger Data:
{ledger_data}

Provide:
1. Total debits and total credits.
2. The balance (credits - debits).
3. Whether the ledger is balanced.
4. Any observations about the account balances.

Format your response clearly with calculations shown."""


INCONSISTENCY_DETECTION_PROMPT = """
You are a financial auditor detecting inconsistencies in ledger data.

Ledger Data:
{ledger_data}

Analyze for:
1. Duplicate entries or transactions.
2. Unusual amounts or patterns.
3. Missing or incomplete transaction details.
4. Timing or sequence issues.

List any inconsistencies found and suggest corrections."""


def get_ledger_analysis_prompt(ledger_data: str) -> str:
    """Get formatted ledger analysis prompt."""
    return LEDGER_ANALYSIS_PROMPT.format(ledger_data=ledger_data)


def get_transaction_recording_prompt(ledger_data: str, user_request: str) -> str:
    """Get formatted transaction recording prompt."""
    return TRANSACTION_RECORDING_PROMPT.format(
        ledger_data=ledger_data,
        user_request=user_request
    )


def get_balance_calculation_prompt(ledger_data: str) -> str:
    """Get formatted balance calculation prompt."""
    return BALANCE_CALCULATION_PROMPT.format(ledger_data=ledger_data)


def get_inconsistency_detection_prompt(ledger_data: str) -> str:
    """Get formatted inconsistency detection prompt."""
    return INCONSISTENCY_DETECTION_PROMPT.format(ledger_data=ledger_data)
