import streamlit as st
from data_fetching import fetch_historical_data, get_data_frame, fetch_data_yfinance, fetch_fundamental_data
from data_processing import (
    calculate_sma, calculate_ema, calculate_rsi, calculate_ath, calculate_atl,
    calculate_atr, calculate_market_movement, calculate_loss_percent,
    calculate_profit_percent, calculate_roc, calculate_swing_percent
)
from ui_components import (display_stock_selector, display_controls, display_header,
                           display_data_table, display_indicator_selector, display_graph)
from cache_management import clear_cache

# Setup page configuration
st.set_page_config(page_title="Market Navigator", layout="wide")

def display_stock_data(symbol):
    historical_data = fetch_historical_data(symbol)
    if historical_data:
        st.write("Connection to Alpha Vantage API Successful")
        df = get_data_frame(historical_data)
    else:
        st.error("Failed to fetch historical data from Alpha Vantage. Trying yFinance...")
        df = fetch_data_yfinance(symbol)
        if df.empty:
            st.error("Failed to fetch historical data from yFinance as well. Please check the ticker symbol or your network connection.")
            return

    if not df.empty:
        # Calculate indicators
        df['sma'] = calculate_sma(df)
        df['ema'] = calculate_ema(df)
        df['rsi'] = calculate_rsi(df)
        df['ath'] = calculate_ath(df)
        df['atl'] = calculate_atl(df)
        df['atr'] = calculate_atr(df)
        df['market_movement'] = calculate_market_movement(df)
        df['loss_percent'] = calculate_loss_percent(df)
        df['profit_percent'] = calculate_profit_percent(df)
        df['roc'] = calculate_roc(df)
        df['swing_percent'] = calculate_swing_percent(df)

        # Displaying data in a table
        st.subheader(f"Indicator Data for {symbol}")
        st.dataframe(df[['close', 'sma', 'ema', 'rsi', 'ath', 'atl', 'atr', 'market_movement', 'loss_percent', 'profit_percent', 'roc', 'swing_percent']])

        # Dropdown for graph visualization
        indicator_to_display = st.selectbox(
            "Choose an indicator to visualize:",
            ["SMA", "EMA", "RSI", "ATH", "ATL", "ATR", "Market Movement", "Loss %", "Profit %", "ROC", "Swing Percent"],
            key='indicator_selector'
        )

        # Display graph based on selection
        if indicator_to_display:
            display_graph(df, indicator_to_display)
    else:
        st.error("No data available for the selected stock.")

    # Button to clear the cache
    if st.button("Clear Cache - Update to Latest Info"):
        clear_cache(f"historical_{symbol}")
        clear_cache(f"yfinance_{symbol}")
        clear_cache(f"fundamental_{symbol}")
        st.success("Cache cleared. Please select the Stock Ticker again.")

def display_fundamental_data(symbol):
    fundamental_data = fetch_fundamental_data(symbol)
    if fundamental_data:
        st.subheader(f"Fundamental Data for {symbol}")
        for key, value in fundamental_data.items():
            if isinstance(value, float):
                formatted_value = f"{value:.2f}"
            else:
                formatted_value = value
            st.write(f"{key}: {formatted_value}")

def main():
    st.title("Market Navigator")
    selected_stock = st.selectbox("Select a stock symbol", ["AAPL", "TSLA", "NVDA", "GOOGL", "MSFT", "AMZN", "META"], index=0)

    # Check if the selection has changed
    if 'selected_stock' not in st.session_state or st.session_state.selected_stock != selected_stock:
        st.session_state.selected_stock = selected_stock
        display_fundamental_data(selected_stock)
        display_stock_data(selected_stock)
    else:
        display_fundamental_data(st.session_state.selected_stock)
        display_stock_data(st.session_state.selected_stock)

if __name__ == "__main__":
    main()
