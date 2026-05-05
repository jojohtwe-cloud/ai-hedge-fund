import streamlit as st
import sys
import os
import re
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Inject Streamlit Cloud secrets into environment
if hasattr(st, "secrets"):
    for _k, _v in st.secrets.items():
        if isinstance(_v, str):
            os.environ.setdefault(_k, _v)

from src.main import run_hedge_fund
from src.utils.display import print_trading_output
import io
import contextlib

_ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*[mK]')

def strip_ansi(text: str) -> str:
    return _ANSI_ESCAPE.sub('', text)

st.title("AI Hedge Fund Simulator")

st.markdown("""
This is an AI-powered hedge fund simulator that uses multiple investment agents to make trading decisions.
**Disclaimer**: This is for educational purposes only. Not for real trading.
""")

# Sidebar for inputs
st.sidebar.header("Configuration")

tickers_input = st.sidebar.text_input("Tickers (comma-separated)", "AAPL,MSFT,NVDA")
tickers = [t.strip() for t in tickers_input.split(',') if t.strip()]

initial_cash = st.sidebar.number_input("Initial Cash", value=100000.0, min_value=0.0)
margin_requirement = st.sidebar.slider("Margin Requirement", 0.0, 1.0, 0.5)

start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.now())

show_reasoning = st.sidebar.checkbox("Show Reasoning", value=False)

# Model selection — names update based on chosen provider
MODEL_OPTIONS = {
    "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-4.1"],
    "Anthropic": ["claude-opus-4-7", "claude-sonnet-4-6", "claude-3-5-sonnet-20241022"],
    "Groq": ["llama3-70b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"],
    "DeepSeek": ["deepseek-chat", "deepseek-reasoner"],
}

model_provider = st.sidebar.selectbox("Model Provider", list(MODEL_OPTIONS.keys()))
model_name = st.sidebar.selectbox("Model Name", MODEL_OPTIONS[model_provider])

st.sidebar.markdown("---")
st.sidebar.markdown("**Important**: Set your API keys in Streamlit Cloud secrets or a `.env` file.")

if st.button("Run Hedge Fund"):
    if not tickers:
        st.error("Please enter at least one ticker.")
    elif start_date >= end_date:
        st.error("Start date must be before end date.")
    else:
        with st.spinner("Running AI Hedge Fund... This may take a few minutes."):
            portfolio = {
                "cash": initial_cash,
                "margin_requirement": margin_requirement,
                "margin_used": 0.0,
                "positions": {
                    ticker: {
                        "long": 0,
                        "short": 0,
                        "long_cost_basis": 0.0,
                        "short_cost_basis": 0.0,
                        "short_margin_used": 0.0,
                    }
                    for ticker in tickers
                },
                "realized_gains": {
                    ticker: {
                        "long": 0.0,
                        "short": 0.0,
                    }
                    for ticker in tickers
                },
            }

            try:
                result = run_hedge_fund(
                    tickers=tickers,
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    portfolio=portfolio,
                    show_reasoning=show_reasoning,
                    model_name=model_name,
                    model_provider=model_provider,
                )

                output_buffer = io.StringIO()
                with contextlib.redirect_stdout(output_buffer):
                    print_trading_output(result)

                st.success("Hedge Fund Run Complete!")
                st.text_area("Output", strip_ansi(output_buffer.getvalue()), height=400)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.text("Please check your API keys and try again.")
