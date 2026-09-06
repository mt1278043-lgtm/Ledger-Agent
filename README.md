# Ledger Agent

A sophisticated ledger management system built with LangGraph and Streamlit, powered by Claude AI.

## Features

- 💬 Interactive chat interface with Claude AI
- 📊 Ledger management and transaction tracking
- 🔄 State management using LangGraph
- 🎨 Modern Streamlit UI
- ⚡ Fast and responsive

## Prerequisites

- Python 3.8+
- Anthropic API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Ledger-Agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Running the Application

Start the Streamlit app on localhost:

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Project Structure

```
Ledger-Agent/
├── frontend/                  # Frontend Streamlit UI
│   ├── app.py                # Main Streamlit application
│   └── __init__.py          # Frontend package init
├── backend/                   # Backend logic and AI agent
│   ├── agent.py             # Claude AI agent configuration
│   ├── utils.py             # Utility functions
│   └── __init__.py          # Backend package init
├── app.py                     # Main entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Usage

1. Open the app in your browser
2. Type your queries about ledger management
3. The AI agent will help you with:
   - Recording transactions
   - Viewing balances
   - Analyzing financial data
   - Managing ledger entries

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
- `STREAMLIT_SERVER_PORT`: Port for Streamlit (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

## Development

To add new features:

1. Modify `agent.py` for agent logic
2. Modify `app.py` for UI changes
3. Update `requirements.txt` for new dependencies

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
