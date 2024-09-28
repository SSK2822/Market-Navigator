import numpy as np
import pandas as pd

def calculate_ath(df):
    return df['high'].max()

def calculate_atl(df):
    return df['low'].min()

def calculate_ema(df, span=12):
    return df['close'].ewm(span=span, adjust=False).mean()

def calculate_sma(df, window=20):
    return df['close'].rolling(window=window).mean()

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    return true_range.rolling(window=period).mean()

def calculate_market_movement(df):
    return (df['close'] - df['close'].shift(1)) / df['close'].shift(1) * 100

def calculate_loss_percent(df):
    return (df['high'].rolling(min_periods=1, window=len(df)).max() - df['close']) / df['high'].rolling(min_periods=1, window=len(df)).max() * 100

def calculate_profit_percent(df):
    return (df['close'] - df['low'].rolling(min_periods=1, window=len(df)).min()) / df['low'].rolling(min_periods=1, window=len(df)).min() * 100

def calculate_roc(df, period=14):
    return df['close'].diff(period) / df['close'].shift(period) * 100

def calculate_rsi(df, periods=14):
    delta = df['close'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(window=periods).mean()
    ma_down = down.rolling(window=periods).mean()
    rsi = ma_up / (ma_up + ma_down) * 100
    return rsi

def calculate_swing_percent(df):
    previous_low = df['low'].shift(1)
    previous_high = df['high'].shift(1)
    swing = (df['high'] - previous_low) / (previous_high - previous_low) * 100
    return swing

def extract_close_prices(df):
    return df[['close']].reset_index().rename(columns={'index': 'date'})
