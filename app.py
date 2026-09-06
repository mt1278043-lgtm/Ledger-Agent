"""Main entry point for running the Ledger Agent Streamlit app."""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    frontend_app = Path(__file__).parent / "frontend" / "app.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(frontend_app)])
