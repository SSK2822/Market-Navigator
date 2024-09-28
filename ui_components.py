import streamlit as st

def display_stock_selector():
    return st.sidebar.selectbox("Choose a stock symbol:", ["AAPL", "TSLA", "NVDA"])

def display_controls():
    if st.sidebar.button("Refresh Data"):
        return True
    return False

def display_header(title):
    st.header(title)

def display_data_table(data):
    st.table(data)

def display_indicator_selector():
    return st.sidebar.selectbox(
        "Choose an indicator to display:",
        ["SMA", "EMA", "RSI", "ATH", "ATL", "ATR", "Market Movement", "Loss %", "Profit %", "ROC", "Swing Percent", "Close Price Table"]
    )

def display_graph(data, indicator):
    if indicator == "SMA":
        st.line_chart(data['sma'])
    elif indicator == "EMA":
        st.line_chart(data['ema'])
    elif indicator == "RSI":
        st.line_chart(data['rsi'])
    elif indicator == "ATH":
        st.line_chart(data['ath'])
    elif indicator == "ATL":
        st.line_chart(data['atl'])
    elif indicator == "ATR":
        st.line_chart(data['atr'])
    elif indicator == "Market Movement":
        st.line_chart(data['market_movement'])
    elif indicator == "Loss %":
        st.line_chart(data['loss_percent'])
    elif indicator == "Profit %":
        st.line_chart(data['profit_percent'])
    elif indicator == "ROC":
        st.line_chart(data['roc'])
    elif indicator == "Swing Percent":
        st.line_chart(data['swing_percent'])
    elif indicator == "Close Price Table":
        display_data_table(data[['close']])
