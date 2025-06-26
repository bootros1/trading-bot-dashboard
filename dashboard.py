import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 60 seconds
st_autorefresh(interval=60000, key="datarefresh")

# Data source selection
data_source = st.selectbox("Select data source", ["Backtest", "Live"])

# --- Page Configuration ---
st.set_page_config(
    page_title="Forex Bot Performance Dashboard",
    page_icon="🤖",
    layout="wide"
)

# --- Load Data ---
@st.cache_data
def load_data(filepath):
    try:
        data = pd.read_csv(filepath)
        if data.empty:
            return "empty"
        if 'time' in data.columns:
            data['time'] = pd.to_datetime(data['time'])
        return data
    except FileNotFoundError:
        return "not_found"
    except pd.errors.EmptyDataError:
        return "empty"

# Use the selected data source
results_obj = load_data('logs/backtest_results.csv' if data_source == "Backtest" else 'logs/trades.csv')

# --- Main Application ---
st.title("🤖 Forex Bot Performance Dashboard")
st.markdown("This dashboard visualizes the performance of the automated trading bot based on backtest or live results.")

if isinstance(results_obj, str):
    if results_obj == "not_found":
        st.error("No data found. Please run a backtest or live trading session first.")
    elif results_obj == "empty":
        st.warning("The results file is empty. This usually means no trades were executed.")
        st.info("💡 Try adjusting your strategy, symbol list, or the historical data range.")
else:
    results_df = results_obj

    # --- Filters ---
    st.sidebar.header("Filters")
    symbols = results_df['symbol'].unique()
    selected_symbols = st.sidebar.multiselect("Symbols", symbols, default=list(symbols))
    filtered_df = results_df[results_df['symbol'].isin(selected_symbols)]

    # --- Key Performance Indicators (KPIs) ---
    st.header("Key Performance Metrics")
    if 'pnl' in filtered_df.columns and 'balance' in filtered_df.columns:
        total_trades = len(filtered_df)
        winning_trades = len(filtered_df[filtered_df['pnl'] > 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        total_pnl = filtered_df['pnl'].sum()
        gross_profit = filtered_df[filtered_df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(filtered_df[filtered_df['pnl'] < 0]['pnl'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total PnL", f"${total_pnl:,.2f}")
        col2.metric("Win Rate", f"{win_rate:.2f}%")
        col3.metric("Profit Factor", f"{profit_factor:.2f}")
        col4.metric("Total Trades", total_trades)

        # --- Advanced Metrics ---
        st.header("Advanced Metrics")
        avg_win = filtered_df[filtered_df['pnl'] > 0]['pnl'].mean()
        avg_loss = filtered_df[filtered_df['pnl'] < 0]['pnl'].mean()
        max_drawdown = (filtered_df['balance'].cummax() - filtered_df['balance']).max() if 'balance' in filtered_df.columns else None
        sharpe = filtered_df['pnl'].mean() / filtered_df['pnl'].std() * np.sqrt(252) if filtered_df['pnl'].std() > 0 else None

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg Win", f"${avg_win:,.2f}")
        col2.metric("Avg Loss", f"${avg_loss:,.2f}")
        col3.metric("Max Drawdown", f"${max_drawdown:,.2f}" if max_drawdown is not None else "N/A")
        col4.metric("Sharpe Ratio", f"{sharpe:.2f}" if sharpe is not None else "N/A")

        # --- Equity Curve Chart ---
        st.header("Equity Curve")
        fig = px.line(filtered_df, x=filtered_df.index, y='balance', title='Account Balance Over Time', labels={'index': 'Trade Number', 'balance': 'Account Balance ($)'})
        fig.update_layout(
            xaxis_title="Trade Number",
            yaxis_title="Account Balance ($)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Win/Loss Pie Chart ---
        st.header("Win vs Loss")
        win_loss = filtered_df['pnl'] > 0
        win_loss_counts = win_loss.value_counts()
        fig_pie = px.pie(values=win_loss_counts, names=['Win', 'Loss'], title='Win vs Loss')
        st.plotly_chart(fig_pie, use_container_width=True)

        # --- PnL Histogram ---
        st.header("PnL Distribution")
        fig_hist = px.histogram(filtered_df, x='pnl', nbins=30, title='Trade PnL Distribution')
        st.plotly_chart(fig_hist, use_container_width=True)

        # --- Latest Trade Notification ---
        st.header("Latest Trade")
        st.write(filtered_df.iloc[-1] if not filtered_df.empty else "No trades yet.")

        # --- Download Button ---
        st.download_button("Download Trade Log as CSV", filtered_df.to_csv(index=False), "trade_log.csv")

    # --- Trade Log Table ---
    st.header("Trade Log")
    st.dataframe(filtered_df)

    # Add a little footer
    st.markdown("---")
    st.text("Run a new backtest or live session to update the data.")