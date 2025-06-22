import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
# Forcing a cache clear by adding a comment
st.set_page_config(
    page_title="Forex Bot Performance Dashboard",
    page_icon="🤖",
    layout="wide"
)

# --- Load Data ---
@st.cache_data
def load_data(filepath):
    """
    Loads the backtest results CSV.
    Returns the DataFrame on success, or a string indicating the error type.
    """
    try:
        data = pd.read_csv(filepath)
        if data.empty:
            return "empty"  # File has headers but no data
        data['time'] = pd.to_datetime(data.get('time'))
        return data
    except FileNotFoundError:
        return "not_found"
    except pd.errors.EmptyDataError:
        return "empty"  # File is completely empty

# --- Main Application ---
st.title("🤖 Forex Bot Performance Dashboard")
st.markdown("This dashboard visualizes the performance of the automated trading bot based on backtest results.")

# Load the data and handle different states
results_obj = load_data('logs/backtest_results.csv')

if isinstance(results_obj, str):
    if results_obj == "not_found":
        st.error("No backtest data found. Please run a backtest first by setting `BACKTEST = True` in `config.py` and running `main.py`.")
    elif results_obj == "empty":
        st.warning("The backtest results file is empty. This usually means no trades were executed during the backtest.")
        st.info("💡 Try adjusting your strategy, symbol list, or the historical data range.")
else:
    results_df = results_obj
    # --- Key Performance Indicators (KPIs) ---
    st.header("Key Performance Metrics")

    total_trades = len(results_df)
    winning_trades = len(results_df[results_df['pnl'] > 0])
    losing_trades = len(results_df[results_df['pnl'] < 0])
    
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    total_pnl = results_df['pnl'].sum()
    
    gross_profit = results_df[results_df['pnl'] > 0]['pnl'].sum()
    gross_loss = abs(results_df[results_df['pnl'] < 0]['pnl'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total PnL", f"${total_pnl:,.2f}")
    col2.metric("Win Rate", f"{win_rate:.2f}%")
    col3.metric("Profit Factor", f"{profit_factor:.2f}")
    col4.metric("Total Trades", total_trades)

    # --- Equity Curve Chart ---
    st.header("Equity Curve")
    fig = px.line(results_df, x=results_df.index, y='balance', title='Account Balance Over Time', labels={'index': 'Trade Number', 'balance': 'Account Balance ($)'})
    fig.update_layout(
        xaxis_title="Trade Number",
        yaxis_title="Account Balance ($)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Trade Log ---
    st.header("Trade Log")
    st.dataframe(results_df)

    # Add a little footer
    st.markdown("---")
    st.text("Run a new backtest to update the data.") 