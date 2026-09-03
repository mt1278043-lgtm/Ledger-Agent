"""LangGraph agent for ledger management."""
from typing import TypedDict
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
import json


class AgentState(TypedDict):
    """State for the ledger agent."""
    messages: list
    ledger_data: dict
    current_action: str


def get_system_prompt() -> str:
    """Get the system prompt for the ledger agent."""
    return """You are a helpful ledger management assistant. You help users:
1. Record transactions
2. View ledger summaries
3. Calculate balances
4. Analyze financial data

When a user asks for a transaction record, extract the details and provide clear responses.
Always be professional and accurate with financial data."""


def initialize_agent():
    """Initialize the LangGraph agent."""
    model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

    def process_message(state: AgentState) -> AgentState:
        """Process user message and generate response."""
        system_prompt = get_system_prompt()

        # Prepare messages for the model
        messages = [
            {"role": "system", "content": system_prompt},
            *state["messages"]
        ]

        # Get response from Claude
        response = model.invoke(messages)

        # Update state
        state["messages"].append({
            "role": "assistant",
            "content": response.content
        })
        state["current_action"] = "message_processed"

        return state

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("process_message", process_message)

    # Set entry point and end point
    workflow.set_entry_point("process_message")
    workflow.add_edge("process_message", END)

    # Compile the graph
    app = workflow.compile()
    return app


def run_agent_with_input(agent, user_input: str, ledger_data: dict = None) -> str:
    """Run the agent with user input."""
    if ledger_data is None:
        ledger_data = {}

    initial_state = {
        "messages": [{"role": "user", "content": user_input}],
        "ledger_data": ledger_data,
        "current_action": "initialized"
    }

    result = agent.invoke(initial_state)

    # Return the last assistant message
    for msg in reversed(result["messages"]):
        if msg.get("role") == "assistant":
            return msg["content"]

    return "No response generated"


if __name__ == "__main__":
    agent = initialize_agent()
    response = run_agent_with_input(agent, "Hello! Can you help me manage my ledger?")
    print(response)
