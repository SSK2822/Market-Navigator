import requests
import pandas as pd
import yfinance as yf
import streamlit as st
from cache_management import cache_data, get_cached_data, clear_cache


API_KEY = "13983GNLN4GLUCXP"

# Define a list of supported tickers
SUPPORTED_TICKERS = ["AAPL", "TSLA", "NVDA", "GOOGL", "MSFT", "AMZN", "META"]

def fetch_historical_data(symbol):
    if symbol not in SUPPORTED_TICKERS:
        raise ValueError(f"Unsupported ticker: {symbol}. Supported tickers are: {SUPPORTED_TICKERS}")

    # Cached memory
    cached_data = get_cached_data(f"historical_{symbol}")
    if cached_data:
        last_date = list(cached_data['Time Series (Daily)'])[0] if 'Time Series (Daily)' in cached_data else "No Date"
        st.write(f"Retrieved historical data for {symbol} from cache.")
        st.write(f"Cache dated {last_date} for all the data")
        return cached_data

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "Error Message" in data:
            raise Exception(f"Error fetching data: {data['Error Message']}")

        # Cache the data
        cache_data(f"historical_{symbol}", data)
        return data
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    return None

def get_data_frame(time_series_data):
    """
    Converts raw time series data into a pandas DataFrame.
    """
    daily_data = time_series_data.get('Time Series (Daily)', {})
    df = pd.DataFrame.from_dict(daily_data, orient='index', dtype=float)
    df.rename(columns=lambda s: s[3:], inplace=True)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    return df

def fetch_data_yfinance(symbol):
    # Check if data is in cache first
    cached_data = get_cached_data(f"yfinance_{symbol}")
    if cached_data:
        st.write(f"Retrieved data for {symbol} from cache.")
        return cached_data

    stock = yf.Ticker(symbol)
    df = stock.history(period="1y")
    df.reset_index(inplace=True)
    df.rename(columns={"Date": "date", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"}, inplace=True)

    # Cache the data
    cache_data(f"yfinance_{symbol}", df.to_dict())
    return df

def fetch_fundamental_data(symbol):
    # Check if data is in cache first
    cached_data = get_cached_data(f"fundamental_{symbol}")
    if cached_data:
        st.write(f"Retrieved fundamental data for {symbol} to cache.")
        return cached_data

    stock = yf.Ticker(symbol)
    info = stock.info
    fundamental_data = {
        'EPS': info.get('trailingEps', 'N/A'),
        'Debt-to-Equity Ratio': info.get('debtToEquity', 'N/A'),
        'P/E Ratio': info.get('trailingPE', 'N/A'),
        'ROE': info.get('returnOnEquity', 'N/A'),
        'Dividend Yield': info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A',  # Convert to percentage
        'Market Cap': info.get('marketCap', 'N/A'),
        'Profit Margin': info.get('profitMargins', 'N/A')
    }

    # Cache the data
    cache_data(f"fundamental_{symbol}", fundamental_data)
    return fundamental_data
